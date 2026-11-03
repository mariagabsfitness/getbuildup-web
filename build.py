# -*- coding: utf-8 -*-
"""Genera el sitio estatico de BuildUp en dist/.
   Uso:  python3 build.py        (y luego abre dist/index.html o usa serve.sh)"""
import io, json, os, re, shutil, html
import content as C

OUT = "dist"
S, P = C.SITE, C.PRECIOS

def esc(x): return html.escape(str(x), quote=True)

IMG_DIR = os.path.join("assets", "img")
EXTS = (".webp", ".png", ".jpg", ".jpeg")
VID_EXTS = (".mp4", ".webm", ".mov")

def slug(t):
    t = t.lower()
    for a, b in zip("áéíóúñü", "aeiounu"): t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")

def _find(base):
    """Devuelve el nombre de archivo si existe assets/img/<base>.<ext>."""
    for e in EXTS:
        if os.path.isfile(os.path.join(IMG_DIR, base + e)):
            return base + e
    return None

def _findv(base):
    """Devuelve el video si existe assets/img/<base>.mp4 (o .webm / .mov)."""
    for e in VID_EXTS:
        if os.path.isfile(os.path.join(IMG_DIR, base + e)):
            return base + e
    return None

def has_video(slot):
    return _findv(slot) is not None

def media(label, dark=False, slot=None, foco=None):
    """Si hay una foto en assets/img/<slot>.jpg la usa; si no, deja el marcador.
       Si ademas existe <slot>-movil.jpg, la usa en pantallas de telefono."""
    if slot:
        vid = _findv(slot)
        if vid:
            poster = _find(slot)
            pa = (' poster="/assets/img/%s"' % poster) if poster else ""
            sty = (' style="object-position:%s"' % foco) if foco else ""
            mobv = _findv(slot + "-movil")
            mob = ('<source src="/assets/img/%s" media="(max-width:767px)">' % mobv) if mobv else ""
            return ('<video class="media" autoplay muted loop playsinline preload="metadata"'
                    '%s aria-label="%s"%s>%s<source src="/assets/img/%s"></video>'
                    % (pa, esc(label), sty, mob, vid))
        desk = _find(slot)
        if desk:
            mob = _find(slot + "-movil")
            src = ('<source media="(max-width:767px)" srcset="/assets/img/%s">' % mob) if mob else ""
            sty = (' style="object-position:%s"' % foco) if foco else ""
            return ('<picture class="media"%s>%s<img src="/assets/img/%s" alt="%s" loading="lazy"%s></picture>'
                    % (" " if False else "", src, desk, esc(label), sty))
    return '<div class="media%s"><span class="tag">%s</span></div>' % (" dark" if dark else "", esc(label))

SCREENS = {
 "hoy": '<div class="sbar"></div><div class="scard"><div class="srow" style="width:60%"></div><div class="srow" style="width:80%"></div><div class="srow" style="width:45%"></div></div><div class="scard fill" style="flex:1.4"></div>',
 "entreno": '<div class="sbar" style="width:52%"></div><div class="scard fill" style="flex:2"></div><div class="scard"><div class="srow" style="width:70%"></div><div class="srow" style="width:40%"></div></div>',
 "nutri": '<div class="sbar" style="width:44%"></div><div class="scard"><div class="srow" style="width:88%"></div><div class="srow" style="width:60%"></div><div class="srow" style="width:74%"></div></div><div class="scard fill"></div><div class="scard"><div class="srow" style="width:52%"></div></div>',
 "perfil": '<div class="sbar" style="width:36%"></div><div class="scard fill" style="flex:1.2"></div><div class="scard"><div class="srow" style="width:66%"></div><div class="srow" style="width:82%"></div><div class="srow" style="width:48%"></div></div>',
 "chat": '<div class="chat"><div class="bub them"><i>María Gabriela · Coach</i>¡Buenos días, BuildFam! Hoy toca pierna. ¿Quién ya entrenó?</div><div class="bub me"><i>Andrea</i>¡Lista! Subí 5 kg en hip thrust</div><div class="bub them"><i>Valeria</i>Duda: ¿puedo cambiar el día 3 por el 4?</div><div class="bub them"><i>María Gabriela · Coach</i>¡Claro! Usa ORDENAR en tu programa y acomoda tu semana como te funcione.</div></div>',
 "chat2": '<div class="chat"><div class="bub me"><i>Tú</i>Terminé la semana 4 de Build &amp; Shred</div><div class="bub them"><i>Cami</i>¡Vamos! Yo voy por la 6 y ya subí peso en sentadilla</div><div class="bub them"><i>María Gabriela · Coach</i>Qué orgullo, BuildFam. Recuerden registrar sus pesos</div></div>',
 "chat3": '<div class="chat"><div class="bub them"><i>Valeria</i>¿Alguna hace la versión en casa?</div><div class="bub me"><i>Andrea</i>Yo sí, te cuento cómo la adapto</div><div class="bub them"><i>María Gabriela · Coach</i>En cada ejercicio tienen alternativas, úsenlas sin miedo</div></div>',
}
def phone(kind): return '<div class="phone"><div class="screen">%s</div></div>' % SCREENS.get(kind, SCREENS["hoy"])

NAV = [("/membresia/","Membresía","membresia"), ("/programas/","Programas","programas"),
       ("/nutricion/","Nutrición","nutricion"), ("/comunidad/","BuildFam","comunidad"),
       ("/login/","Iniciar sesión","login")]

def header(active=""):
    links = "".join('<a href="%s"%s>%s</a>' % (u, ' class="on"' if k==active else "", t) for u,t,k in NAV)
    return """<div class="notebar">Empieza con <b>%d días gratis</b> · acceso completo a BuildUp · cancela cuando quieras</div>
<header class="hdr"><div class="hdr-in">
  <a href="/" class="logo"><b>Build</b><span>Up</span></a>
  <nav class="nav" id="nav">%s</nav>
  <div class="hdr-cta">
    <button class="burger" id="burger" aria-label="Menú"><span></span></button>
    <a href="/crear-cuenta/" class="btn">Únete</a>
  </div>
</div></header>""" % (P["prueba_dias"], links)

def footer():
    li = lambda arr: "".join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (C.legal_url(u), t) for t,u in arr)
    return """<footer class="ftr"><div class="wrap">
  <div class="ftr-grid">
    <div><h4>Contacto</h4><ul>
      <li>%s</li>
      <li><a href="mailto:%s">%s</a></li>
      <li style="color:var(--muted)">Consultas generales</li>
      <li style="margin-top:12px"><a href="mailto:%s">%s</a></li>
      <li style="color:var(--muted)">Reportar un problema con la app</li>
      <li style="margin-top:16px;color:var(--muted)">Entrenamiento creado por %s</li>
      <li style="color:var(--muted)">%s</li>
    </ul></div>
    <div><h4>La app</h4><ul>
      <li><a href="/programas/">Programas</a></li>
      <li><a href="/nutricion/">Nutrición</a></li>
      <li><a href="/comunidad/">BuildFam</a></li>
      <li><a href="/membresia/">Membresía</a></li>
      <li><a href="/programas/#faq">Preguntas frecuentes</a></li>
    </ul></div>
    <div><h4>Legal</h4><ul>%s</ul></div>
    <div><h4>Legal · EN</h4><ul>%s</ul></div>
  </div>
  <div class="gdpr">
    <a class="gdprbadge" href="%s" target="_blank" rel="noopener">
      <span class="shield">&#9094;</span>
      <span class="txt"><b>EU GDPR</b><i>Representative</i><em>Certified · %s</em></span>
      <span class="chev">&rsaquo;</span>
    </a>
    <p class="gdprby">powered by <a href="https://prighter.com" target="_blank" rel="noopener">Prighter</a></p>
  </div>
  <div class="ftr-bot">
    <div class="social"><a href="%s" aria-label="Instagram">IG</a><a href="%s" aria-label="TikTok">TT</a></div>
    <div>© 2026 — %s</div>
  </div>
</div></footer>""" % (S["horario"], S["email_general"], S["email_general"], S["email_soporte"], S["email_soporte"],
                      S["coach"], S["empresa"], li(C.LEGAL_ES), li(C.LEGAL_EN),
                      S["prighter_portal"], S["prighter_fecha"], S["instagram"], S["tiktok"], S["empresa"])

def doc(path, title, desc, body, active=""):
    canon = S["dominio"] + path
    return """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="BuildUp">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:locale" content="es_ES">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#000000">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/styles.css">
</head>
<body>
%s
<main>
%s
</main>
%s
<script src="/assets/app.js" defer></script>
</body>
</html>
""" % (esc(title), esc(desc), canon, esc(title), esc(desc), canon, header(active), body, footer())

# ---------------------------------------------------------------- componentes
def plan_block():
    a, m = P["anual"], P["mensual"]
    return """<div>
  <h2 class="h-section" style="text-align:left;letter-spacing:.1em">Elige tu membresía</h2>
  <p style="color:var(--grey);margin:18px 0 6px;max-width:52ch">Empieza con <b>%d días gratis</b> y desbloquea BuildUp completa: programas, progreso, nutrición y comunidad.</p>
  <p style="color:var(--grey);margin:0 0 8px;max-width:52ch">Entrenamiento, nutrición, progreso y comunidad en un solo lugar por menos de $1 al día.</p>
  <div class="plan sel" data-plan="anual" data-price="%s al año" role="button" tabindex="0">
    <span class="ribbon">%s</span>
    <div><div class="mini">★ Oferta exclusiva</div><div class="nm">Membresía anual</div>
      <div class="pr">%s %s</div>
      <div class="rn">Equivale a %s al mes · %s</div><span class="trial">%d días gratis</span></div>
    <span class="dot"></span>
  </div>
  <div class="plan" data-plan="mensual" data-price="%s al mes" role="button" tabindex="0">
    <div><div class="mini">Cancela cuando quieras</div><div class="nm">Membresía mensual</div>
      <div class="pr">%s %s</div><div class="rn">%s</div><span class="trial">%d días gratis</span></div>
    <span class="dot"></span>
  </div>
  <div style="margin-top:26px"><a href="/crear-cuenta/" class="btn wide">Empieza %d días gratis</a></div>
</div>""" % (P["prueba_dias"], a["importe"], a["cinta"], a["importe"], a["periodo"], a["mensualizado"],
             a["renovacion"], P["prueba_dias"], m["importe"], m["importe"], m["periodo"], m["renovacion"],
             P["prueba_dias"], P["prueba_dias"])

def member_band(wash=True):
    return """<section class="section%s"><div class="wrap member">
  <div class="shot">%s</div>
  %s
</div></section>""" % (" wash" if wash else "",
                       media("María Gabriela, entrenadora de BuildUp", False, "retrato"),
                       plan_block())

def comparator():
    def side(cls, slot, lbl, lblcls):
        if _find(slot):
            return ('<div class="side %s img">%s<span class="lbl %s">%s</span></div>'
                    % (cls, media(lbl, False, slot), lblcls, lbl))
        return '<div class="side %s"><span class="lbl %s">%s</span></div>' % (cls, lblcls, lbl)
    return """<div class="compare" data-compare tabindex="0" role="slider" aria-label="Comparador antes y después" aria-valuemin="0" aria-valuemax="100" aria-valuenow="50">
  %s
  %s
  <div class="handle"><span class="knob">↔</span></div>
</div>
<p class="compare-hint">Arrastra la barra para ver el antes y el después</p>""" % (
        side("after", "comparador-despues", "Después", "a"),
        side("before", "comparador-antes", "Antes", "b"))


def before_after(n=6):
    pares = [i for i in range(1, 13)
             if _find("antes-%d" % i) and _find("despues-%d" % i)]
    if pares:
        items = "".join(
            '<div class="ba zoom"><div class="h b img">%s<em>Antes</em></div>'
            '<div class="h a img">%s<em>Después</em></div></div>'
            % (media("Antes", True, "antes-%d" % i), media("Después", False, "despues-%d" % i))
            for i in pares)
    else:
        items = "".join('<div class="ba zoom"><div class="h b"><em>Antes</em></div>'
                        '<div class="h a"><em>Después</em></div></div>' for _ in range(n))
    cols = 1 if len(pares) == 1 else (2 if len(pares) in (2, 4) else 3)
    return '<div class="bagrid" style="--cols:%d">%s</div>' % (cols, items)


def video_row(nombres):
    out = []
    for w in nombres:
        sl = "video-" + slug(w)
        out.append('<div class="vid">%s</div>' % media(w, True, sl))
    return '<div class="vids hscroll">%s</div>' % "".join(out)


ICONOS = {
 # mancuerna: barra central con dos discos a cada lado
 "mancuerna": '<path d="M6.6 8.4v7.2M4 10.2v3.6M17.4 8.4v7.2M20 10.2v3.6M6.6 12h10.8"/>',
 # aguacate: contorno de la fruta con el hueso dentro
 "aguacate": '<path d="M12 3.2c3.5 0 6.3 3.3 6.3 7.4 0 4.5-2.8 9.4-6.3 9.4s-6.3-4.9-6.3-9.4c0-4.1 2.8-7.4 6.3-7.4Z"/><circle cx="12" cy="13.6" r="2.5"/>',
 # comunidad: una persona en primer plano y otra detras
 "comunidad": '<circle cx="9.4" cy="8.8" r="2.9"/><path d="M3.8 19.2c0-3.1 2.5-5 5.6-5s5.6 1.9 5.6 5"/><path d="M16.6 6.6a3 3 0 0 1 0 5.6"/><path d="M17.8 14.4c1.6.7 2.4 2.2 2.4 4.1"/>',
 # grafica: tres barras en ascenso sobre una base
 "grafica": '<path d="M4 19.4h16"/><path d="M7.4 19.4v-4.6M12 19.4v-8.4M16.6 19.4v-12"/>',
}


def icono(nombre):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % ICONOS[nombre])


def all_in_one():
    return """<div class="allin">
  <div class="collage">%s</div>
  <div class="stackr">
    <div class="panel k">
      <p class="eyebrow">Tu día, resuelto</p>
      <h3>Abre la app y ya sabes qué toca hoy</h3>
      <p class="sig">Creado por mujeres, para mujeres</p>
    </div>
    <div class="panel l">
      <p>Tu entrenamiento del día, tus macros y tus recetas te esperan abiertos. Sin improvisar y sin buscar rutinas en internet.</p>
      <a href="/crear-cuenta/" class="btn">Empezar</a>
    </div>
  </div>
</div>
<div class="tiles4">
  <a class="tile" href="/programas/"><span class="ic">%s</span><b>Entreno</b><span>6 programas</span></a>
  <a class="tile" href="/nutricion/"><span class="ic">%s</span><b>SmartFuel</b><span>Macros y recetas</span></a>
  <a class="tile" href="/comunidad/"><span class="ic">%s</span><b>BuildFam</b><span>Chat de la comunidad</span></a>
  <a class="tile" href="/membresia/"><span class="ic">%s</span><b>Progreso</b><span>Pesos, reps y selfies</span></a>
</div>""" % (media("Capturas de la app BuildUp", True, "collage"),
                  icono("mancuerna"), icono("aguacate"), icono("comunidad"), icono("grafica"))

def reviews_row():
    out = []
    for i, (txt, w) in enumerate(C.TESTIMONIOS):
        out.append('<div class="trev"><div class="tphoto zoom">%s</div>'
                   '<div class="tcard"><div class="stars">★★★★★</div><p>“%s”</p>'
                   '<div class="who">%s</div></div></div>'
                   % (media(w, False, "testimonio-" + str(i+1)), esc(txt), esc(w)))
    return '<div class="treviews">%s</div>' % "".join(out)


def recipe_card(r, link=None):
    n, cat, k, pr, cb, g, f = r
    inner = """<div class="thumb">%s<span class="rcat">%s</span></div>
      <div class="body"><h4>%s</h4>
        <div class="macros"><span><b>%d</b> kcal</span><span><b>%d</b>P</span><span><b>%d</b>C</span><span><b>%d</b>G</span></div>
      </div>""" % (media(n, False, "receta-" + slug(n)), esc(cat), esc(n), k, pr, cb, g)
    return ('<a class="rcard" href="%s">%s</a>' % (link, inner)) if link else ('<div class="rcard">%s</div>' % inner)

def vistazo(link=None):
    by = {r[0]: r for r in C.RECETAS}
    return "".join(recipe_card(by[n], link) for n in C.VISTAZO)

def program_card(p):
    chips = ('<span class="chip solid">Disponible</span>' if p["disponible"]
             else '<span class="chip soon">Próximamente</span>')
    tail = ('<span class="arrow">Ver programa <span>→</span></span>' if p["disponible"]
            else '<span class="soonnote">Muy pronto en BuildUp</span>')
    body = """<div class="thumb">%s</div>
    <div class="body">
      <div class="chips">%s<span class="chip">%s</span></div>
      <h3>%s</h3><p>%s</p>%s
    </div>""" % (media(p["nombre"], False, "programa-" + p["slug"]), chips, esc(p["nivel"]), esc(p["nombre"]), esc(p["corta"]), tail)
    if p["disponible"]:
        return '<a class="pcard" href="/programa/%s/">%s</a>' % (p["slug"], body)
    return '<div class="pcard soon" aria-disabled="true">%s</div>' % body

def faq_block(items=None):
    if items is None:
        items = C.FAQS
    return '<div class="faq">%s</div>' % "".join(
        '<details><summary>%s</summary><p class="ans">%s</p></details>' % (esc(q), esc(a)) for q, a in items)


def faq_programa(p):
    items = C.FAQS_PROGRAMA.get(p["slug"])
    if not items:
        return ""
    return """
<section class="section wash"><div class="wrap">
  <p class="section-kicker">Preguntas frecuentes</p>
  <h2 class="h-section">Sobre %s</h2>
  <div style="margin-top:42px">%s</div>
</div></section>""" % (esc(p["nombre"]), faq_block(items))

# ---------------------------------------------------------------- páginas
def page_home():
    return """<section class="hero home full">%s
  <div class="hero-in">
    <p class="eyebrow">BuildUp</p>
    <h1>Todo lo que necesitas</h1>
    <p class="sub">Entrenamiento, nutrición, progreso y comunidad en una sola app.</p>
    <a href="/crear-cuenta/" class="btn on-dark">Empieza %d días gratis</a>
  </div>
</section>

<div class="stats">
  <div class="stat"><div class="n">6</div><div class="l">Programas</div><div class="d"><span>Versión gym</span> <span>y casa</span></div></div>
  <div class="stat"><div class="n">8</div><div class="l">Semanas por ciclo</div><div class="d"><span>Tiempo real para</span> <span>adaptarte y progresar</span></div></div>
  <div class="stat"><div class="n">3<span class="dash"></span>6</div><div class="l">Días a la semana</div><div class="d"><span>Elige el split</span> <span>que se adapta a tu vida</span></div></div>
</div>

<section class="section tight ink"><div class="wrap">%s</div></section>

<section class="section"><div class="wrap">
  <p class="section-kicker">Todo en una app</p>
  <h2 class="h-section">Qué encuentras dentro</h2>
  <p class="lede center" style="margin-top:18px">Entrena, come y mide tu progreso sin salir de BuildUp.</p>
  <div class="phones three hscroll" style="margin-top:52px">
    <div class="pcol">%s<h3>Entreno</h3><p>Series, reps, descansos y video de cada ejercicio, con Modo guiado paso a paso.</p></div>
    <div class="pcol">%s<h3>SmartFuel</h3><p>Calcula tus macros, arma tu plan y registra lo que comes cada día.</p></div>
    <div class="pcol">%s<h3>Progreso</h3><p>Guarda pesos y repeticiones, tus selfies y tus semanas completadas.</p></div>
  </div>
</div></section>

%s

<section class="section"><div class="wrap">
  <p class="section-kicker">Encuentra el tuyo</p>
  <h2 class="h-section">Programas que cambian tu cuerpo</h2>
  <p class="lede center" style="margin-top:18px">Con tantos programas para elegir sabemos que puede ser difícil decidir por dónde empezar. Cada uno está diseñado para un objetivo distinto.</p>
  <div class="pgrid hscroll" style="margin-top:48px">%s</div>
</div></section>

<section class="section wash"><div class="wrap">
  <p class="section-kicker">Entrenamientos</p>
  <h2 class="h-section">Así se entrena con BuildUp</h2>
  <p class="lede center" style="margin-top:18px">Cada ejercicio con su video de técnica, sus series y repeticiones, y sus alternativas si no tienes el equipo.</p>
  <div style="margin-top:44px">%s</div>
</div></section>

<section class="section wash"><div class="wrap">
  <p class="section-kicker">Recetario</p>
  <h2 class="h-section">Un vistazo a las recetas</h2>
  <p class="lede center" style="margin-top:18px">Recetas simples y nutritivas, con calorías y macros ya calculados, que se adaptan a tu plan sin restricciones ni complicaciones.</p>
  <div class="recipes hscroll" style="margin-top:44px">%s</div>
  <div class="center" style="margin-top:40px"><a href="/nutricion/" class="btn ghost">Ver la nutrición</a></div>
</div></section>

<section class="section ink"><div class="wrap">
  <p class="section-kicker">Transformaciones</p>
  <h2 class="h-section">Resultados reales</h2>
  <p class="lede center" style="margin-top:18px">Cuando el entrenamiento, la nutrición y la rutina trabajan juntos, el progreso deja de ser suerte.</p>
  <div style="margin-top:44px">%s</div>
</div></section>

<section class="section"><div class="wrap">
  <p class="section-kicker">Comunidad</p>
  <h2 class="h-section">Lo que dice la BuildFam</h2>
  <p class="lede center" style="margin-top:18px">Historias reales de las chicas que entrenan con el método BuildUp, desde antes de que fuera una app.</p>
  <div style="margin-top:44px">%s</div>
  <div class="center" style="margin-top:44px"><a href="/crear-cuenta/" class="btn wide">Empieza %d días gratis</a></div>
</div></section>""" % (media("Entrenamiento en el gym", True, "hero-home", "center 35%"), P["prueba_dias"], all_in_one(),
       media("Entreno en BuildUp", False, "dentro-entreno"),
       media("SmartFuel en BuildUp", False, "dentro-smartfuel"),
       media("Progreso en BuildUp", False, "dentro-progreso"), member_band(True),
       "".join(program_card(p) for p in C.PROGRAMAS), video_row(C.ENTRENOS_DEMO), vistazo("/nutricion/"),
       comparator(), reviews_row(), P["prueba_dias"])

def page_membresia():
    return """<section class="hero full">%s
  <div class="hero-in"><p class="eyebrow">Tu membresía</p><h1>¿Qué pasa cuando te unes?</h1></div>
</section>
%s
<section class="section wash"><div class="wrap">
  <p class="section-kicker">Cómo se ve tu día</p>
  <h2 class="h-section">Un día con BuildUp</h2>
  <div class="phones hscroll" style="margin-top:52px">
    <div class="pcol">%s<h3>Empieza el día</h3><p>Abres la app y ves tu entreno, tus macros y tu lista del día en un solo lugar.</p></div>
    <div class="pcol">%s<h3>Entrena</h3><p>Sigue la rutina con series, reps, temporizador de descanso y video de técnica.</p></div>
    <div class="pcol">%s<h3>Aliméntate</h3><p>Registra tus comidas y mira cómo se actualizan tus macros en tiempo real.</p></div>
    <div class="pcol">%s<h3>Cierra el día</h3><p>Marca tu entrenamiento como completado, guarda tu selfie y comparte tu logro con la BuildFam.</p></div>
  </div>
</div></section>
<section class="section"><div class="wrap">
  <p class="section-kicker">Entrenamientos</p>
  <h2 class="h-section">Entrenamientos del día</h2>
  <p class="lede center" style="margin-top:18px">Cada ejercicio viene con su video, señales de técnica y alternativas si no tienes el equipo.</p>
  <div style="margin-top:44px">%s</div>
</div></section>
<section class="section ink"><div class="wrap">
  <p class="section-kicker">Transformaciones</p>
  <h2 class="h-section">Resultados reales</h2>
  <p class="lede center" style="margin-top:18px">Cuando el entrenamiento, la nutrición y la rutina trabajan juntos, el progreso deja de ser suerte. Esto es lo que parece la constancia.</p>
  <div style="margin-top:44px">%s</div>
  <div class="center" style="margin-top:44px"><a href="/crear-cuenta/" class="btn on-dark wide">Empieza %d días gratis</a></div>
</div></section>
<section class="section wash"><div class="wrap">
  <p class="section-kicker">Incluido en la membresía</p>
  <h2 class="h-section">Todo lo que desbloqueas</h2>
  <div class="two-col" style="margin-top:44px">
    <div class="listcard"><h4>Entrenamiento</h4><ul>
      <li>Los 6 programas y todas sus versiones</li><li>Splits de 3 a 6 días</li>
      <li>Versión gym y versión en casa</li><li>Registro de pesos y reps</li>
      <li>Calentamiento y abdominales</li><li>Cardio HIIT y LISS, casa y gym</li>
      <li>Movilidad, estiramientos y descanso activo</li><li>Modo guiado y reordenar tu semana</li>
    </ul></div>
    <div class="listcard"><h4>Nutrición y comunidad</h4><ul>
      <li>Calorías y macros personalizados</li><li>Plan de alimentación editable</li>
      <li>Recetario con macros</li><li>Tracker diario de comidas y agua</li>
      <li>Chat de la BuildFam</li><li>Selfies y línea de progreso</li>
    </ul></div>
  </div>
  <div class="center" style="margin-top:48px"><a href="/crear-cuenta/" class="btn wide">Empieza %d días gratis</a></div>
</div></section>""" % (media("Sentadilla con barra", True, "hero-membresia", "center 35%"), member_band(False),
        media("Empieza el día en BuildUp", False, "mem-paso-1"),
        media("Entrena con BuildUp", False, "mem-paso-2"),
        media("Aliméntate con SmartFuel", False, "mem-paso-3"),
        media("Cierra el día en BuildUp", False, "mem-paso-4"),
        video_row(C.ENTRENOS_DEMO),
        before_after(6), P["prueba_dias"], P["prueba_dias"])

def page_programas():
    return """<div class="pagehead"><div class="wrap">
  <p class="eyebrow">Programas</p>
  <h1>Encuentra tu programa ideal</h1>
  <p>Con tantos programas para elegir sabemos que puede ser difícil decidir por dónde empezar. Seis programas, un mismo método: ciclos de 8 semanas, progresión medida y versión gym o casa.</p>
</div><div class="rule"></div></div>
<section class="section"><div class="wrap"><div class="pgrid two">%s</div></div></section>
<section class="section wash" id="faq"><div class="wrap">
  <p class="section-kicker">Preguntas frecuentes</p>
  <h2 class="h-section">Antes de empezar</h2>
  <div style="margin-top:42px">%s</div>
</div></section>
%s""" % ("".join(program_card(p) for p in C.PROGRAMAS), faq_block(), member_band(False))

def programa_shots(p):
    sl = "capturas-" + p["slug"]
    if _find(sl):
        return '<div class="shots">%s</div>' % media("Capturas de " + p["nombre"], True, sl)
    return '<div class="trio">%s%s%s</div>' % (phone("hoy"), phone("entreno"), phone("perfil"))


def page_programa(p):
    vers = ""
    if len(p["versiones"]) > 1:
        pills = "".join('<span class="ver%s">%s %s</span>' % (" now" if i == len(p["versiones"])-1 else "",
                        esc(p["nombre"].split(" ")[0]), esc(v)) for i, v in enumerate(p["versiones"]))
        vers = """<h4 style="margin-top:34px">Versiones</h4>
        <p style="font-size:13.5px;color:var(--grey);margin:0 0 14px">Cada versión es un ciclo completo de 8 semanas. Al terminar una, pasas a la siguiente, con nuevos ejercicios y variantes para evitar el estancamiento.</p>
        <div class="versions">%s</div>""" % pills
    badges = "".join('<span class="badge%s">%s</span>' % (" k" if i == 0 else "", esc(b)) for i, b in enumerate(p["badges"]))
    return """<section class="hero full">%s
  <div class="hero-in"><p class="eyebrow">%s</p><h1>%s</h1><p class="sub">%s</p></div>
</section>
<section class="section ink"><div class="wrap inside">
  %s
  <div>
    <p class="kicker">%s</p><h2>Dentro del programa</h2>
    <div class="badges">%s</div>
    %s
    <div style="margin-top:26px"><a href="/crear-cuenta/" class="btn">Empieza %d días gratis</a></div>
  </div>
</div></section>
<section class="section"><div class="wrap"><div class="two-col">
  <div class="listcard"><h4>Enfoque del programa</h4><ul>%s</ul>%s</div>
  <div class="listcard"><h4>¿Qué incluye?</h4><ul>%s</ul></div>
</div></div></section>
<section class="section wash"><div class="wrap">
  <p class="section-kicker">Entrenamientos</p>
  <h2 class="h-section">Entrenamientos del día</h2>
  <p class="lede center" style="margin-top:18px">Así se entrena con el Modo guiado: cada ejercicio con su video de técnica, sus series y repeticiones, y sus alternativas.</p>
  <div style="margin-top:44px">%s</div>
</div></section>
<section class="section"><div class="wrap">
  <p class="section-kicker">Se adapta a tu estilo de vida</p>
  <h2 class="h-section">Elige cuántos días entrenas</h2>
  <div class="splits" style="margin-top:44px">%s</div>
</div></section>
<section class="section wash"><div class="wrap">
  <p class="section-kicker">Cómo ejecutar el entrenamiento</p>
  <h2 class="h-section">Tu sesión, paso a paso</h2>
  <div class="steps" style="margin-top:46px">
    <div class="step"><div class="num">1</div><h4>Calentamiento y abs</h4><p>Rutina de abdominales de ~10 minutos en circuito, siguiendo el orden y los tiempos indicados.</p></div>
    <div class="step"><div class="num">2</div><h4>Fuerza</h4><p>Ejercicios solos y supersets. Registra el peso y las reps de cada serie para aplicar sobrecarga progresiva.</p></div>
    <div class="step"><div class="num">3</div><h4>Cardio</h4><p>Elige la opción que se adapte a tu nivel y disponibilidad. El HIIT no más de 4 días por semana.</p></div>
    <div class="step"><div class="num">4</div><h4>Registro</h4><p>Marca el entreno como completado y guarda tus datos para medir el progreso semana a semana.</p></div>
  </div>
</div></section>
<section class="section ink"><div class="wrap">
  <p class="section-kicker">Transformaciones</p>
  <h2 class="h-section">Resultados reales</h2>
  <p class="lede center" style="margin-top:18px">Cuando el entrenamiento, la nutrición y la rutina trabajan juntos, el progreso deja de ser suerte. Esto es lo que parece la constancia.</p>
  <div style="margin-top:44px">%s</div>
  <div class="center" style="margin-top:44px"><a href="/crear-cuenta/" class="btn on-dark wide">Empieza %d días gratis</a></div>
</div></section>%s""" % (
    media(p["nombre"], True, "hero-programa-" + p["slug"], "center 18%"),
    "Disponible ahora" if p["disponible"] else "Próximamente", esc(p["nombre"]), esc(p["enfoque_linea"]),
    programa_shots(p), esc(p["nombre"]), badges,
    "".join("<p>%s</p>" % esc(t) for t in p["intro"]), P["prueba_dias"],
    "".join("<li>%s</li>" % esc(x) for x in p["enfoque"]), vers,
    "".join("<li>%s</li>" % esc(x) for x in p["incluye"]),
    video_row(C.ENTRENOS_DEMO),
    "".join('<div class="split"><div class="d">%s</div><div class="u">%s</div><p>%s</p></div>' % (esc(d), esc(u), esc(t)) for d, u, t in p["splits"]),
    before_after(6), P["prueba_dias"], faq_programa(p))

def page_nutricion():
    return """<section class="hero full izq">%s
  <div class="hero-in">
    <p class="eyebrow">SmartFuel</p>
    <h1>Nutre tus metas</h1>
    <p class="sub">Tu nutrición y recetas, en un mismo lugar.</p>
    <a href="/crear-cuenta/" class="btn on-dark">Empieza %d días gratis</a>
  </div>
</section>
<section class="section"><div class="wrap">
  <p class="section-kicker">Cómo funciona</p>
  <h2 class="h-section">Registra tu día en minutos</h2>
  <p class="lede center" style="margin-top:18px">Explora nuestras recetas, calcula tus macros y empieza a nutrirte de acuerdo a tus objetivos con el tracker diario, todo dentro de la app.</p>
  <div class="phones hscroll" style="margin-top:52px">
    <div class="pcol">%s<h3>1 · Tu objetivo</h3><p>Perder grasa, definición muscular o superávit calórico moderado.</p></div>
    <div class="pcol">%s<h3>2 · Tus macros</h3><p>Calculamos tus calorías y macros personalizados según tus datos.</p></div>
    <div class="pcol">%s<h3>3 · Registra</h3><p>Alimentos sueltos, una receta o tu comida personalizada. Como te quede más fácil.</p></div>
    <div class="pcol">%s<h3>4 · Sigue tu día</h3><p>Mira cuánto te queda de cada macro y cierra el día completo.</p></div>
  </div>
  <div class="center" style="margin-top:44px"><a href="/crear-cuenta/" class="btn">Empieza %d días gratis</a></div>
</div></section>
<section class="section wash"><div class="wrap">
  <p class="section-kicker">Tu nutrición, a tu manera</p>
  <h2 class="h-section">Tres formas de registrar tus comidas</h2>
  <p class="lede center" style="margin-top:18px">Registra como te resulte más fácil ese día. Las tres suman a los mismos macros.</p>
  <div class="ways three hscroll" style="margin-top:46px">
    <a class="way zoom" href="/crear-cuenta/">
      <div class="thumb">%s</div><h3>Alimentos individuales</h3>
      <p>Busca cualquier alimento en la biblioteca de SmartFuel, elige la porción y los macros se calculan solos.</p>
      <span class="arrow">Explorar <span>→</span></span></a>
    <a class="way zoom" href="/crear-cuenta/">
      <div class="thumb">%s</div><h3>Desde una receta</h3>
      <p>Elige una receta de la biblioteca y agrégala a tu día con sus calorías y macros ya calculados.</p>
      <span class="arrow">Explorar <span>→</span></span></a>
    <div class="way soon" aria-disabled="true">
      <div class="thumb">%s<span class="lock"><span>&#128274;</span></span></div><h3>Comida personalizada</h3>
      <p>¿Comiste algo que no está en la app? Agrégalo manualmente con su foto y sus macros y guárdalo para después.</p>
      <span class="soonpill">Próximamente</span></div>
  </div>
</div></section>
<section class="section"><div class="wrap" style="max-width:760px">
  <p class="section-kicker">Sin restricciones</p>
  <h2 class="h-section">Comida real, calculada</h2>
  <div class="checks" style="margin-top:34px">
    <div class="check"><b>✓</b><span>Cada receta trae sus calorías y macros ya calculados.</span></div>
    <div class="check"><b>✓</b><span>Sin eliminar grupos de alimentos ni prohibir nada.</span></div>
    <div class="check"><b>✓</b><span>Diseñada para acompañar tu entrenamiento, no para pelearse con él.</span></div>
    <div class="check"><b>✓</b><span>Objetivos calculados según tus datos: perder grasa, definir o superávit moderado.</span></div>
  </div>
</div></section>
<section class="section wash"><div class="wrap">
  <p class="section-kicker">Recetario</p>
  <h2 class="h-section">Un vistazo a las recetas</h2>
  <p class="lede center" style="margin-top:18px">Recetas simples y nutritivas, con calorías y macros ya calculados, que se adaptan a tu plan sin restricciones ni complicaciones.</p>
  <div class="recipes hscroll" style="margin-top:44px">%s</div>
</div></section>
%s""" % (media("Ingredientes frescos", True, "nutricion-hero", "center 40%"), P["prueba_dias"],
         media("Tu objetivo en SmartFuel", False, "nutri-paso-1"),
         media("Tus macros en SmartFuel", False, "nutri-paso-2"),
         media("Registrar una comida en SmartFuel", False, "nutri-paso-3"),
         media("Seguimiento del día en SmartFuel", False, "nutri-paso-4"), P["prueba_dias"],
         media("Buscador de alimentos", False, "nutricion-alimentos"), media("Receta lista", False, "nutricion-receta"), media("Plato casero", False, "nutricion-personalizada"),
         vistazo(), member_band(False))

def page_comunidad():
    return """<section class="hero full">%s
  <div class="hero-in"><p class="eyebrow">BuildFam</p><h1>No entrenas sola</h1>
  <p class="sub">Comparte tu progreso y conecta con BuildFam.</p></div>
</section>
<section class="section"><div class="wrap inside">
  %s
  <div>
    <p class="kicker">BuildFam</p><h2>Dentro de la comunidad</h2>
    <div class="badges"><span class="badge k">CHAT</span><span class="badge">DUDAS</span><span class="badge">PROGRESO</span></div>
    <p>Mantente activa en el chat de la BuildFam: un espacio para motivarte, recibir apoyo, resolver dudas y compartir tu progreso durante tu transformación.</p>
    <p>Aquí preguntas cómo adaptar un ejercicio, cuentas que terminaste la semana 4, o encuentras a alguien que va por el mismo programa que tú.</p>
    <p>Y no estás sola: %s está dentro del chat, leyendo y respondiendo, para ayudarte cuando lo necesites.</p>
    <div style="margin-top:26px"><a href="/crear-cuenta/" class="btn">Únete a BuildFam</a></div>
  </div>
</div></section>
<section class="section wash"><div class="wrap">%s
  <div class="center" style="margin-top:44px"><a href="/crear-cuenta/" class="btn wide">Empieza %d días gratis</a></div>
</div></section>""" % (media("La comunidad BuildFam", True, "hero-comunidad", "center 28%"), ('<div class="shots">%s</div>' % media("Chat de la BuildFam", False, "capturas-comunidad")
                        if _find("capturas-comunidad")
                        else '<div class="trio">%s%s%s</div>' % (phone("chat2"), phone("chat"), phone("chat3"))),
                       esc(S["coach"]), reviews_row(), P["prueba_dias"])


RC_SDK = "https://cdn.jsdelivr.net/npm/@revenuecat/purchases-js@1.73.2/dist/Purchases.es.js"
FB_APP = "https://www.gstatic.com/firebasejs/13.2.0/firebase-app.js"
FB_AUTH = "https://www.gstatic.com/firebasejs/13.2.0/firebase-auth.js"
FB_FS = "https://www.gstatic.com/firebasejs/13.2.0/firebase-firestore.js"
FB_FN = "https://www.gstatic.com/firebasejs/13.2.0/firebase-functions.js"


def script_pago():
    cfg = json.dumps({
        "activo": C.PAGO["activo"],
        "rcKey": C.PAGO["rc_api_key"],
        "ent": C.PAGO["entitlement"],
        "fb": C.PAGO["firebase"],
        "terminos": C.legal_url("terminos"),
    }, ensure_ascii=False)
    return """
<script type="module">
const CFG = %s;
const qsPrueba = new URLSearchParams(location.search).get("pago") === "prueba";
if (qsPrueba) { try { sessionStorage.setItem("bu_prueba", "1"); } catch (_) {} }
let pruebaGuardada = false;
try { pruebaGuardada = sessionStorage.getItem("bu_prueba") === "1"; } catch (_) {}
const modoPrueba = qsPrueba || pruebaGuardada;
const activo = CFG.activo || modoPrueba;
if (modoPrueba && !CFG.activo) {
  const bandera = document.createElement("div");
  bandera.textContent = "MODO PRUEBA \u00b7 el cobro es de mentira";
  bandera.style.cssText = "position:fixed;left:14px;bottom:14px;z-index:99999;background:#111;color:#fff;font:600 11px/1 Inter,system-ui,sans-serif;letter-spacing:.09em;text-transform:uppercase;padding:10px 14px;border-radius:999px;box-shadow:0 6px 24px rgba(0,0,0,.28)";
  (document.body || document.documentElement).appendChild(bandera);
}
const boton = document.getElementById("btn-pagar");
const panelDiag = (() => {
  if (!modoPrueba || CFG.activo) return null;
  const d = document.createElement("div");
  d.style.cssText = "position:fixed;left:14px;bottom:58px;z-index:99999;background:rgba(17,17,17,.95);color:#8ef0c0;max-width:320px;max-height:46vh;overflow:auto;font:500 11px/1.5 ui-monospace,Menlo,monospace;padding:11px 13px;border-radius:12px;white-space:pre-wrap;box-shadow:0 6px 24px rgba(0,0,0,.3)";
  d.textContent = "DIAGNOSTICO";
  (document.body || document.documentElement).appendChild(d);
  return d;
})();
const diag = (t) => { if (panelDiag) { panelDiag.textContent += "\n" + t; panelDiag.scrollTop = panelDiag.scrollHeight; } };
if (modoPrueba) {
  window.addEventListener("error", (e) => diag("JS ERROR: " + e.message));
  window.addEventListener("unhandledrejection", (e) => diag("PROMESA: " + ((e.reason && (e.reason.message || e.reason.code)) || e.reason)));
}

const aviso = document.getElementById("pago-error");
const caja  = document.getElementById("checkout");
const salud = document.getElementById("salud");
const nota  = document.getElementById("nota-salud");
const sincro = () => {
  const ok = !!(salud && salud.checked);
  if (boton) boton.disabled = !ok;
  if (nota) nota.hidden = ok;
};
if (salud) salud.addEventListener("change", sincro);
sincro();
if (boton) {
  if (!activo) {
    boton.addEventListener("click", () => { location.href = "/listo/"; });
  } else {
    const di = (m) => { aviso.textContent = m; aviso.hidden = !m; };
    const planSel = () => {
      const s = document.querySelector(".plan.sel");
      return s && s.dataset.plan === "mensual" ? "mensual" : "anual";
    };
    boton.addEventListener("click", async () => {
      const nombre = (document.getElementById("n").value || "").trim();
      const correo = (document.getElementById("e").value || "").trim();
      const clave  = document.getElementById("c").value || "";
      const fnac   = document.getElementById("f").value || "";
      const quiereSalud = document.getElementById("salud").checked;
      di("");
      if (!nombre)                      return di("Escribe tu nombre.");
      if (!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(correo)) return di("Revisa tu correo, parece que falta algo.");
      if (clave.length < 8)             return di("La contraseña necesita al menos 8 caracteres.");
      if (!fnac)                        return di("Pon tu fecha de nacimiento.");
      const nacimiento = new Date(fnac + "T12:00:00");
      if (isNaN(nacimiento))            return di("Esa fecha de nacimiento no es válida.");
      const hoy = new Date();
      let edad = hoy.getFullYear() - nacimiento.getFullYear();
      const md = hoy.getMonth() - nacimiento.getMonth();
      if (md < 0 || (md === 0 && hoy.getDate() < nacimiento.getDate())) edad--;
      if (edad < 18)                    return di("Tienes que ser mayor de 18 años para usar BuildUp.");
      if (edad > 110)                   return di("Revisa tu fecha de nacimiento.");
      const textoOriginal = boton.textContent;
      boton.disabled = true; boton.textContent = "Creando tu cuenta...";
      try {
        const [{ initializeApp }, fbAuth, fbFs, fbFn, { Purchases }] = await Promise.all([
          import("%s"), import("%s"), import("%s"), import("%s"), import("%s"),
        ]);
        const app  = initializeApp(CFG.fb);
        const auth = fbAuth.getAuth(app);
        const db   = fbFs.getFirestore(app);
        let cred;
        try {
          cred = await fbAuth.createUserWithEmailAndPassword(auth, correo, clave);
          await fbAuth.updateProfile(cred.user, { displayName: nombre });
        } catch (err) {
          if (err && err.code === "auth/email-already-in-use") {
            try {
              cred = await fbAuth.signInWithEmailAndPassword(auth, correo, clave);
            } catch (_) {
              boton.textContent = textoOriginal; sincro();
              return di("Ya existe una cuenta con ese correo. Entra desde Iniciar sesión.");
            }
          } else if (err && err.code === "auth/weak-password") {
            boton.textContent = textoOriginal; sincro();
            return di("Esa contraseña es muy débil, prueba con una más larga.");
          } else if (err && err.code === "auth/invalid-email") {
            boton.textContent = textoOriginal; sincro();
            return di("Ese correo no parece válido.");
          } else {
            throw err;
          }
        }
        const uid = cred.user.uid;
        diag("1 cuenta OK uid=" + uid.slice(0, 10));
        // Mismo documento que crea la app al registrarse (users/{uid}).
        // Si ya existe no lo tocamos: lo habra creado la app o un intento anterior.
        const ref = fbFs.doc(db, "users", uid);
        const snap = await fbFs.getDoc(ref);
        if (!snap.exists()) {
          await fbFs.setDoc(ref, {
            uid: uid,
            email: correo,
            display_name: nombre,
            created_time: fbFs.serverTimestamp(),
            photo_url: "",
            phone_number: "",
            fechaNacimiento: fbFs.Timestamp.fromDate(nacimiento),
            aceptoTerminos: true,
            aceptoTerminosFecha: fbFs.serverTimestamp(),
            aceptoTerminosVersion: "1.0",
          });
          diag("2 documento users creado");
        } else { diag("2 users ya existia"); }
        if (quiereSalud) {
          // Igual que la app: la funcion deja constancia en registroConsentimientos
          // ademas de poner los campos en el perfil.
          try {
            const fn = fbFn.httpsCallable(fbFn.getFunctions(app), "actualizarConsentimiento");
            await fn({ tipo: "salud", otorgar: true, origen: "web" });
            diag("3 consentimiento por funcion OK");
          } catch (errFn) {
            diag("3 funcion fallo: " + (errFn && (errFn.code || errFn.message)) + " -> escribo directo");
            console.warn("consentimiento por funcion no disponible, se escribe directo", errFn);
            let version = "1.0";
            try {
              const aj = await fbFs.getDoc(fbFs.doc(db, "ajustes", "legal"));
              if (aj.exists() && aj.data().versionConsentSalud) version = aj.data().versionConsentSalud;
            } catch (_) {}
            await fbFs.setDoc(ref, {
              consintioSalud: true,
              consintioSaludFecha: fbFs.serverTimestamp(),
              consintioSaludVersion: version,
            }, { merge: true });
          }
        }
        if (!Purchases.isConfigured()) Purchases.configure({ apiKey: CFG.rcKey, appUserId: uid });
        else await Purchases.getSharedInstance().changeUser(uid);
        const rc = Purchases.getSharedInstance();
        diag("4 revenuecat configurado");
        const offs = await rc.getOfferings();
        diag("5 offerings OK");
        const act = offs.current;
        if (!act) throw new Error("sin offering");
        const pkg = planSel() === "mensual" ? act.monthly : act.annual;
        if (!pkg) throw new Error("sin paquete");
        boton.textContent = "Abriendo el pago...";
        caja.hidden = false;
        const irAlPago = () => { try { caja.scrollIntoView({ behavior: "auto", block: "start" }); } catch (_) {} };
        irAlPago(); setTimeout(irAlPago, 900); setTimeout(irAlPago, 2400);
        const ajustarCaja = () => {
          const k = caja.firstElementChild;
          if (!k) return;
          const sc = Array.from(k.querySelectorAll("div")).find(
            (d) => d.scrollHeight > d.clientHeight + 4 && d.clientHeight > 120
          );
          if (!sc) return;
          const extra = sc.scrollHeight - sc.clientHeight;
          const alto = caja.getBoundingClientRect().height + extra + 12;
          caja.style.height = Math.min(1600, Math.round(alto)) + "px";
        };
        [700, 1400, 2200, 3200, 4500, 6000].forEach((ms) => setTimeout(ajustarCaja, ms));
        window.addEventListener("resize", () => {
          caja.style.height = "";
          setTimeout(ajustarCaja, 300);
        });
        setTimeout(() => {
          diag("7 a los 9s: hijos=" + caja.children.length + " alto=" + caja.offsetHeight + " iframes=" + caja.querySelectorAll("iframe").length);
          if (!caja.hidden && caja.children.length === 0) {
            di("No pudimos abrir el formulario de pago. Recarga la p\u00e1gina e int\u00e9ntalo otra vez; si sigue igual, escr\u00edbenos y lo resolvemos.");
          }
        }, 9000);
        diag("6 llamando a purchase()");
        const res = await rc.purchase({
          rcPackage: pkg,
          customerEmail: correo,
          htmlTarget: caja,
          selectedLocale: "es",
          termsAndConditionsUrl: location.origin + CFG.terminos,
          brandingAppearanceOverride: {
            color_buttons_primary: "#000000",
            color_buttons_primary_text: "#FFFFFF",
            color_accent: "#000000",
            color_error: "#B42318",
            color_product_info_bg: "#F5F5F5",
            color_form_bg: "#FFFFFF",
            color_page_bg: "#FFFFFF",
            font: "Inter",
            shapes: "rounded",
            show_product_description: true,
          },
        });
        if (res) { location.href = "/listo/"; return; }
      } catch (err) {
        caja.hidden = true; caja.innerHTML = "";
        boton.textContent = textoOriginal; sincro();
        diag("ERROR FINAL: " + (err && (err.message || err.errorCode || err.code)));
        const cancelado = err && (err.errorCode === 1 || String(err.message || "").toLowerCase().includes("cancel"));
        if (cancelado) di("");
        else { console.error(err); di("No pudimos completar el pago. Inténtalo de nuevo o escríbenos."); }
      }
    });
  }
}
</script>""" % (cfg, FB_APP, FB_AUTH, FB_FS, FB_FN, RC_SDK)


def page_crear_cuenta():
    a, m = P["anual"], P["mensual"]
    return """<section class="section" style="padding:66px 0 92px"><div class="wrap" style="max-width:880px">
  <p class="section-kicker">Empieza hoy</p>
  <h2 class="h-section">Crea tu cuenta</h2>
  <p class="lede center" style="margin-top:16px">%d días gratis con acceso a toda la app. Cancela cuando quieras.</p>
  <div class="stepper"><span class="stp on"><b>1</b> Cuenta</span><span class="stp on"><b>2</b> Plan</span><span class="stp"><b>3</b> Pago</span></div>
  <div class="signup">
    <div class="scardx"><h4>Tu cuenta</h4>
      <label for="n">Nombre</label><input id="n" type="text" placeholder="Tu nombre">
      <label for="e">Correo</label><input id="e" type="email" placeholder="tu@correo.com">
      <label for="c">Contraseña</label><input id="c" type="password" placeholder="Mínimo 8 caracteres">
      <label for="f">Fecha de nacimiento</label><input id="f" type="date">
      <p class="hint">Este mismo correo y contraseña son los que usarás para entrar en la app. Tu prueba queda ligada a esta cuenta. Debes ser mayor de 18 años.</p>
      <label class="chk" for="salud"><input id="salud" type="checkbox"><span>Sí, quiero registrar mi peso, mis medidas y mis fotos de progreso en mi cuenta para ver mi evolución. <a href="%s" target="_blank" rel="noopener">Más información</a></span></label>
    </div>
    <div class="scardx"><h4>Tu plan</h4>
      <div class="plan sel" data-plan="anual" data-price="%s al año" role="button" tabindex="0" style="margin-top:0">
        <span class="ribbon">%s</span>
        <div><div class="mini">★ Oferta exclusiva</div><div class="nm">Anual</div><div class="pr">%s %s</div><div class="rn">Equivale a %s al mes</div></div>
        <span class="dot"></span></div>
      <div class="plan" data-plan="mensual" data-price="%s al mes" role="button" tabindex="0">
        <div><div class="mini">Cancela cuando quieras</div><div class="nm">Mensual</div><div class="pr">%s %s</div><div class="rn">%s</div></div>
        <span class="dot"></span></div>
      <div class="summary">
        <div class="big"><span>Hoy pagas</span><b>$0.00</b></div>
        <div><span>A partir del día %d</span><b data-after>%s al año</b></div>
      </div>
      <div style="margin-top:22px"><button id="btn-pagar" class="btn wide" style="width:100%%">Empezar %d días gratis</button></div>
      <p class="hint" id="nota-salud" style="margin-top:10px">Marca la casilla de arriba para continuar.</p>
      <p class="formerr" id="pago-error" hidden></p>
      <p class="legalnote">Al continuar aceptas los <a href="%s" target="_blank" rel="noopener">Términos de servicio</a> y la <a href="%s" target="_blank" rel="noopener">Política de privacidad</a>. Te avisamos por correo antes de que terminen los %d días, y puedes cancelar en cualquier momento desde tu cuenta.</p>
    </div>
  </div>
  <div id="checkout" hidden></div>
</div></section>""" % (P["prueba_dias"], C.legal_url("consentimiento-datos-salud"),
    a["importe"], a["cinta"], a["importe"], a["periodo"], a["mensualizado"],
    m["importe"], m["importe"], m["periodo"], m["renovacion"], P["prueba_dias"]+1, a["importe"],
    P["prueba_dias"], C.legal_url("terminos"), C.legal_url("privacidad"), P["prueba_dias"]) + script_pago()

def page_listo():
    return """<section class="section" style="padding:86px 0 100px"><div class="wrap" style="max-width:660px;text-align:center">
  <div class="donemark">✓</div>
  <h2 class="h-section" style="margin-top:26px">Tu prueba empieza hoy</h2>
  <p class="lede" style="margin-top:18px">Ya tienes acceso completo a BuildUp durante %d días. Descarga la app y entra con el mismo correo con el que acabas de crear tu cuenta.</p>
  <div class="stores">
    <a class="store" href="#"><b>App Store</b><span>Descargar para iPhone</span></a>
    <a class="store" href="#"><b>Google Play</b><span>Descargar para Android</span></a>
  </div>
  <div class="nextsteps"><h4>Qué sigue</h4><ol>
    <li>Descarga la app e inicia sesión con tu correo.</li>
    <li>Responde el cuestionario: tu objetivo, dónde entrenas y cuántos días.</li>
    <li>Elige tu programa, o deja que la guía te recomiende uno.</li>
    <li>Empieza tu primer entrenamiento y registra tus pesos.</li>
  </ol></div>
</div></section>""" % P["prueba_dias"]

def page_login():
    return """<section class="section" style="padding:110px 0 130px"><div class="wrap" style="max-width:440px">
  <div style="border:1px solid var(--line);border-radius:var(--r-md);padding:38px 34px">
    <h2 style="font-size:26px;letter-spacing:-.01em">Iniciar sesión</h2>
    <p style="color:var(--grey);font-size:14px;margin:10px 0 26px">Entra con el correo con el que creaste tu cuenta BuildUp.</p>
    <label style="font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)" for="le">Correo</label>
    <input id="le" type="email" placeholder="tu@correo.com" style="width:100%;margin:8px 0 18px;padding:14px 16px;border:1px solid var(--line);border-radius:var(--r-sm);font:inherit;background:#fff">
    <label style="font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)" for="lc">Contraseña</label>
    <input id="lc" type="password" placeholder="••••••••" style="width:100%;margin:8px 0 24px;padding:14px 16px;border:1px solid var(--line);border-radius:var(--r-sm);font:inherit;background:#fff">
    <button class="btn" style="width:100%">Entrar</button>
    <p style="text-align:center;font-size:13px;color:var(--grey);margin:20px 0 0">¿No tienes cuenta? <a href="/crear-cuenta/" style="border-bottom:1px solid var(--line)">Crea la tuya y empieza 7 días gratis</a></p>
  </div>
</div></section>"""

# ---------------------------------------------------------------- generar

# ---------------------------------------------------------------- legal
import re as _re

def _inline(s):
    s = esc(s)
    s = _re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    def _a(m):
        txt, url = m.group(1), m.group(2)
        url = _re.sub(r'^https?://mariagabsfitness\.com/pages/([a-z0-9\-]+)/?$', r'/legal/\1/', url)
        ext = '' if url.startswith('/') else ' target="_blank" rel="noopener"'
        return '<a href="%s"%s>%s</a>' % (url, ext, txt)
    return _re.sub(r'\[([^\]]+)\]\(([^)]+)\)', _a, s)


def md_a_html(texto):
    out, lista = [], False
    for linea in texto.split("\n"):
        l = linea.rstrip()
        if l.startswith("- "):
            if not lista: out.append("<ul>"); lista = True
            out.append("<li>%s</li>" % _inline(l[2:]))
            continue
        if lista: out.append("</ul>"); lista = False
        if not l.strip(): continue
        if l.startswith("### "):  out.append("<h3>%s</h3>" % _inline(l[4:]))
        elif l.startswith("## "): out.append("<h2>%s</h2>" % _inline(l[3:]))
        else:                     out.append("<p>%s</p>" % _inline(l))
    if lista: out.append("</ul>")
    return "\n".join(out)


def leer_legal(slug):
    ruta = os.path.join("legal", slug + ".md")
    if not os.path.isfile(ruta):
        return None, None
    txt = io.open(ruta, encoding="utf-8").read().strip()
    lineas = txt.split("\n")
    titulo = lineas[0][2:].strip() if lineas[0].startswith("# ") else slug
    for cola in (" | BuildUp", " – BuildUp", " — BuildUp", " de BuildUp"):
        if titulo.endswith(cola):
            titulo = titulo[: -len(cola)].strip()
    return titulo, md_a_html("\n".join(lineas[1:]))


def page_legal(slug):
    titulo, cuerpo = leer_legal(slug)
    return """<div class="pagehead"><div class="wrap">
  <p class="eyebrow">Legal</p>
  <h1>%s</h1>
</div><div class="rule"></div></div>
<section class="section"><div class="wrap"><div class="legal">%s</div></div></section>""" % (esc(titulo), cuerpo)


PAGES = [
  ("/", "BuildUp — Entrenamiento, nutrición y progreso en una sola app",
   "Programas de entrenamiento para gym y casa, plan de alimentación con macros, recetario y comunidad. Empieza con 7 días gratis.", page_home, ""),
  ("/membresia/", "Membresía BuildUp — 7 días gratis, acceso a todo",
   "Acceso completo a los 6 programas, SmartFuel, el recetario, el registro de progreso y la BuildFam. Desde $15.00 al mes.", page_membresia, "membresia"),
  ("/programas/", "Programas de entrenamiento — BuildUp",
   "Seis programas para gym y casa: Build & Shred, Build & Sculpt, BuildXpress y más. Ciclos de 8 semanas con splits de 3 a 6 días.", page_programas, "programas"),
  ("/nutricion/", "SmartFuel — Nutrición y recetas — BuildUp",
   "Calcula tus calorías y macros, arma tu plan de alimentación y registra tu día con 42 recetas calculadas.", page_nutricion, "nutricion"),
  ("/comunidad/", "BuildFam — La comunidad de BuildUp",
   "El chat donde las chicas de BuildUp comparten su progreso, resuelven dudas y se motivan durante su transformación.", page_comunidad, "comunidad"),
  ("/crear-cuenta/", "Crea tu cuenta — 7 días gratis — BuildUp",
   "Crea tu cuenta BuildUp y empieza 7 días gratis con acceso completo a la app. Cancela cuando quieras.", page_crear_cuenta, ""),
  ("/listo/", "Tu prueba empieza hoy — BuildUp",
   "Descarga la app y entra con tu cuenta para empezar tus 7 días gratis.", page_listo, ""),
  ("/login/", "Iniciar sesión — BuildUp",
   "Entra a tu cuenta de BuildUp.", page_login, "login"),
]

def write(path, text):
    full = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    io.open(full, "w", encoding="utf-8").write(text)
    return full

def main():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree("assets", os.path.join(OUT, "assets"))
    urls = []
    for path, title, desc, fn, active in PAGES:
        write(path, doc(path, title, desc, fn(), active)); urls.append(path)
    for _t, sl in C.LEGAL_ES + C.LEGAL_EN:
        tit, _c = leer_legal(sl)
        if tit is None:
            print("  (falta legal/%s.md)" % sl); continue
        path = "/legal/%s/" % sl
        write(path, doc(path, "%s — BuildUp" % tit, tit, page_legal(sl), ""))
        urls.append(path)
    for p in C.PROGRAMAS:
        path = "/programa/%s/" % p["slug"]
        title = "%s — Programa de entrenamiento — BuildUp" % p["nombre"]
        write(path, doc(path, title, p["corta"], page_programa(p), "programas")); urls.append(path)
    # 404
    io.open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(
        doc("/404", "Página no encontrada — BuildUp", "Esta página no existe.",
            '<section class="section" style="padding:120px 0"><div class="wrap" style="text-align:center">'
            '<p class="section-kicker">Error 404</p><h2 class="h-section">Esta página no existe</h2>'
            '<div class="center" style="margin-top:34px"><a href="/" class="btn">Volver al inicio</a></div></div></section>'))
    io.open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % S["dominio"])
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append("  <url><loc>%s%s</loc></url>" % (S["dominio"], u))
    sm.append("</urlset>")
    io.open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
    print("Generadas %d páginas en %s/" % (len(urls) + 1, OUT))

if __name__ == "__main__":
    main()
