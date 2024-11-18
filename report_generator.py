from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import json
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import Optional  # Importar Optional para campos opcionales

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class ReportSection(BaseModel):
    Rating: str
    Comment: str

# Definir el modelo principal ReportModel con Nota_de_prueba_escrita como campo opcional
class ReportModel(BaseModel):
    Motivación_y_Participación: ReportSection
    Aprendizaje: ReportSection
    Comportamiento: ReportSection
    Nota_de_prueba_oral: str  # Solo se necesita el comentario
    Nota_de_prueba_escrita: str  # Solo para B&B y tweens
    Evaluación_general: str    # Solo se necesita el comentario

llm4o = ChatOpenAI(model="gpt-4o")
llm4o_mini = ChatOpenAI(model="gpt-4o-mini")

def generar_reporte(student):
    print(student)
    print(student.student_name)

    # Determinar si la categoría del estudiante incluye prueba escrita
    courses_with_written_test = ['B&B', 'Tweens']
    include_written_test = student.category in courses_with_written_test

    dod = '''1. Personaliza el informe y refleja el carácter y estilo de aprendizaje del estudiante.
2. Cada sección debe tener al menos 300 caracteres.
3. Usa el nombre del estudiante al menos una vez en cada sección, no uses los apellidos.
4. Incluye ejemplos de actividades que el estudiante disfruta y estructuras de inglés que ha aprendido.
5. Las frases aprendidas en inglés entre comillas y las traducciones seguidas en español entre paréntesis (Solo las frases aprendidas que estén en inglés deben ser traducidas entre paréntesis, nada más entre paréntesis.).
6. Asegúrate de que el informe refleje con precisión el progreso, carácter y aptitudes del estudiante.
7. Escribe en tercera persona, evitando declaraciones en primera persona.
8. Enfócate en información relevante para el rendimiento en clase, evitando comentarios demasiado personales.
9. Sé tacto al abordar problemas, siempre proponiendo soluciones.
10. Asegúrate de que la evaluación (excelente, muy bien, bien, satisfactorio, deficiente) coincida con el contenido escrito. No hables de la nota concreta, solo justifícala.
11. Usa lenguaje positivo y propone soluciones al abordar problemas.
12. Para el informe final del año, incluye una evaluación general y recomendaciones de práctica para el verano.
13. Para las clases de Babies, enfócate en las reacciones e indicadores de comprensión.
14. Para las clases de T&T, aborda el comportamiento, hábitos de trabajo y rendimiento en todas las habilidades.
15. No menciones verano o otros tiempos del año ya que no sabes en que trimestre está el alumno, tampoco menciones que no lo sabes.'''

    descripcion_tarea = f"""
Escribe un informe detallado para el estudiante basado en sus datos de rendimiento, sin inventar datos.
Sigue estas pautas de la Definición de Hecho:
{dod}

Motivación y Participación for rating: {student.motivation_rating}
Aprendizaje for rating: {student.learning_rating}
Comportamiento for rating: {student.behavior_rating}

**Formato de Salida:**
{{
    "Motivación_y_Participación": {{
        "Rating": "Excellent/Very good/Good/Satisfactory",
        "Comment": "<Detailed comment>"
    }},
    "Aprendizaje": {{
        "Rating": "Excellent/Very good/Good/Satisfactory",
        "Comment": "<Detailed comment>"
    }},
    "Comportamiento": {{
        "Rating": "Excellent/Very good/Good/Satisfactory",
        "Comment": "<Detailed comment>"
    }},
    "Nota_de_prueba_oral": "<Detailed comment>",
    {"\"Nota_de_prueba_escrita\": \"<Detailed comment>\"," if include_written_test else ""}
    "Evaluación_general": "<Detailed comment>"
}}

**
Esto es solo un ejemplo para que tengas una idea, el lenguaje debe ser claro y común, redacta fácil en castellano de españa, *cambia la estructura y contenido*:
{{
    "Motivación_y_Participación": {{
        "Rating": "Very good",
        "Comment": "Elisa muestra una participación activa y entusiasta en clase. Se destaca por su energía positiva, entrando siempre con entusiasmo que contagia a sus compañeros. Aunque a veces puede dispersarse, Elisa compensa esto con una notable disposición para iniciar actividades, especialmente aquellas que implican explorar nuevos términos en inglés. Se siente particularmente atraída por actividades grupales, donde puede interactuar y compartir ideas con su grupo de amigos. Su carácter extrovertido y curioso la distingue como una presencia vibrante en cada sesión."
    }},
    "Aprendizaje": {{
        "Rating": "Very good",
        "Comment": "Elisa ha demostrado una buena comprensión de las estructuras básicas del inglés, utilizando frases como \\\"I like to play with my friends\\\" (Me gusta jugar con mis amigos). Aunque su uso de palabras clave ha sido adecuado, hay margen para el fortalecimiento de estructuras complejas y la expansión de su vocabulario. Elisa no duda en formular preguntas cuando encuentra dificultades, lo que refleja su constructiva curiosidad. Continúa esforzándose por comunicarse en inglés y su pronunciación ha mejorado notablemente. Un enfoque más centrado en la práctica oral y auditiva la beneficiaría aún más."
    }},
    "Comportamiento": {{
        "Rating": "Excellent",
        "Comment": "El comportamiento de Elisa en clase es ejemplar. Respeta los turnos de palabra de manera consistente y demuestra gran colaboración con sus compañeros, lo que provoca un entorno armónico y productivo. Su capacidad para ayudar a sus compañeros y colaborar con la profesora, como cuando organiza materiales, es uno de sus puntos más destacados. Elisa sigue las instrucciones con precisión y cuida el material con esmero, manteniendo siempre en mente el bienestar común de su grupo de estudio. Esta actitud positiva y cooperativa la convierte en un miembro indispensable para su grupo de clase."
    }},
    "Nota_de_prueba_oral": "Aunque los datos de la prueba oral de Elisa no están disponibles, su creciente habilidad para articular sus pensamientos en inglés sugiere que está progresando bien en esta área. Se recomienda continuar practicando inglés conversacional, permitiéndole ganar más confianza en sus habilidades orales.",
    {"\"Nota_de_prueba_escrita\": \"Elisa ha demostrado un sólido desempeño en la prueba escrita, evidenciando su comprensión de las estructuras gramaticales y vocabulario aprendido durante el curso. Sería beneficioso que continuara practicando la escritura en inglés para consolidar sus habilidades.\"," if include_written_test else ""}
    "Evaluación_general": "El rendimiento general de Elisa durante este término ha sido notable. Su comportamiento proactivo y positivo se traduce directamente en sus experiencias de aprendizaje. Se evidencia un buen uso de estructuras básicas del inglés, aunque podría beneficiarse de más práctica en el uso de frases complejas y enriquecimiento de vocabulario. Sugiero que durante el verano, Elisa continúe exponiéndose al inglés mediante audiolibros y conversaciones con hablantes nativos. Con estas estrategias, Elisa podrá seguir desarrollando sus habilidades lingüísticas y mantener su entusiasmo por el idioma en el futuro académico."
}}
**

**Ahora, utilizando los datos proporcionados a continuación para el estudiante, genera el informe siguiendo el estilo del ejemplo anterior pero variando la estructura para evitar repeticiones.**

**Datos del estudiante: ESENCIAL QUE SOLO USES DATOS DE AQUÍ Y NO TE INVENTES NINGÚN DATO NO PRESENTE**
- Nombre: {student.student_name.split()[0]}
- Puntuación de prueba oral: {student.oral_test_score}
"""

    if include_written_test:
        
        descripcion_tarea += f"- Puntuación de prueba escrita: {student.written_test_score if student.written_test_score != 0 else 'no disponible de momento'}"

    descripcion_tarea += f"""- Entra contento a clase: {student.enters_happy}
- Actitud positiva: {student.positive_attitude}
- Entusiasmo: {student.enthusiasm}
- Toma iniciativa: {student.initiative}
- Dato diferenciador: {student.differentiator}
- Puntos a mejorar en comportamiento: {student.behavior_improvement_points}
- Puntos fuertes en comportamiento: {student.behavior_strong_points}
- Tiene amigos en clase: {student.has_friends_in_class}
- Se distrae: {student.gets_distracted}
- Colabora con compañeros: {student.collaborates_with_peers}
- Respeta turnos de palabra: {student.respects_turns}
- Cuida el material: {student.cares_for_materials}
- Acciones en caso de mal comportamiento: {student.misbehavior_action}
- Participa: {student.participates}
- Actividades preferidas: {student.preferred_activities}
- Buena pronunciación: {student.good_pronunciation}
- Se esfuerza por comunicarse en inglés: {student.efforts_to_communicate}
- Se expresa con seguridad: {student.confident_expression}
- Pregunta dudas: {student.asks_questions}
- Ayuda a la profe: {student.helps_teacher}
- Sigue instrucciones: {student.follows_instructions}
- Comprende: {student.understands}
- Usa palabras clave: {student.uses_keywords}
- Hace estructuras completas: {student.makes_complete_structures}
- Ejemplo de oraciones que hace en inglés (único al que le siguen paréntesis): {student.example_sentences}
- Puntos fuertes de rendimiento: {student.learning_strong_points}
- Puntos a mejorar en rendimiento: {student.learning_improvement_points}

- Deberes: {student.homework}

**Importante**:
- REDACTA LO MÁS HUMANO POSIBLE COMO UN BUEN PROFESOR
- Asegúrate de que el informe final esté en formato JSON válido.    
- Utiliza comillas dobles para las claves y los valores.
- Si necesitas incluir comillas dentro de un valor, escápalas usando \\\".

"""
    respuesta = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": descripcion_tarea}],
        response_format=ReportModel
    )

    # Extraer el contenido del informe
    informe = respuesta.choices[0].message.content

    try:
        # Convertir la respuesta a formato JSON si es válida
        report = json.loads(informe)
    except json.JSONDecodeError:
        # Manejar el caso donde la respuesta no es JSON válido
        print("Error: La respuesta no es JSON válido.")
        report = {}

    return report




class ReportModelTweens(BaseModel):
    Comportamiento: ReportSection
    Trabajo: ReportSection
    Rendimiento: ReportSection
    Nota_de_prueba_oral: str  # Solo se necesita el comentario
    Nota_de_prueba_escrita: str  # Incluida para "Tweens"
    Homework: str  # Añadido Homework sin calificación
    Evaluación_general: str    # Solo se necesita el comentario
    Global_Score: str  # Añadido Global Score sin calificación

'''bb lo detecta como'''

def generar_reporte_tweens(student):
    print(student)
    print(student.student_name)

    # Verificar si la categoría del estudiante es "Tweens"
    is_tweens = student.category.lower() == 'tweens'

    dod = '''1. Personaliza el informe y refleja el carácter y estilo de aprendizaje del estudiante.
    2. Cada sección debe tener al menos 300 caracteres.
    3. Usa el nombre del estudiante al menos una vez en cada sección, no uses los apellidos.
    4. Incluye ejemplos de actividades que el estudiante disfruta y estructuras de inglés que ha aprendido.
    5. Las frases aprendidas en inglés entre comillas y las traducciones seguidas en español entre paréntesis (Solo las frases aprendidas que estén en inglés deben ser traducidas entre paréntesis, nada más entre paréntesis.).
    6. Asegúrate de que el informe refleje con precisión el progreso, carácter y aptitudes del estudiante.
    7. Escribe en tercera persona, evitando declaraciones en primera persona.
    8. Enfócate en información relevante para el rendimiento en clase, evitando comentarios demasiado personales.
    9. Sé tacto al abordar problemas, siempre proponiendo soluciones.
    10. Asegúrate de que la evaluación (excellent, very good, good, satisfactory, poor) coincida con el contenido escrito. No hables de la nota concreta, solo justifícala.
    11. Usa lenguaje positivo y propone soluciones al abordar problemas.
    12. Para el informe final del año, incluye una evaluación general y recomendaciones de práctica para el verano.
    13. Para las clases de Babies, enfócate en las reacciones e indicadores de comprensión.
    14. Para las clases de T&T, aborda el comportamiento, hábitos de trabajo y rendimiento en todas las habilidades.
    15. No menciones verano o otros tiempos del año ya que no sabes en que trimestre está el alumno, tampoco menciones que no lo sabes.'''

    # Construir la parte inicial del prompt con las calificaciones
    descripcion_tarea = f"""
Escribe un informe detallado para el estudiante basado en sus datos de rendimiento, sin inventar datos.
Sigue estas pautas de la Definición de Hecho:
{dod}

Comportamiento rating: {student.behavior_rating}
Trabajo rating: {student.work_rating}
Rendimiento rating: {student.performance_rating}
"""

    # Formato de salida específico para "Tweens" incluyendo Homework y Global Score
    formato_salida = """
**Formato de Salida:**
{
    "Comportamiento": {
        "Rating": "Excellent/Very good/Good/Satisfactory/Poor",
        "Comment": "<Detailed comment>"
    },
    "Trabajo": {
        "Rating": "Excellent/Very good/Good/Satisfactory/Poor",
        "Comment": "<Detailed comment>"
    },
    "Rendimiento": {
        "Rating": "Excellent/Very good/Good/Satisfactory/Poor",
        "Comment": "<Detailed comment>"
    },
    "Nota_de_prueba_oral": "<Detailed comment>",
    "Nota_de_prueba_escrita": "<Detailed comment>",
    "Homework": "<Detailed comment>",
    "Evaluación_general": "<Detailed comment>",
    "Global_Score": "<Detailed comment>"
}
"""

    descripcion_tarea += formato_salida

    # Ejemplo de informe adaptado para "Tweens" incluyendo Homework y Global Score
    sample_report = """
**
Esto es solo un ejemplo para que tengas una idea, el lenguaje debe ser claro y común, redacta fácil en castellano de España, *cambia la estructura y contenido*:
{
    "Comportamiento": {
        "Rating": "Very good",
        "Comment": "Carlos ha demostrado un comportamiento ejemplar en clase. Siempre muestra una actitud positiva y colabora activamente con sus compañeros. Es respetuoso, sigue las instrucciones y contribuye a crear un ambiente de aprendizaje agradable."
    },
    "Trabajo": {
        "Rating": "Very good",
        "Comment": "Carlos participa de manera entusiasta en todas las actividades. Disfruta especialmente de las tareas grupales y siempre está dispuesto a ayudar. Su pronunciación ha mejorado y se esfuerza por comunicarse en inglés con seguridad."
    },
    "Rendimiento": {
        "Rating": "Very good",
        "Comment": "Carlos comprende bien los conceptos enseñados y es capaz de usar palabras clave y estructuras completas. Ha utilizado frases como \\\"I went to the park yesterday\\\" (Fui al parque ayer). Su progreso es notable."
    },
    "Nota_de_prueba_oral": "Carlos obtuvo una alta calificación en la prueba oral, demostrando fluidez y buena pronunciación. Su confianza al hablar en inglés es evidente.",
    "Nota_de_prueba_escrita": "En la prueba escrita, Carlos mostró un sólido entendimiento de la gramática y el vocabulario. Continuar practicando la escritura le ayudará a consolidar sus habilidades.",
    "Homework": "Carlos siempre entrega sus deberes a tiempo y con gran calidad. Esto ha contribuido a su aprendizaje continuo.",
    "Evaluación_general": "El desempeño general de Carlos este trimestre ha sido excelente. Su dedicación y entusiasmo han contribuido a su progreso. Se recomienda que continúe practicando inglés durante el verano para mantener y mejorar sus habilidades.",
    "Global_Score": "Carlos ha alcanzado un nivel de competencia muy bueno para su edad y curso, reflejando su esfuerzo y dedicación."
}
**
"""

    descripcion_tarea += sample_report

    # Construir la sección de datos del estudiante, incluyendo Homework y Global Score
    descripcion_tarea += f"""
**Ahora, utilizando los datos proporcionados a continuación para el estudiante, genera el informe siguiendo el estilo del ejemplo anterior pero variando la estructura para evitar repeticiones.**

**Datos del estudiante: ESENCIAL QUE SOLO USES DATOS DE AQUÍ Y NO TE INVENTES NINGÚN DATO NO PRESENTE**
- Nombre: {student.student_name.split()[0]}
- Homework: {student.homework_comment}
- Entra contento a clase: {student.enters_happy}
- Actitud positiva: {student.positive_attitude}
- Entusiasmo: {student.enthusiasm}
- Toma iniciativa: {student.initiative}
- Dato diferenciador: {student.differentiator}
- Puntos a mejorar en comportamiento: {student.behavior_improvement_points}
- Puntos fuertes en comportamiento: {student.behavior_strong_points}
- Tiene amigos en clase: {student.has_friends_in_class}
- Se distrae: {student.gets_distracted}
- Colabora con compañeros: {student.collaborates_with_peers}
- Respeta turnos de palabra: {student.respects_turns}
- Cuida el material: {student.cares_for_materials}
- Acciones en caso de mal comportamiento: {student.misbehavior_action}

- Participa: {student.work_participates}
- Actividades preferidas: {student.work_preferred_activities}
- Buena pronunciación: {student.work_good_pronunciation}
- Se esfuerza por comunicarse en inglés: {student.work_efforts_to_communicate}
- Se expresa con seguridad: {student.work_confident_expression}
- Pregunta dudas: {student.work_asks_questions}
- Ayuda a la profe: {student.work_helps_teacher}
- Sigue instrucciones: {student.work_follows_instructions}

- Comprende: {student.performance_understands}
- Usa palabras clave: {student.performance_uses_keywords}
- Hace estructuras completas: {student.performance_makes_complete_structures}
- Ejemplo de oraciones que hace en inglés (único al que le siguen paréntesis): {student.performance_example_sentences}
- Puede deletrear correctamente: {student.performance_spells_correctly}
- Puntos fuertes de rendimiento: {student.performance_strong_points}
- Puntos a mejorar en rendimiento: {student.performance_improvement_points}

**Importante**:
- REDACTA LO MÁS HUMANO POSIBLE COMO UN BUEN PROFESOR
- Asegúrate de que el informe final esté en formato JSON válido.
- Utiliza comillas dobles para las claves y los valores.
- Si necesitas incluir comillas dentro de un valor, escápalas usando \\\".
"""

    # Generar el informe utilizando el modelo
    respuesta = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[{"role": "user", "content": descripcion_tarea}],
        response_format=ReportModelTweens
    )

    # Extraer el contenido del informe
    informe = respuesta.choices[0].message.content

    try:
        # Convertir la respuesta a formato JSON si es válida
        report = json.loads(informe)
    except json.JSONDecodeError:
        # Manejar el caso donde la respuesta no es JSON válido
        print("Error: La respuesta no es JSON válido.")
        report = {}
    return report