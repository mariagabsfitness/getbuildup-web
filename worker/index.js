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
const ASUNTOS = {
  bienvenida: "Ya estás dentro de BuildUp \u2661",
  lanzamiento: "BuildUp ya está aquí \u2661",
  general: "BuildUp ya está aquí \u2661",
  primeras: "Tú ya estabas aquí \u2661",
  cancelacion: "¿Me cuentas qué pasó?",
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === "/api/rc-webhook") {
      return manejarWebhook(request, env, ctx);
    }

    // Cualquier otra cosa: el sitio estatico de siempre.
    return env.ASSETS.fetch(request);
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

  // Cancelacion voluntaria: le escribimos para saber por que se va.
  // Solo cuando la persona lo cancela ella misma. Si fue un fallo de cobro,
  // una devolucion o algo nuestro, no le mandamos nada.
  if (tipo === "CANCELLATION") {
    const motivo = ev.cancellation_reason || "";
    if (motivo !== "UNSUBSCRIBE") {
      return respuestaOk("cancelacion ignorada: " + (motivo || "sin motivo"));
    }
    ctx.waitUntil(enviarBienvenida(ev, env, "cancelacion"));
    return respuestaOk("correo de cancelacion encolado");
  }

  // Solo la primera compra / inicio de prueba. Las renovaciones no mandan nada.
  if (tipo !== "INITIAL_PURCHASE") {
    return respuestaOk("ignorado: " + tipo);
  }

  // Trabajo en segundo plano: contestamos 200 ya para que RevenueCat no
  // reintente, y mandamos el correo despues.
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
    } else {
      console.log(cual + " enviado a " + correo + " (" + (ev.store || "?") + ")");
    }
  } catch (e) {
    console.log("error en enviarBienvenida: " + (e && e.message ? e.message : e));
  }
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
