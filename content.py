# -*- coding: utf-8 -*-
"""CONTENIDO DEL SITIO getbuildup.app

Este es el unico archivo que hace falta tocar para cambiar textos, precios,
programas, recetas o preguntas frecuentes. Al guardar un cambio aqui, la web
se regenera y se publica sola en un minuto.

TRES REGLAS para no romper nada:

  1. Cambia SOLO lo que esta entre comillas.
     Bien:  "importe": "$179.99"
     Mal:   "importe" : $179.99     <- sin comillas, rompe

  2. No borres comas, corchetes [ ] ni llaves { }.

  3. Si un texto lleva comillas por dentro, usa comillas simples:
     "corta": "Lo que llaman 'busy girls'"

Si algo se rompe, NO pasa nada: la publicacion falla y la web se queda
como estaba. Nunca se cae. Avisame y lo arreglo.
"""

SITE = {
    "nombre": "BuildUp",
    "dominio": "https://getbuildup.app",
    "empresa": "Maria Gabs Fitness LLC",
    "coach": "María Gabriela",
    "email_general": "team@mariagabsfitness.com",
    "email_soporte": "buildup@mariagabsfitness.com",
    "horario": "Lun – Vie | 9:00 – 17:00",
    "instagram": "#",
    "tiktok": "#",
    "prighter_portal": "https://app.prighter.com/portal/13541273953",
    "prighter_fecha": "2026-10-27",
}

PRECIOS = {
    "anual": {"importe": "$179.99", "periodo": "por año", "mensualizado": "$15.00",
              "renovacion": "se renueva cada 12 meses", "cinta": "Ahorra 40%"},
    "mensual": {"importe": "$24.99", "periodo": "por mes",
                "renovacion": "Se renueva cada mes"},
    "prueba_dias": 7,
}

PROGRAMAS = [
    {
        "slug": "build-shred", "nombre": "Build & Shred", "disponible": True,
        "enfoque_linea": "Tren inferior · Fuerza y resistencia",
        "nivel": "Intermedio · Avanzado",
        "corta": "Gana masa muscular, definición y resistencia. Fuerza intensa y cardio, con mayor enfoque en tren inferior.",
        "badges": ["GYM", "CASA", "3 / 4 / 5 / 6 días", "FUERZA", "HIPERTROFIA", "RESISTENCIA"],
        "intro": [
            "Un programa de entrenamiento estructurado para trabajar todo el cuerpo, desarrollar masa muscular, reducir grasa y mejorar tu fuerza y resistencia.",
            "Ya sea que entrenes en el gimnasio o en casa, cada sesión está diseñada para desafiarte, ayudarte a superar tus límites y mantener una progresión constante.",
            "Cada día empieza con una rutina de abdominales de ~10 minutos, sigue con el entrenamiento de fuerza (ejercicios solos y supersets) y termina con opciones de cardio a tu nivel.",
        ],
        "enfoque": ["Tren inferior principalmente", "Tren superior y abdomen", "Fuerza y resistencia"],
        "incluye": ["Plan de entrenamiento de 8 semanas", "Splits de 3, 4, 5 y 6 días",
                    "Registro de progreso (pesos y reps)", "Versión gym y versión en casa",
                    "Alternativas para cada ejercicio", "Entrenamiento de abdominales estructurado",
                    "Recomendaciones de cardio"],
        "versiones": ["1.0", "2.0", "3.0", "4.0", "5.0", "6.0"],
        "splits": [["3", "días", "2 tren inferior · 1 tren superior"],
                   ["4", "días", "2 tren inferior · 2 tren superior"],
                   ["5", "días", "3 tren inferior · 2 tren superior"],
                   ["6", "días", "3 inferior · 2 superior · 1 cardio y abs"]],
        "entrenos": ["Glúteo (upper glutes)", "Hombros, bíceps y pecho", "Cuádriceps y glúteos", "Espalda, tríceps y pecho"],
    },
    {
        "slug": "build-sculpt", "nombre": "Build & Sculpt", "disponible": True,
        "enfoque_linea": "Tren superior · Definición", "nivel": "Intermedio",
        "corta": "Esculpe tu cuerpo, construye masa muscular y definición, con mayor enfoque en tren superior.",
        "badges": ["GYM", "CASA", "3 / 4 / 5 días"],
        "intro": [
            "Build & Sculpt está construido alrededor del tren superior: espalda, hombros, brazos y core, sin dejar de trabajar piernas y glúteos para mantener el equilibrio.",
            "El objetivo es forma y definición: rangos de repeticiones más altos, control del tempo y trabajo de aislamiento para dar detalle al músculo que ya construiste.",
            "Igual que el resto de programas, cada ciclo dura 8 semanas y registra tus pesos y repeticiones para aplicar sobrecarga progresiva.",
        ],
        "enfoque": ["Tren superior principalmente", "Glúteos y piernas de soporte", "Definición y control"],
        "incluye": ["Plan de entrenamiento de 8 semanas", "Splits de 3, 4 y 5 días",
                    "Registro de progreso (pesos y reps)", "Versión gym y versión en casa",
                    "Alternativas para cada ejercicio", "Bloques de core y estabilidad",
                    "Recomendaciones de cardio"],
        "versiones": ["1.0", "2.0"],
        "splits": [["3", "días", "2 tren superior · 1 tren inferior"],
                   ["4", "días", "2 tren superior · 2 tren inferior"],
                   ["5", "días", "3 tren superior · 2 tren inferior"],
                   ["+", "cardio", "Opciones LISS y HIIT al final de cada sesión"]],
        "entrenos": ["Espalda y bíceps", "Hombro y tríceps", "Pecho y core", "Glúteos y femoral"],
    },
    {
        "slug": "buildxpress", "nombre": "BuildXpress", "disponible": True,
        "enfoque_linea": "45–50 minutos · Cuerpo completo", "nivel": "Todos los niveles",
        "corta": "Rutinas rápidas de 45–50 minutos para ganar músculo y definir. Para las busy girls con poco tiempo.",
        "badges": ["GYM", "CASA", "45–50 MIN"],
        "intro": [
            "BuildXpress comprime el entrenamiento en 45–50 minutos sin perder el estímulo: menos ejercicios, más densidad y supersets bien elegidos.",
            "Pensado para las semanas en las que la agenda manda. Entras, sigues la rutina en el orden indicado y sales.",
            "Mantiene el registro de pesos y repeticiones, así que aunque entrenes menos tiempo sigues midiendo tu progreso.",
        ],
        "enfoque": ["Cuerpo completo por sesión", "Densidad y supersets", "Mínimo tiempo, máximo estímulo"],
        "incluye": ["Plan de entrenamiento de 8 semanas", "Splits de 3, 4 y 5 días",
                    "Sesiones de 45–50 minutos", "Registro de progreso (pesos y reps)",
                    "Versión gym y versión en casa", "Alternativas para cada ejercicio",
                    "Cardio opcional corto"],
        "versiones": ["1.0", "2.0"],
        "splits": [["3", "días", "Full body con énfasis rotativo"],
                   ["4", "días", "2 inferior · 2 superior"],
                   ["5", "días", "3 inferior · 2 superior"],
                   ["50", "min máx", "Cada sesión está cronometrada dentro de la app"]],
        "entrenos": ["Full body express", "Glúteos en 45'", "Superior en 45'", "Core y cardio"],
    },
    {
        "slug": "buildonthego", "nombre": "BuildOnTheGo", "disponible": False,
        "enfoque_linea": "Sin equipo · Peso corporal", "nivel": "Todos los niveles",
        "corta": "Programa de viaje con rutinas rápidas y sin equipo, usando solo peso corporal. Para seguir entrenando estés donde estés.",
        "badges": ["SIN EQUIPO", "VIAJE", "20–35 MIN"],
        "intro": [
            "BuildOnTheGo existe para las semanas fuera de casa: hotel, casa de tus papás, vacaciones. Cero equipo, cero excusas.",
            "Cada sesión usa solo peso corporal y se completa en 20 a 35 minutos, en el espacio de una alfombra.",
            "No sustituye a tu programa principal: es el puente que evita que pierdas el ritmo mientras viajas.",
        ],
        "enfoque": ["Solo peso corporal", "Sesiones cortas", "Mantener el hábito en viaje"],
        "incluye": ["Rutinas de 20–35 minutos", "Cero equipo necesario",
                    "Progresiones y regresiones por ejercicio", "Bloques de core",
                    "Opciones de cardio sin impacto", "Se adapta a cualquier espacio"],
        "versiones": ["1.0"],
        "splits": [["3", "días", "Full body con peso corporal"],
                   ["4", "días", "Alterna inferior y superior"],
                   ["20", "min mín", "La sesión más corta del programa"],
                   ["0", "equipo", "Ni una banda ni una mancuerna"]],
        "entrenos": ["Full body sin equipo", "Glúteos en el cuarto", "Core de viaje", "Cardio sin impacto"],
    },
    {
        "slug": "buildginner", "nombre": "BuildGinner", "disponible": False,
        "enfoque_linea": "Principiantes · Técnica y bases", "nivel": "Principiante",
        "corta": "Programa para principiantes: rutinas guiadas paso a paso para iniciar tu camino fitness con confianza y bases sólidas.",
        "badges": ["GYM", "CASA", "3 / 4 días"],
        "intro": [
            "Si nunca has entrenado con pesas o llevas mucho tiempo fuera, este es el punto de partida.",
            "BuildGinner enseña primero el movimiento: cada ejercicio viene con video, señales de técnica y una progresión clara antes de subir la carga.",
            "En 8 semanas construyes la base de fuerza y el hábito que necesitas para pasar a Build & Shred o Build & Sculpt.",
        ],
        "enfoque": ["Técnica antes que carga", "Patrones básicos de fuerza", "Construir el hábito"],
        "incluye": ["Plan de entrenamiento de 8 semanas", "Splits de 3 y 4 días",
                    "Video y señales de técnica en cada ejercicio", "Progresión de carga guiada",
                    "Versión gym y versión en casa", "Glosario de términos del gym",
                    "Recomendaciones de cardio suave"],
        "versiones": ["1.0"],
        "splits": [["3", "días", "Full body de aprendizaje"],
                   ["4", "días", "2 inferior · 2 superior"],
                   ["8", "semanas", "Un ciclo completo de adaptación"],
                   ["→", "siguiente", "Salida natural hacia Build & Shred"]],
        "entrenos": ["Sentadilla paso a paso", "Empuje básico", "Tracción básica", "Core para empezar"],
    },
    {
        "slug": "hyroxready", "nombre": "HyroxReady", "disponible": False,
        "enfoque_linea": "Competencia · Fuerza y resistencia", "nivel": "Intermedio · Avanzado",
        "corta": "Prepárate para HYROX con fuerza, resistencia y trabajo específico de competencia.",
        "badges": ["GYM", "CASA", "HÍBRIDO"],
        "intro": [
            "HyroxReady combina fuerza pesada con trabajo de resistencia y las estaciones específicas de la competencia.",
            "Cada semana mezcla bloques de fuerza, intervalos de carrera y simulaciones de estación (trineo, burpees, wall balls, farmer carry).",
            "El plan te lleva de la base a la semana de competencia con una descarga programada.",
        ],
        "enfoque": ["Fuerza aplicada", "Resistencia y carrera", "Estaciones de competencia"],
        "incluye": ["Plan de entrenamiento por bloques", "Simulaciones de estación",
                    "Intervalos de carrera estructurados", "Registro de progreso (pesos y reps)",
                    "Versión gym y versión en casa", "Semana de descarga previa a competencia",
                    "Guía de ritmo y transiciones"],
        "versiones": ["1.0"],
        "splits": [["4", "días", "2 fuerza · 2 híbrido"],
                   ["5", "días", "2 fuerza · 2 híbrido · 1 carrera"],
                   ["8", "estaciones", "Trabajo específico de la competencia"],
                   ["1", "descarga", "Semana ligera antes del evento"]],
        "entrenos": ["Fuerza pesada", "Intervalos de carrera", "Simulación de estaciones", "Core y transiciones"],
    },
]

# Las 42 recetas reales de la app (nombre, categoria, kcal, proteina, carbos, grasas, fibra)
RECETAS = [
    ("Arepa crunch de avena","desayuno",444,46,36,12,12),("Panquecas de zanahoria","desayuno",419,48,47,3,6),
    ("Tostadas francesas","desayuno",425,37,35,15,4),("Avocado toast","desayuno",442,33,39,18,9),
    ("Protein cereal","desayuno",535,50,43,16,5),("Panquecas carb smart","desayuno",444,44,24,18,4),
    ("Savory french toast","desayuno",409,35,31,15,4),("Panquecas de banana","desayuno",537,52,48,16,6),
    ("Cottage avotoast","desayuno",465,34,49,18,9),("Protein greek oats","desayuno",518,50,36,20,9),
    ("Salmon platter","almuerzo",452,31,47,15,8),("Tacos con pavo molido","almuerzo",480,34,33,20,7),
    ("Tacos tunacado","almuerzo",384,26,31,18,7),("Arroz con pollo","almuerzo",298,31,37,2,3),
    ("Arroz frito con pavo","almuerzo",309,34,37,2,5),("Tuna pasta","almuerzo",317,24,42,8,7),
    ("Mango sushi","almuerzo",470,34,28,27,7),("Tuna poke bowl","almuerzo",343,31,36,7,4),
    ("Burger 328 cal","almuerzo",328,35,33,7,5),("Tacos de lechuga","almuerzo",332,35,16,14,7),
    ("Wrap de pollo","almuerzo",394,42,25,16,8),("Salmon y esparragos","cena",245,29,6,12,4),
    ("Cilantro lime chicken","cena",341,31,16,18,7),("Smart sushi","cena",393,36,18,21,7),
    ("Botes de atun","cena",270,23,10,15,4),("Mahi mahi en salsa","cena",380,27,21,22,9),
    ("Shrimp con cauliflower rice","cena",383,41,14,17,5),("Fish bowl","cena",303,25,27,9,3),
    ("Ceviche mahi mahi","cena",341,26,28,14,6),("Tuna nori wrap","cena",293,25,12,16,5),
    ("Tartar salmon tacos","cena",309,29,8,17,5),("Chocolate yogurt bowl","merienda",195,25,18,3,3),
    ("Tuna ricecakes","merienda",276,24,21,10,4),("Helado pie de limon","merienda",295,51,12,4,1),
    ("Pepino tuna sandwich","merienda",227,24,15,8,2),("Fresas con crema","merienda",146,26,10,0,3),
    ("Cottage crackers","merienda",170,17,23,3,4),("Chocolate mugcake","merienda",288,25,25,10,4),
    ("Omelette proteica","merienda",148,23,10,2,2),("Batido proteina y colageno","merienda",143,23,4,3,1),
    ("Helado de proteina","merienda",120,25,1,0,1),("Baked apple yogurt","merienda",190,16,28,2,4),
]

# Las 5 que se muestran como vistazo en Home y en Nutricion
VISTAZO = ["Arepa crunch de avena","Tuna poke bowl","Cilantro lime chicken","Protein greek oats","Chocolate mugcake"]

TESTIMONIOS = [
    ("Llevo tres versiones de Build & Shred y por primera vez veo progresión real en los pesos. El registro dentro de la app lo cambia todo.", "Ana · Build & Shred 4.0"),
    ("Entreno a las 5:30 am antes del trabajo. BuildXpress me salvó: 45 minutos y salgo con la sensación de haber entrenado completo.", "Cami · BuildXpress"),
    ("Nunca había pisado un gym. Empecé con las rutinas guiadas y hoy hago sentadilla con barra sin miedo.", "Vale · Primeras 8 semanas"),
]

FAQS = [
    ("¿Todos los programas están incluidos en mi membresía?",
     "Sí. Con tu membresía tienes acceso a todos los programas y a todas sus versiones, y puedes cambiar de uno a otro cuando quieras."),
    ("¿Cuánto dura cada programa?",
     "Cada versión es un ciclo completo de 8 semanas. Al terminarla pasas a la siguiente, con nuevos ejercicios y variantes para seguir progresando y evitar el estancamiento."),
    ("¿Cuántos días a la semana tengo que entrenar?",
     "Tú eliges. Cada programa tiene splits de 3, 4, 5 o 6 días, y seleccionas el tuyo al empezar según el tiempo que tengas."),
    ("¿Puedo hacer los programas en casa?",
     "Sí. Todos los programas tienen versión gym y versión en casa, y eliges dónde entrenas en el cuestionario inicial. Si elegiste gym pero un día quieres entrenar en casa, puedes cambiarlo desde tu entrenamiento del día."),
    ("¿Puedo reorganizar mi semana?",
     "Sí. Con ORDENAR acomodas los entrenamientos de la semana según los días que mejor te funcionen, sin perder el orden del programa."),
    ("¿Qué incluye cada entrenamiento?",
     "Calentamiento y abdominales, el bloque de fuerza con series, repeticiones y descansos, y opciones de cardio al final. Cada ejercicio trae video, alternativas y Modo guiado para seguirlo paso a paso."),
    ("¿Qué pasa cuando termino un programa?",
     "Marcas el programa como completado, guardas tu progreso y eliges qué sigue: la siguiente versión del mismo programa u otro distinto."),
    ("Soy principiante, ¿por dónde empiezo?",
     "Dentro de la app hay una guía rápida que te recomienda el programa según tus objetivos, tu nivel y los días que puedas entrenar."),
    ("¿La nutrición está incluida?",
     "Sí. SmartFuel viene incluido: cálculo de tus calorías y macros, plan de alimentación, recetario completo y el registro diario de comidas."),
    ("¿Puedo cancelar cuando quiera?",
     "Sí. Empiezas con 7 días gratis y cancelas cuando quieras desde tu cuenta."),
]

_LEG = "https://mariagabsfitness.com/pages/"
LEGAL_ES = [("Términos de servicio","terminos"),("Política de privacidad","privacidad"),
            ("Privacidad de datos de salud","privacidad-salud"),("Consentimiento de datos de salud","consentimiento-datos-salud"),
            ("Aviso de salud y nutrición","aviso-salud"),("Normas de BuildFam","normas-comunidad"),
            ("Eliminar cuenta y datos","borrar-cuenta")]
LEGAL_EN = [("Terms of Service","terms-en"),("Privacy Policy","privacy-en"),
            ("Health Data Privacy","health-data-privacy-en"),("Health Data Consent","health-data-consent-en"),
            ("Health &amp; Nutrition Notice","health-notice-en"),("BuildFam Guidelines","community-guidelines-en"),
            ("Delete Account &amp; Data","delete-account-en")]
def legal_url(slug): return _LEG + slug
