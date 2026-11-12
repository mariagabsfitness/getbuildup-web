// ---------------------------------------------------------------------------
//  getbuildup.app — Worker
//
//  1. Sirve el sitio estatico (dist/) igual que antes.
//  2. Escucha el webhook de RevenueCat en /api/rc-webhook y manda el correo
//     de bienvenida con Resend, funcione la compra por web, App Store o
//     Google Play.
//
//  Secretos que necesita (se ponen en Cloudflare, nunca en el repo):
//    RESEND_API_KEY      clave de Resend (empieza por re_)
//    RC_WEBHOOK_SECRET   la misma palabra secreta que se pone en RevenueCat
//    FIREBASE_SA         el JSON completo de la cuenta de servicio de Firebase
// ---------------------------------------------------------------------------

import PLANTILLAS from "./plantillas.js";

const REMITENTE = '"BuildUp by MariaGabsFitness" <hola@getbuildup.app>';
const RESPONDER_A = "buildup@mariagabsfitness.com";
// Hora de Miami a la que sale el correo de vuelta, la tarde siguiente.
const HORA_ENVIO = 16;
const ASUNTOS = {
  bienvenida: "Ya estás dentro de BuildUp \u2661",
  lanzamiento: "BuildUp ya está aquí \u2661",
  general: "BuildUp ya está aquí \u2661",
  primeras: "Tú ya estabas aquí \u2661",
  cancelacion: "¿Me cuentas qué pasó?",
  clave: "Crea una contraseña nueva",
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === "/api/rc-webhook") {
      return manejarWebhook(request, env, ctx);
    }

    if (url.pathname === "/api/clave") {
      return manejarClave(request, env, ctx);
    }

    // Cualquier otra cosa: el sitio estatico de siempre.
    return env.ASSETS.fetch(request);
  },

  // El reloj de Cloudflare nos despierta a las 20:00 y a las 21:00 UTC. Solo
  // una de las dos es la tarde de Miami, segun el horario de verano.
  async scheduled(evento, env, ctx) {
    const hora = new Date(evento.scheduledTime + desfaseMiami(new Date(evento.scheduledTime))).getUTCHours();
    if (hora !== HORA_ENVIO) {
      console.log("reloj a las " + hora + "h de Miami: no toca");
      return;
    }
    ctx.waitUntil(revisarCola(env, false));
  },
};

// ---------------------------------------------------------------------------
//  Webhook
// ---------------------------------------------------------------------------

async function manejarWebhook(request, env, ctx) {
  if (request.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }

  // Autenticacion: RevenueCat manda la cabecera Authorization que configuramos.
  const esperado = env.RC_WEBHOOK_SECRET || "";
  const recibido = request.headers.get("Authorization") || "";
  if (!esperado || !iguales(recibido, esperado)) {
    return new Response("Unauthorized", { status: 401 });
  }

  let cuerpo;
  try {
    cuerpo = await request.json();
  } catch (_) {
    return new Response("Bad JSON", { status: 400 });
  }

  const ev = cuerpo && cuerpo.event ? cuerpo.event : {};
  const tipo = ev.type || "";

  // Crear las campanas en Resend con el HTML exacto, sin pasar por el editor
  // del panel (que reordena las tablas y descoloca el diseno).
  if (tipo === "TEST" && env.TEST_PLANTILLA === "crear-campanas") {
    const r = await crearCampanas(env);
    return new Response(JSON.stringify(r, null, 1), {
      status: 200,
      headers: { "content-type": "application/json" },
    });
  }

  // Prueba del correo programado: lo deja en la cola de Resend para manana y
  // acto seguido lo cancela, como si la persona se hubiera vuelto a suscribir.
  // Sirve para comprobar que las dos mitades funcionan sin esperar un dia.
  if (tipo === "TEST" && env.TEST_PLANTILLA === "probar-programado") {
    if (!env.TEST_UID) return respuestaOk("ignorado: falta TEST_UID");
    const falso = {
      type: "EXPIRATION",
      app_user_id: env.TEST_UID,
      store: "PRUEBA",
      expiration_at_ms: Date.now(),
      subscriber_attributes: {},
    };
    await apuntarPendiente(falso, env);
    const mandados = await revisarCola(env, true);
    return respuestaOk("prueba de la cola hecha, mandados: " + mandados);
  }

  // Prueba manual: el boton "Send Test Event" de RevenueCat manda un evento
  // TEST. Si hay un TEST_UID configurado, hacemos el recorrido completo con
  // ese usuario para comprobar Firebase + Resend sin tener que comprar nada.
  if (tipo === "TEST") {
    if (!env.TEST_UID) return respuestaOk("ignorado: TEST (sin TEST_UID)");
    const falso = {
      type: "INITIAL_PURCHASE",
      app_user_id: env.TEST_UID,
      store: "PRUEBA",
      expiration_at_ms: Date.now() + 7 * 24 * 60 * 60 * 1000,
      subscriber_attributes: {},
    };
    const cual = env.TEST_PLANTILLA || "bienvenida";
    ctx.waitUntil(enviarBienvenida(falso, env, cual));
    return respuestaOk("prueba (" + cual + ") encolada para " + env.TEST_UID);
  }

  // Cuando alguien cancela no le escribimos todavia: el descuento solo se
  // puede usar en una suscripcion nueva, asi que no le sirve mientras siga
  // teniendo acceso. Lo dejamos apuntado y esperamos.
  if (tipo === "CANCELLATION") {
    const motivo = ev.cancellation_reason || "sin motivo";
    console.log("cancelacion de " + (ev.app_user_id || "?") + " (" + motivo +
      "): esperamos a que se le acabe el acceso");
    return respuestaOk("cancelacion anotada: " + motivo);
  }

  // Se le acabo el acceso. Si se fue ella misma, este es el momento de
  // escribirle: ya puede volver con el descuento. Si fue un fallo de cobro
  // o algo nuestro, no le mandamos nada.
  if (tipo === "EXPIRATION") {
    const motivo = ev.expiration_reason || "sin motivo";
    if (motivo !== "UNSUBSCRIBE") {
      console.log("fin de acceso de " + (ev.app_user_id || "?") + " ignorado: " + motivo);
      return respuestaOk("fin de acceso ignorado: " + motivo);
    }
    console.log("fin de acceso de " + (ev.app_user_id || "?") + ": lo dejamos en la cola");
    ctx.waitUntil(apuntarPendiente(ev, env));
    return respuestaOk("correo de vuelta en la cola");
  }

  // Solo la primera compra / inicio de prueba. Las renovaciones no mandan nada.
  if (tipo !== "INITIAL_PURCHASE") {
    console.log("evento sin correo: " + tipo);
    return respuestaOk("ignorado: " + tipo);
  }

  // Trabajo en segundo plano: contestamos 200 ya para que RevenueCat no
  // reintente, y mandamos el correo despues.
  // Si estaba en la cola del correo de vuelta, ya no hace falta: ha vuelto.
  ctx.waitUntil(quitarDeLaCola(ev.app_user_id || ev.original_app_user_id || "", env));
  ctx.waitUntil(enviarBienvenida(ev, env));
  return respuestaOk("encolado");
}

function respuestaOk(nota) {
  return new Response(JSON.stringify({ ok: true, nota }), {
    status: 200,
    headers: { "content-type": "application/json" },
  });
}

// Comparacion en tiempo constante, para no filtrar el secreto.
function iguales(a, b) {
  const ea = new TextEncoder().encode(a);
  const eb = new TextEncoder().encode(b);
  if (ea.length !== eb.length) return false;
  let d = 0;
  for (let i = 0; i < ea.length; i++) d |= ea[i] ^ eb[i];
  return d === 0;
}

// ---------------------------------------------------------------------------
//  Armar y mandar el correo
// ---------------------------------------------------------------------------

async function enviarBienvenida(ev, env, plantilla) {
  const cual = plantilla || "bienvenida";
  try {
    const uid = ev.app_user_id || ev.original_app_user_id || "";

    // 1. El correo. Mandamos siempre al correo con el que la persona entra
    //    en la app (Firebase), que es el que aparece en el correo como
    //    "tu membresia esta ligada a ...". Si por lo que sea no se puede
    //    consultar Firebase, usamos lo que venga de RevenueCat (solo llega
    //    en las compras por web).
    let correo = "";
    let nombre = "";

    if (uid) {
      const u = await buscarEnFirebase(uid, env);
      if (u) {
        correo = u.email || "";
        nombre = u.displayName || "";
      }
    }
    if (!correo) correo = atributo(ev, "$email");
    if (!nombre) nombre = atributo(ev, "$displayName");

    if (!correo) {
      console.log("sin correo para uid=" + uid + " store=" + (ev.store || "?"));
      return;
    }

    // 2. Fecha del primer cobro.
    const fecha = formatearFecha(ev.expiration_at_ms);

    // 3. Rellenar la plantilla.
    const primerNombre = (nombre || "").trim().split(/\s+/)[0] || "";
    let html = PLANTILLAS[cual] || PLANTILLAS.bienvenida;
    if (primerNombre) {
      html = html.split("{{NOMBRE}}").join(escapar(primerNombre));
    } else {
      // Sin nombre: "Hola, que alegria tenerte aqui."
      html = html.split("Hola {{NOMBRE}},").join("Hola,");
      html = html.split("{{NOMBRE}}").join("");
    }
    html = html.split("{{CORREO}}").join(escapar(correo));
    html = html.split("{{FECHA_COBRO}}").join(fecha);
    html = html.split("{{FECHA_FIN}}").join(fecha);

    // 4. Mandar con Resend.
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + env.RESEND_API_KEY,
        "content-type": "application/json",
      },
      body: JSON.stringify({
        from: REMITENTE,
        to: [correo],
        reply_to: RESPONDER_A,
        subject:
          (ASUNTOS[cual] || ASUNTOS.bienvenida) +
          // En las pruebas añadimos la hora para que Gmail no las agrupe en
          // una misma conversación y recorte el contenido repetido.
          (ev.store === "PRUEBA"
            ? " · prueba " + cual + " " + new Date().toISOString().slice(11, 19)
            : ""),
        html,
        tags: [{ name: "tipo", value: cual }],
      }),
    });

    if (!r.ok) {
      console.log("resend fallo " + r.status + " " + (await r.text()));
      return;
    }
    console.log(cual + " enviado a " + correo + " (" + (ev.store || "?") + ")");
  } catch (e) {
    console.log("error en enviarBienvenida: " + (e && e.message ? e.message : e));
  }
}

// La tarde del dia siguiente, hora de Miami, en el formato que entiende Resend.
function siguienteTarde() {
  const ahora = new Date();
  const desfase = desfaseMiami(ahora);
  const alla = new Date(ahora.getTime() + desfase);
  const objetivo = Date.UTC(
    alla.getUTCFullYear(), alla.getUTCMonth(), alla.getUTCDate() + 1, HORA_ENVIO, 0, 0
  );
  // El desfase puede cambiar entre hoy y manana (cambio de hora), asi que lo
  // recalculamos ya situados en la fecha de destino.
  const aprox = objetivo - desfase;
  const utc = objetivo - desfaseMiami(new Date(aprox));
  return new Date(utc).toISOString();
}

// Cuanto hay que sumarle a una fecha UTC para leerla como hora de Miami.
function desfaseMiami(fecha) {
  const f = new Intl.DateTimeFormat("en-US", {
    timeZone: "America/New_York", hour12: false,
    year: "numeric", month: "2-digit", day: "2-digit",
    hour: "2-digit", minute: "2-digit", second: "2-digit",
  });
  const p = {};
  for (const parte of f.formatToParts(fecha)) p[parte.type] = parte.value;
  const comoSiFueraUTC = Date.UTC(
    +p.year, +p.month - 1, +p.day, +p.hour % 24, +p.minute, +p.second
  );
  return comoSiFueraUTC - fecha.getTime();
}

// --------------------------------------------------------------------------
//  La cola del correo de vuelta
//
//  No mandamos el correo en el momento en que alguien pierde el acceso: lo
//  apuntamos aqui y lo manda la tarea de las 16:00 de Miami del dia siguiente.
//  Asi le damos un dia por si se vuelve a suscribir sola; si lo hace, la
//  quitamos de la cola y no le llega nada.
// --------------------------------------------------------------------------

async function apuntarPendiente(ev, env) {
  try {
    const uid = ev.app_user_id || ev.original_app_user_id || "";
    if (!uid || !env.PENDIENTES) return;
    const cuando = siguienteTarde();
    await env.PENDIENTES.put(
      "pendiente:" + uid,
      JSON.stringify({ uid, desde: Date.now(), cuando, store: ev.store || "" }),
      { expirationTtl: 60 * 60 * 24 * 14 }
    );
    console.log("en la cola: " + uid + ", le toca el " + new Date(cuando).toISOString());
  } catch (e) {
    console.log("error apuntando en la cola: " + (e && e.message ? e.message : e));
  }
}

async function quitarDeLaCola(uid, env) {
  try {
    if (!uid || !env.PENDIENTES) return;
    const clave = "pendiente:" + uid;
    if (!(await env.PENDIENTES.get(clave))) return;
    await env.PENDIENTES.delete(clave);
    console.log("fuera de la cola: " + uid + " se ha vuelto a suscribir");
  } catch (e) {
    console.log("error quitando de la cola: " + (e && e.message ? e.message : e));
  }
}

// Recorre la cola y manda lo que ya toca. La llama el reloj de Cloudflare.
async function revisarCola(env, forzar) {
  if (!env.PENDIENTES) return 0;
  const ahora = Date.now();
  let mandados = 0;
  let cursor;
  do {
    const lista = await env.PENDIENTES.list({ prefix: "pendiente:", cursor });
    cursor = lista.list_complete ? null : lista.cursor;
    for (const clave of lista.keys) {
      const crudo = await env.PENDIENTES.get(clave.name);
      if (!crudo) continue;
      let dato = {};
      try { dato = JSON.parse(crudo) || {}; } catch (_) {}
      const toca = dato.cuando ? Date.parse(dato.cuando) : 0;
      if (!forzar && toca && ahora < toca) continue;
      await env.PENDIENTES.delete(clave.name);
      await enviarBienvenida(
        { type: "EXPIRATION", app_user_id: dato.uid, store: dato.store || "" },
        env,
        "cancelacion"
      );
      mandados++;
    }
  } while (cursor);
  if (mandados) console.log("correos de vuelta mandados: " + mandados);
  return mandados;
}

function atributo(ev, clave) {
  const a = ev.subscriber_attributes || {};
  const v = a[clave];
  if (!v) return "";
  return (typeof v === "object" ? v.value : v) || "";
}

function escapar(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

const MESES = [
  "enero", "febrero", "marzo", "abril", "mayo", "junio",
  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
];

function formatearFecha(ms) {
  let d;
  if (ms && Number(ms) > 0) {
    d = new Date(Number(ms));
  } else {
    d = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000);
  }
  return d.getUTCDate() + " de " + MESES[d.getUTCMonth()];
}

// ---------------------------------------------------------------------------
//  Campanas (Broadcasts) de Resend
// ---------------------------------------------------------------------------

const CAMPANAS = [
  {
    clave: "lanzamiento",
    nombre: "Lanzamiento - lista de espera (precio de fundadora)",
    segmento: "dcba5589-6dce-4750-8840-44ca164875c5",
    asunto: "BuildUp ya está aquí (y tú entras con precio de fundadora)",
  },
  {
    clave: "general",
    nombre: "Lanzamiento - resto de Shopify (precio normal)",
    segmento: "e86ac9fd-2a43-415c-bcbf-e30342fc3e0d",
    asunto: "BuildUp ya está aquí \u2661",
  },
  {
    clave: "primeras",
    nombre: "Gracias - las que ya estaban suscritas",
    segmento: "0a6a3666-d6ba-4d44-9524-31b8d1e7114b",
    asunto: "Tú ya estabas aquí \u2661",
  },
];

async function crearCampanas(env) {
  const salida = [];
  for (const c of CAMPANAS) {
    const html = (PLANTILLAS.envio || {})[c.clave];
    if (!html) {
      salida.push({ campana: c.clave, error: "sin plantilla de envio" });
      continue;
    }
    const r = await fetch("https://api.resend.com/broadcasts", {
      method: "POST",
      headers: {
        // Crear campanas necesita una clave con permiso completo. La clave de
        // siempre solo puede enviar, y asi se queda: es la que usa el correo
        // automatico todos los dias.
        Authorization: "Bearer " + (env.RESEND_ADMIN_KEY || env.RESEND_API_KEY),
        "content-type": "application/json",
      },
      body: JSON.stringify({
        segment_id: c.segmento,
        name: c.nombre,
        from: REMITENTE,
        reply_to: RESPONDER_A,
        subject: c.asunto,
        html,
      }),
    });
    const texto = await r.text();
    salida.push({ campana: c.clave, estado: r.status, respuesta: texto.slice(0, 300) });
  }
  return { ok: true, campanas: salida };
}

// ---------------------------------------------------------------------------
//  Contrasena nueva
//
//  Firebase tiene bloqueada la edicion de sus plantillas en este proyecto, asi
//  que el correo lo mandamos nosotros: le pedimos a Firebase el enlace (sin
//  que lo mande el), lo apuntamos a nuestra pagina /clave/ y enviamos el
//  correo de BuildUp con Resend.
// ---------------------------------------------------------------------------

async function manejarClave(request, env, ctx) {
  if (request.method !== "POST") {
    return new Response("Method not allowed", { status: 405 });
  }
  let correo = "";
  try {
    const cuerpo = await request.json();
    correo = String((cuerpo && cuerpo.correo) || "").trim().toLowerCase();
  } catch (_) {}

  // Contestamos siempre lo mismo, exista la cuenta o no: asi nadie puede usar
  // esto para averiguar quien esta registrada.
  if (/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(correo)) {
    ctx.waitUntil(enviarClave(correo, env));
  }
  return respuestaOk("recibido");
}

async function enviarClave(correo, env) {
  try {
    const sa = leerCuentaServicio(env);
    if (!sa) return;
    const token = await tokenDeAcceso(sa);
    if (!token) return;

    const r = await fetch(
      "https://identitytoolkit.googleapis.com/v1/projects/" +
        encodeURIComponent(sa.project_id) + "/accounts:sendOobCode",
      {
        method: "POST",
        headers: {
          Authorization: "Bearer " + token,
          "content-type": "application/json",
        },
        body: JSON.stringify({
          requestType: "PASSWORD_RESET",
          email: correo,
          returnOobLink: true,
        }),
      }
    );

    if (!r.ok) {
      // EMAIL_NOT_FOUND es lo normal cuando alguien escribe mal su correo.
      console.log("oobCode fallo " + r.status + " " + (await r.text()));
      return;
    }

    const j = await r.json();
    let codigo = "";
    try { codigo = new URL(j.oobLink || "").searchParams.get("oobCode") || ""; } catch (_) {}
    if (!codigo) { console.log("sin oobCode en la respuesta"); return; }

    const enlace = "https://getbuildup.app/clave/?c=" + encodeURIComponent(codigo);

    let html = PLANTILLAS.clave || "";
    html = html.split("{{ENLACE}}").join(enlace);
    html = html.split("{{CORREO}}").join(escapar(correo));

    const envio = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: "Bearer " + env.RESEND_API_KEY,
        "content-type": "application/json",
      },
      body: JSON.stringify({
        from: REMITENTE,
        to: [correo],
        reply_to: RESPONDER_A,
        subject: ASUNTOS.clave,
        html,
        tags: [{ name: "tipo", value: "clave" }],
      }),
    });

    if (!envio.ok) console.log("resend fallo " + envio.status + " " + (await envio.text()));
    else console.log("correo de contrasena enviado a " + correo);
  } catch (e) {
    console.log("error en enviarClave: " + (e && e.message ? e.message : e));
  }
}

// ---------------------------------------------------------------------------
//  Firebase: UID -> correo y nombre
// ---------------------------------------------------------------------------

let tokenCache = { valor: null, expira: 0 };

async function buscarEnFirebase(uid, env) {
  const sa = leerCuentaServicio(env);
  if (!sa) return null;

  const token = await tokenDeAcceso(sa);
  if (!token) return null;

  const r = await fetch(
    "https://identitytoolkit.googleapis.com/v1/projects/" +
      encodeURIComponent(sa.project_id) +
      "/accounts:lookup",
    {
      method: "POST",
      headers: {
        Authorization: "Bearer " + token,
        "content-type": "application/json",
      },
      body: JSON.stringify({ localId: [uid] }),
    }
  );

  if (!r.ok) {
    console.log("firebase lookup fallo " + r.status + " " + (await r.text()));
    return null;
  }

  const j = await r.json();
  const u = j.users && j.users[0];
  if (!u) return null;

  let correo = u.email || "";
  let nombre = u.displayName || "";

  // Si entro con Apple/Google, a veces el correo solo esta en providerUserInfo.
  if (!correo && Array.isArray(u.providerUserInfo)) {
    for (const p of u.providerUserInfo) {
      if (p.email) { correo = p.email; break; }
    }
  }
  if (!nombre && Array.isArray(u.providerUserInfo)) {
    for (const p of u.providerUserInfo) {
      if (p.displayName) { nombre = p.displayName; break; }
    }
  }

  return { email: correo, displayName: nombre };
}

function leerCuentaServicio(env) {
  try {
    const raw = env.FIREBASE_SA;
    if (!raw) return null;
    return typeof raw === "string" ? JSON.parse(raw) : raw;
  } catch (e) {
    console.log("FIREBASE_SA no es un JSON valido");
    return null;
  }
}

async function tokenDeAcceso(sa) {
  const ahora = Math.floor(Date.now() / 1000);
  if (tokenCache.valor && tokenCache.expira > ahora + 60) {
    return tokenCache.valor;
  }

  const cabecera = { alg: "RS256", typ: "JWT" };
  const reclamos = {
    iss: sa.client_email,
    scope: "https://www.googleapis.com/auth/identitytoolkit",
    aud: "https://oauth2.googleapis.com/token",
    iat: ahora,
    exp: ahora + 3600,
  };

  const sinFirma =
    b64url(JSON.stringify(cabecera)) + "." + b64url(JSON.stringify(reclamos));

  const clave = await importarClave(sa.private_key);
  if (!clave) return null;

  const firma = await crypto.subtle.sign(
    "RSASSA-PKCS1-v1_5",
    clave,
    new TextEncoder().encode(sinFirma)
  );
  const jwt = sinFirma + "." + b64urlBytes(new Uint8Array(firma));

  const r = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body:
      "grant_type=urn%3Aietf%3Aparams%3Aoauth%3Agrant-type%3Ajwt-bearer&assertion=" +
      encodeURIComponent(jwt),
  });

  if (!r.ok) {
    console.log("google token fallo " + r.status + " " + (await r.text()));
    return null;
  }

  const j = await r.json();
  tokenCache = {
    valor: j.access_token,
    expira: ahora + (j.expires_in || 3600),
  };
  return j.access_token;
}

async function importarClave(pem) {
  try {
    const limpio = String(pem)
      .replace(/\\n/g, "\n")
      .replace(/-----BEGIN PRIVATE KEY-----/, "")
      .replace(/-----END PRIVATE KEY-----/, "")
      .replace(/\s+/g, "");
    const bin = atob(limpio);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return await crypto.subtle.importKey(
      "pkcs8",
      bytes.buffer,
      { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" },
      false,
      ["sign"]
    );
  } catch (e) {
    console.log("no se pudo leer private_key: " + (e && e.message));
    return null;
  }
}

function b64url(texto) {
  return b64urlBytes(new TextEncoder().encode(texto));
}

function b64urlBytes(bytes) {
  let s = "";
  for (let i = 0; i < bytes.length; i++) s += String.fromCharCode(bytes[i]);
  return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}
