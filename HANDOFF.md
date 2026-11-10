# BuildUp — estado del proyecto

Última actualización: **10 de noviembre de 2026**

Documento de traspaso. Si esta conversación se pierde o empieza una nueva,
todo lo necesario para seguir está aquí.

---

## 1. Qué es y dónde vive cada cosa

| Pieza | Dónde | Notas |
|---|---|---|
| Web pública | **getbuildup.app** | Cloudflare Workers |
| Código | `~/Desktop/getbuildup-web` → GitHub `mariagabsfitness/getbuildup-web` | Se despliega solo al hacer push a `main` (~90 s) |
| App móvil | App Store + Google Play | |
| Cuentas de usuarias | **Firebase** (proyecto `buildup-40951`) | Authentication + Firestore |
| Cobros | **RevenueCat** (proyecto `e3689e01`) + **Paddle** (web) | |
| Correos | **Resend** (dominio `getbuildup.app`) | |
| DNS | **Cloudflare**, cuenta `info@mariagabsfitness.com` | |
| Tienda antigua | Shopify `57f695` (mariagabsfitness.com) | Solo como origen de la lista de clientas |

---

## 2. La web

### Cómo se construye

No se edita `dist/` a mano. El flujo es:

1. `_mockup.html` → es la **fuente de la verdad** del CSS y el JS
2. `python3 extract.py` → saca `assets/styles.css` y `assets/app.js`
3. `python3 build.py` → genera todo `dist/` (borra y reconstruye)
4. `git push` → Cloudflare despliega solo

`content.py` tiene los textos, precios y configuración.

### Datos clave en `content.py`

- `PAGO["rc_api_key"]` = clave **de producción** de RevenueCat Web Billing
- `PAGO["activo"] = True` → el cobro está encendido
- `PAGO["descuentos"]` = `{"mensual": "BUILD", "anual": "BUILDANUAL"}`
- `PAGO["descuentos_vuelve"]` = `{"mensual": "VUELVE"}`

### El descuento de fundadora

- Códigos creados en **Paddle**: `BUILD` (25 % los 3 primeros meses) y
  `BUILDANUAL` (25 % el primer año)
- Se aplican **solos** si la persona entra por `getbuildup.app/crear-cuenta/?fundadora=1`
- Se guarda en `sessionStorage` 6 horas, por si navega y vuelve
- Solo funciona **desde la web**. Dentro de la app (App Store / Google Play)
  no se puede aplicar

### El descuento de vuelta

- Código creado en **Paddle**: `VUELVE` (50 % los 3 primeros meses, solo plan
  mensual, sin fecha de caducidad)
- Se aplica **solo** si la persona entra por `getbuildup.app/crear-cuenta/?vuelve=1`,
  que es el enlace del correo de cancelación
- Mismo mecanismo que el de fundadora: se guarda en `sessionStorage` 6 horas
- Si el código fallara, el pago se reintenta solo sin descuento, para que nadie
  se quede sin poder pagar

### Precios

| | Normal | Fundadora |
|---|---|---|
| Mensual | $24.99 | $18.74 los 3 primeros meses |
| Anual | $179.99 | $134.99 el primer año |

Todas empiezan con **7 días gratis**.

---

## 3. El Worker (`worker/index.js`)

Un solo Worker hace dos cosas: sirve la web y recibe el webhook de RevenueCat.

### Correos automáticos

```
Alguien se suscribe (web, App Store o Google Play)
  → RevenueCat manda INITIAL_PURCHASE a getbuildup.app/api/rc-webhook
  → el Worker busca el correo y el nombre en Firebase por el UID
  → Resend envía el correo de bienvenida
```

Funciona para las tres tiendas. El correo **siempre** se manda a la dirección
con la que la persona entra en la app (Firebase), no a la que escribió al pagar.

El mismo Worker escucha `CANCELLATION`. Si el motivo es `UNSUBSCRIBE` (la
persona canceló ella misma, no un fallo de cobro) manda el correo de
cancelación con la oferta del 50 %. Cualquier otro motivo se ignora.

### Correo de contraseña nueva

Firebase tiene **bloqueada la edición de sus plantillas** en este proyecto
("Email template updates are currently unavailable for this project"), así que
ese correo lo mandamos nosotros:

```
Alguien pulsa "Olvidé mi contraseña" en /login/
  → la web llama a getbuildup.app/api/clave
  → el Worker le pide a Firebase el enlace (returnOobLink, sin que lo mande él)
  → lo convierte en getbuildup.app/clave/?c=CODIGO
  → Resend envía el correo de BuildUp en español
  → la persona elige su contraseña en /clave/ y entra
```

`/api/clave` contesta siempre lo mismo exista la cuenta o no, para que nadie
pueda usarlo para averiguar quién está registrada.

En Firebase quedó configurado el SMTP de Resend (`smtp.resend.com`, puerto 587,
usuario `resend`, remitente `hola@getbuildup.app`). Eso afecta a los demás
correos de Firebase, que siguen en inglés porque no se pueden editar.

### Secretos (en Cloudflare, nunca en el repositorio)

| Nombre | Qué es |
|---|---|
| `RESEND_API_KEY` | Clave de Resend, permiso **solo enviar** |
| `RC_WEBHOOK_SECRET` | Frase secreta compartida con RevenueCat |
| `FIREBASE_SA` | JSON de la cuenta de servicio de Firebase |
| `RESEND_ADMIN_KEY` | Sobra: apunta a una clave ya borrada |

Variables normales: `TEST_UID`, `TEST_PLANTILLA`.

### Mecanismo de pruebas

En RevenueCat → Integrations → Webhooks → *Correo de bienvenida* → **Send Test Event**.
El Worker, al recibir un evento `TEST`, manda la plantilla que diga
`TEST_PLANTILLA` (`bienvenida`, `lanzamiento`, `general`, `primeras`,
`cancelacion`) al usuario
de `TEST_UID`. Los asuntos de prueba llevan la hora para que Gmail no los agrupe.

⚠️ `TEST_PLANTILLA = "crear-campanas"` **crea las tres campañas en Resend**.
Dejarlo siempre en `bienvenida`.

---

## 4. Los correos

Viven en `correos/`. `build.py` genera dos cosas a partir de ellos:

- `worker/plantillas.js` → lo que usa el Worker
- `correos/envio/*.html` → copias con el enlace de baja real de Resend,
  que son las que se suben a las campañas

| Archivo | Para quién |
|---|---|
| `correo-bienvenida.html` | Automático, al suscribirse |
| `correo-lanzamiento.html` | Lista de espera, con precio de fundadora |
| `correo-lanzamiento-general.html` | Resto de Shopify, precios normales |
| `correo-primeras.html` | Las que ya estaban suscritas antes del lanzamiento |
| `correo-cancelacion.html` | Automático, al cancelar. Oferta: 50 % los 3 primeros meses |
| `correo-clave.html` | Automático, al pedir una contraseña nueva |

Remitente: **BuildUp by MariaGabsFitness `<hola@getbuildup.app>`**
Responder a: `buildup@mariagabsfitness.com`

---

## 5. Resend

- Dominio `getbuildup.app` **verificado** (DKIM + SPF)
- Seguimiento de clics y aperturas: subdominio **`links.getbuildup.app`**, verificado
- Planes: **Transactional $20/mes** (50.000 correos) + **Marketing $40/mes** (5.000 contactos) = **$60/mes**
- DMARC ya estaba en `p=reject`

### Grupos (máximo 3 en este plan)

| Grupo | Contactos |
|---|---|
| Lista de espera | 150 |
| Resto Shopify | 907 |
| Gracias ya suscritas | 16 |

`info@mariagabsfitness.com` y `edgardobertim@hotmail.com` están en los tres,
para recibir todo lo que se envíe.

### Campañas

| Campaña | Estado | Resultado |
|---|---|---|
| Gracias | Enviada 8 nov | 14/14 entregados · 0 rebotes · 0 bajas |
| Lanzamiento lista de espera | Enviada 8 nov 11:00 | 148/148 · 0 rebotes · 1 baja |
| Lanzamiento resto de Shopify | **Programada 10 nov 11:00** | 907 contactos |

---

## 6. Cosas aprendidas (para no repetir errores)

1. **El editor de Resend destroza el HTML.** Si subes el correo por el panel,
   reescribe las tablas y descoloca las fotos. Las campañas se crean **por API**
   (desde el Worker) para que el HTML viaje intacto.
2. **Los contadores de Resend van retrasados.** El número de contactos de un
   grupo puede tardar media hora en actualizarse. El dato bueno es el que sale
   al filtrar los contactos por grupo.
3. **Al reprogramar una campaña se borra la hora.** Hay que volver a ponerla.
4. **Gmail agrupa correos con el mismo asunto** y esconde las partes repetidas
   detrás de "···". En pruebas, usar asuntos distintos.
5. **Imágenes con ancho fijo rompen el móvil.** Todas deben ir con
   `width:100%; max-width:XXXpx`. Un solo `width:330px` hacía que el correo
   entero midiera 418 px y Gmail lo mostrara descuadrado.
6. **`border-radius` no funciona en un `<td>`** con `border-collapse:collapse`.
   Va en un elemento interior.
7. **El plan de $20 de Resend no incluye contactos de marketing**, van aparte.
8. **Las listas de correos no van al repositorio** (`listas/` está en `.gitignore`).

---

## 7. Números a 9 de noviembre

- **53 suscripciones activas** (49 en prueba, 4 pagando). Antes del lanzamiento eran 20.
- Web: **118 visitas** y **231 páginas vistas** en 24 h
- Correos: **162 enviados, 0 rebotes, 1 baja**

---

## 8. Pendiente

- [ ] **Que la app use también nuestro correo de contraseña.** En FlutterFlow,
      cambiar la acción *Send Password Reset Email* por una llamada a
      `POST https://getbuildup.app/api/clave` con `{"correo": "..."}`.
      Hasta entonces, desde la app sigue llegando el correo de Firebase en inglés.
- [ ] Corregir el correo de la clienta gloredor@gmail.com en Paddle
      (está guardado como gloredoe@gmail.com y no recibe sus facturas)
- [ ] **Verificación en dos pasos en Cloudflare** — esa cuenta controla el dominio
- [ ] Bajar el plan de marketing de Resend cuando ya no haga falta
      (ojo: el gratis son 1.000 contactos y ahora hay ~1.070)
- [ ] Correo de retención para quien creó cuenta pero no empezó la prueba
      (hace falta una tarea diaria que compare Firebase con RevenueCat)
- [ ] El onboarding de la app no se ve si la cuenta se crea desde la web.
      Debería dispararse con un campo `onboardingCompleto` en Firestore,
      no al registrarse
- [ ] Quitar `RESEND_ADMIN_KEY` de Cloudflare (apunta a una clave borrada)
- [ ] Borrar los archivos de vista previa en `assets/vista/`
- [ ] Quitar el `snippets/page.buildup.liquid` huérfano de Shopify
- [ ] Convertir mariagabsfitness.com en página de marca personal
- [ ] Más adelante: registrar la marca BuildUp (abre la puerta al logo en el
      correo vía BIMI, que hoy pide marca registrada o un año de uso)

---

## 9. Normas de trabajo

- Las claves y contraseñas **las introduce siempre María Gabriela**, nunca Claude.
- Nada se envía a nadie sin que ella lo confirme antes.
- Solo se escribe a quien ha dado permiso de marketing: de los 1.362 clientes de
  Shopify, **307 no lo dieron** y quedan fuera de todo envío.
