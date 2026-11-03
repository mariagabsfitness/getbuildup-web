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

# ---------------------------------------------------------------- pagos
# activo=False -> el boton de "crear cuenta" sigue llevando a /listo/ sin cobrar.
#                 Para probar el cobro de verdad sin exponerlo al publico,
#                 abre /crear-cuenta/?pago=prueba
# Cuando Paddle apruebe la cuenta de produccion, se cambia rc_api_key por la
# clave de produccion y se pone activo=True. Nada mas cambia.
PAGO = {
    "activo": False,
    "rc_api_key": "pdl_ipkHDTDyCXEIJgZjsTHzfbwIoJWg",   # sandbox
    "entitlement": "acceso",
    "firebase": {
        "apiKey": "AIzaSyBKMmf-LA-4OIAfi2ptCiemva7AEDE2ego",
        "authDomain": "buildup-40951.firebaseapp.com",
        "projectId": "buildup-40951",
        "appId": "1:869364925842:web:d78fc11ef48bf437ce2d4b",
    },
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
        "enfoque_linea": "Ganancia muscular · Fuerza · Definición · Resistencia",
        "nivel": "Intermedio · Avanzado",
        "corta": "Gana masa muscular, definición y resistencia, con fuerza intensa y cardio.",
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
    },
    {
        "slug": "build-sculpt", "nombre": "Build & Sculpt", "disponible": True,
        "enfoque_linea": "Ganancia muscular · Fuerza · Definición", "nivel": "Intermedio · Avanzado",
        "corta": "Construye músculo y define con entrenamiento de pesas, sin movimientos funcionales ni HIIT dentro de las rutinas.",
        "badges": ["GYM", "CASA", "3 / 4 / 5 / 6 días", "FUERZA", "HIPERTROFIA"],
        "intro": [
            "Un programa de entrenamiento estructurado para trabajar todo el cuerpo, desarrollar masa muscular, mejorar tu fuerza y esculpir tu físico a través de entrenamientos enfocados principalmente en pesas.",
            "A diferencia de Build & Shred, Build & Sculpt tiene un enfoque más directo en fuerza e hipertrofia: no incorpora movimientos funcionales ni de estilo HIIT dentro de las rutinas de pesas.",
            "Ya sea que entrenes en el gimnasio o en casa, cada sesión está diseñada para ayudarte a progresar en tus ejercicios, mejorar tu técnica y aumentar gradualmente tu fuerza y rendimiento.",
        ],
        "enfoque": ["Desarrollo de masa muscular", "Glúteos y tren inferior",
                    "Tren superior y abdomen", "Fuerza e hipertrofia"],
        "incluye": ["Plan de entrenamiento de 8 semanas", "Splits de 3, 4, 5 y 6 días",
                    "2 días principales de tren inferior", "Registro de progreso (pesos y reps)",
                    "Versión gym y versión en casa", "Alternativas para diferentes ejercicios",
                    "Entrenamiento de abdominales estructurado", "Recomendaciones de cardio"],
        "versiones": ["1.0"],
        "splits": [["3", "días", "2 tren inferior · 1 tren superior"],
                   ["4", "días", "2 tren inferior · 2 tren superior"],
                   ["5", "días", "2 tren inferior · 3 tren superior"],
                   ["6", "días", "2 tren inferior · 3 tren superior · 1 abdomen y cardio"]],
    },
    {
        "slug": "buildxpress", "nombre": "BuildXpress", "disponible": True,
        "enfoque_linea": "Ganancia muscular · Fuerza · Definición · Rutinas express", "nivel": "Intermedio · Avanzado",
        "corta": "Entrenamientos eficientes de unos 45 minutos para ganar músculo y fuerza, con una estructura completa.",
        "badges": ["GYM", "CASA", "3 / 4 / 5 / 6 días", "45 MIN", "FUERZA", "HIPERTROFIA"],
        "intro": [
            "Un programa de entrenamiento diseñado para ayudarte a desarrollar masa muscular, ganar fuerza y trabajar todo el cuerpo con sesiones más cortas, eficientes y estructuradas.",
            "BuildXpress mantiene los principios de un programa completo de fuerza e hipertrofia, pero con una selección estratégica de ejercicios, supersets y tiempos de descanso más controlados para que puedas completar tus entrenamientos en aproximadamente 45 minutos.",
            "Menos tiempo no significa menos intención: cada ejercicio está seleccionado para aprovechar al máximo cada sesión y permitirte seguir progresando en pesos, repeticiones y rendimiento.",
        ],
        "enfoque": ["Entrenamientos eficientes de unos 45 minutos", "Desarrollo de masa muscular",
                    "Glúteos y tren inferior", "Tren superior y abdomen", "Fuerza y progresión"],
        "incluye": ["Plan de entrenamiento de 8 semanas", "Splits de 3, 4, 5 y 6 días",
                    "Sesiones estructuradas para realizarse en unos 45 minutos",
                    "Registro de progreso (pesos y reps)", "Versión gym y versión en casa",
                    "Alternativas para diferentes ejercicios",
                    "Entrenamiento de abdominales estructurado", "Recomendaciones de cardio"],
        "versiones": ["1.0"],
        "splits": [["3", "días", "2 tren inferior · 1 tren superior"],
                   ["4", "días", "2 tren inferior · 2 tren superior"],
                   ["5", "días", "3 tren inferior · 2 tren superior"],
                   ["6", "días", "3 tren inferior · 2 tren superior · 1 abdomen y cardio"]],
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

# Testimonios REALES. La foto de cada uno es testimonio-1.jpg, testimonio-2.jpg...
# en el mismo orden de esta lista. Si quitas uno, quita tambien su foto.
TESTIMONIOS = [
    ("Los entrenamientos me encantan porque son retadores: salgo sintiendo que de verdad trabajé. Amo la dieta, no me da ansiedad, tengo buen ánimo siempre y duermo súper bien. Y aparte del cambio físico, el de la piel y el pelo también es una locura. Este estilo de vida lo aprendí con BuildUp y me lo voy a quedar, porque me encanta cómo me siento.",
     "Olga · Build & Shred"),
    ("Empecé a entrenar con BuildUp después de mis primeros dos hijos, antes de que fuera una app, y fue de las mejores decisiones que tomé. Luego llegó mi tercer bebé y tocó empezar de nuevo, con una rutina completamente distinta 😂. Hoy, un año y medio después, me siento más fuerte y feliz con mis resultados. Aprendí a hacer del entrenamiento parte de mi vida, incluso en medio del caos de ser mamá de tres. ¡Y vamos por más! ❤️",
     "María B · Build & Sculpt"),
    ("Hace 10 años, antes de conocer el fitness, el entrenamiento y la alimentación, mi pensamiento de veinteañera era operarme las bubis y quitarme dos costillas, jajaja, porque sentía que mi cuerpo no tenía forma. Bastó empezar a entrenar y cambiar mi alimentación para ver el cambio que siempre quise. No tenía idea de que la solución era entrenar con un programa estructurado y comer saludable según mi cuerpo y mi objetivo.",
     "María Gabriela · Build & Shred"),
]

# Los 4 entrenamientos de ejemplo que se ven en TODAS las páginas de programa.
# Son una muestra del Modo guiado, no la semana de un programa concreto.
# Cambia los nombres aquí y renombra los archivos de video/miniatura igual.
ENTRENOS_DEMO = [
    "Glúteo (upper glutes)",
    "Espalda y hombros",
    "Cuádriceps y glúteos",
    "Espalda y tríceps",
]

FAQS_PROGRAMA = {
    "build-shred": [
        ("¿Para quién es Build & Shred?",
         "Para quienes disfrutan los entrenamientos más retadores. Combina el trabajo de pesas con movimientos funcionales y de estilo HIIT dentro de las rutinas, así que además de ganar masa muscular y reducir grasa, mejoras tu resistencia cardiovascular y tu condición física general. Es el programa de las que quieren convertirse en máquinas."),
        ("¿En qué se diferencia de Build & Sculpt?",
         "Build & Shred incorpora movimientos funcionales y de alta intensidad dentro de los entrenamientos de pesas, con mayor enfoque en tren inferior. Build & Sculpt es entrenamiento de pesas más directo, centrado en fuerza e hipertrofia, sin ese componente funcional."),
        ("¿Qué nivel necesito?",
         "Está pensado para nivel intermedio y avanzado. Si vienes de cero, puedes empezar por la versión en casa y usar las alternativas de cada ejercicio para adaptar la intensidad."),
        ("¿Necesito gimnasio?",
         "No. Cada entrenamiento tiene versión gym y versión en casa, con alternativas para diferentes ejercicios."),
        ("¿Por qué tiene seis versiones?",
         "Cada versión es un ciclo completo de 8 semanas. Build & Shred 6.0 es la más reciente. Al terminar una versión pasas a la siguiente, con nuevos ejercicios y variantes que te ayudan a seguir progresando y evitar el estancamiento."),
    ],
    "build-sculpt": [
        ("¿Para quién es Build & Sculpt?",
         "Para quienes quieren enfocarse principalmente en desarrollar músculo, ganar fuerza y trabajar su composición corporal con una estructura de entrenamiento basada en pesas. Se recomienda especialmente si tienes un metabolismo rápido y te cuesta ganar masa muscular: al no incluir tantos movimientos funcionales ni HIIT dentro de las rutinas, el gasto de cada sesión es menor y la energía se concentra en construir músculo."),
        ("¿En qué se diferencia de Build & Shred?",
         "Build & Sculpt tiene un enfoque más directo en fuerza e hipertrofia y no incorpora movimientos funcionales ni de estilo HIIT dentro de las rutinas de pesas. Build & Shred sí los incluye, y por eso trabaja más la resistencia y la condición física."),
        ("¿Incluye cardio?",
         "El cardio no va dentro de las rutinas de pesas. Encontrarás recomendaciones de cardio aparte, para que elijas cuándo y cuánto hacer según tu objetivo."),
        ("¿Necesito gimnasio?",
         "No. Cada entrenamiento tiene versión gym y versión en casa, con alternativas para diferentes ejercicios."),
        ("¿Qué nivel necesito?",
         "Intermedio y avanzado. Cada sesión está diseñada para que progreses en tus ejercicios, mejores tu técnica y aumentes gradualmente tu fuerza y rendimiento."),
    ],
    "buildxpress": [
        ("¿Para quién es BuildXpress?",
         "Para quienes quieren seguir entrenando con una estructura completa y progresiva, pero necesitan sesiones más cortas. Ideal si tienes poco tiempo y no quieres sacrificar un entrenamiento bien estructurado."),
        ("¿Cuánto dura cada sesión?",
         "Aproximadamente 45 minutos. Se logra con una selección estratégica de ejercicios, supersets y tiempos de descanso más controlados."),
        ("Si entreno menos tiempo, ¿progreso menos?",
         "No. BuildXpress mantiene los principios de un programa completo de fuerza e hipertrofia y el registro de pesos y repeticiones, así que sigues aplicando sobrecarga progresiva sesión a sesión."),
        ("¿Necesito gimnasio?",
         "No. Cada entrenamiento tiene versión gym y versión en casa, con alternativas para diferentes ejercicios."),
        ("¿Qué nivel necesito?",
         "Intermedio y avanzado."),
    ],
}

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

_LEG = "/legal/"
LEGAL_ES = [("Términos de servicio","terminos"),("Política de privacidad","privacidad"),
            ("Privacidad de datos de salud","privacidad-salud"),("Consentimiento de datos de salud","consentimiento-datos-salud"),
            ("Aviso de salud y nutrición","aviso-salud"),("Normas de BuildFam","normas-comunidad"),
            ("Eliminar cuenta y datos","borrar-cuenta"),("Política de reembolsos","reembolsos")]
LEGAL_EN = [("Terms of Service","terms-en"),("Privacy Policy","privacy-en"),
            ("Health Data Privacy","health-data-privacy-en"),("Health Data Consent","health-data-consent-en"),
            ("Health &amp; Nutrition Notice","health-notice-en"),("BuildFam Guidelines","community-guidelines-en"),
            ("Delete Account &amp; Data","delete-account-en"),("Refund Policy","refunds-en")]
def legal_url(slug): return _LEG + slug + "/"
