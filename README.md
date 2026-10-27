# getbuildup.app — sitio web de BuildUp

Sitio estático. Se publica solo en Cloudflare Pages cada vez que se sube un cambio a GitHub.

## Cómo cambiar textos, precios o datos

Todo el contenido editable está en **`content.py`**: precios, los 6 programas, las 42 recetas,
los testimonios, las preguntas frecuentes y los enlaces legales.

Después de editar, hay que regenerar el sitio:

    python3 build.py

Eso reescribe la carpeta `dist/`, que es lo que se publica.

## Estructura

    content.py       Todo el contenido editable (lo que normalmente se toca)
    build.py         Genera dist/ a partir de content.py — las plantillas de cada página
    extract.py       Saca el CSS y el JS desde _mockup.html hacia assets/
    _mockup.html     El mockup original, fuente de los estilos
    assets/          styles.css y app.js (generados por extract.py)
    dist/            El sitio ya generado. Esto es lo que publica Cloudflare

## Páginas

    /                        Home
    /membresia/              Membresía y planes
    /programas/              Índice de programas + preguntas frecuentes
    /programa/<slug>/        Una por programa (6)
    /nutricion/              SmartFuel
    /comunidad/              BuildFam
    /crear-cuenta/           Alta con 7 días gratis
    /listo/                  Confirmación tras el alta
    /login/                  Iniciar sesión

## Pendiente de conectar

- Las fotos y videos son marcadores de posición, con etiqueta de qué va en cada uno.
- El alta todavía no crea la cuenta: falta conectar Firebase Auth y RevenueCat Web Billing.
- Los enlaces de App Store y Google Play en /listo/ están vacíos.
