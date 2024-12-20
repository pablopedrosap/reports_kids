# from crewai import Agent, Task, Crew
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
    Nota_de_prueba_oral: str
    Nota_de_prueba_escrita: Optional[str] = None  # Make this field optional
    Evaluación_general: str

llm4o = ChatOpenAI(model="gpt-4o")
llm4o_mini = ChatOpenAI(model="gpt-4o-mini")

def generar_reporte(student):
    # print(student)
    # print(student.student_name)
    # for attr, value in vars(student).items():
    #     setattr(student, attr, str(value) if value is not None else '')


    # # Determinar si la categoría del estudiante incluye prueba escrita
    # courses_with_written_test = ['B&B', 'Ben&Brenda', 'Tweens', 'Teens']
    # include_written_test = student.category in courses_with_written_test

    # # Construir la sección de datos del estudiante
    # datos_estudiante = []

    print(student.data.get('student_name', ''))

    # Convert all values to strings, handling None
    student_data = {
        k: str(v).split()[0] if k == 'Nombre alumno' and v is not None else str(v)
        for k, v in student.data.items()
        if k != 'Nombre grupo' and k != 'Profesora' and v is not None  # Exclude 'Nombre grupo' and None values
    }

    # Determine if the category includes written test
    courses_with_written_test = ['B&B', 'Ben&Brenda', 'Tweens', 'Teens']
    include_written_test = student.category in courses_with_written_test

    # Prepare data to pass to LLM
    datos_estudiante = {k: v for k, v in student_data.items() if v.strip()}



    # Sólo añadimos líneas si el valor no es vacío

    # if student.student_name.strip():
    #     datos_estudiante.append(f"- Nombre: {student.student_name.split()[0]}")
    # if student.oral_test_score.strip():
    #     datos_estudiante.append(f"- Puntuación de prueba oral: {student.oral_test_score}")

    # if include_written_test and student.written_test_score != 0:
    #     datos_estudiante.append(f"- Puntuación de prueba escrita: {student.written_test_score if student.written_test_score != 0 else 'no disponible de momento'}. No menciones la nota específica")

    # if student.enters_happy.strip():
    #     datos_estudiante.append(f"- Entra contento a clase: {student.enters_happy}")
    # if student.positive_attitude.strip():
    #     datos_estudiante.append(f"- Actitud positiva: {student.positive_attitude}")
    # if student.enthusiasm.strip():
    #     datos_estudiante.append(f"- Entusiasmo: {student.enthusiasm}")
    # if student.initiative.strip():
    #     datos_estudiante.append(f"- Toma iniciativa: {student.initiative}")
    # if student.differentiator.strip():
    #     datos_estudiante.append(f"- Dato diferenciador: {student.differentiator}")
    # if student.behavior_improvement_points.strip():
    #     datos_estudiante.append(f"- Puntos a mejorar en comportamiento: {student.behavior_improvement_points}")
    # if student.behavior_strong_points.strip():
    #     datos_estudiante.append(f"- Puntos fuertes en comportamiento: {student.behavior_strong_points}")
    # if student.has_friends_in_class.strip():
    #     datos_estudiante.append(f"- Tiene amigos en clase: {student.has_friends_in_class}")
    # if student.gets_distracted.strip():
    #     datos_estudiante.append(f"- Se distrae: {student.gets_distracted}")
    # if student.collaborates_with_peers.strip():
    #     datos_estudiante.append(f"- Colabora con compañeros: {student.collaborates_with_peers}")
    # if student.respects_turns.strip():
    #     datos_estudiante.append(f"- Respeta turnos de palabra: {student.respects_turns}")
    # if student.cares_for_materials.strip():
    #     datos_estudiante.append(f"- Cuida el material: {student.cares_for_materials}")
    # if student.misbehavior_action.strip():
    #     datos_estudiante.append(f"- Acciones en caso de mal comportamiento: {student.misbehavior_action}")
    # if student.participates.strip():
    #     datos_estudiante.append(f"- Participa: {student.participates}")
    # if student.preferred_activities.strip():
    #     datos_estudiante.append(f"- Actividades preferidas: {student.preferred_activities}")
    # if student.good_pronunciation.strip():
    #     datos_estudiante.append(f"- Buena pronunciación: {student.good_pronunciation}")
    # if student.efforts_to_communicate.strip():
    #     datos_estudiante.append(f"- Se esfuerza por comunicarse en inglés: {student.efforts_to_communicate}")
    # if student.confident_expression.strip():
    #     datos_estudiante.append(f"- Se expresa con seguridad: {student.confident_expression}")
    # if student.asks_questions.strip():
    #     datos_estudiante.append(f"- Pregunta dudas: {student.asks_questions}")
    # if student.helps_teacher.strip():
    #     datos_estudiante.append(f"- Ayuda a la profe: {student.helps_teacher}")
    # if student.follows_instructions.strip():
    #     datos_estudiante.append(f"- Sigue instrucciones: {student.follows_instructions}")
    # if student.understands.strip():
    #     datos_estudiante.append(f"- Comprende: {student.understands}")
    # if student.uses_keywords.strip():
    #     datos_estudiante.append(f"- Usa palabras clave: {student.uses_keywords}")
    # if student.makes_complete_structures.strip():
    #     datos_estudiante.append(f"- Hace estructuras completas: {student.makes_complete_structures}")
    # if student.example_sentences.strip():
    #     datos_estudiante.append(f"- Ejemplo de oraciones que hace en inglés (único al que le siguen paréntesis): {student.example_sentences}")
    # if student.learning_strong_points.strip():
    #     datos_estudiante.append(f"- Puntos fuertes de rendimiento: {student.learning_strong_points}")
    # if student.learning_improvement_points.strip():
    #     datos_estudiante.append(f"- Puntos a mejorar en rendimiento: {student.learning_improvement_points}")
    # if student.homework.strip():
    #     datos_estudiante.append(f"- Deberes: {student.homework}")

    # Unir todas las líneas filtradas


    dod = f'''1. Personaliza el informe y refleja el carácter y estilo de aprendizaje del estudiante.
2. Cada sección debe tener al menos 300 caracteres.
3. Usa el nombre del estudiante al menos una vez en cada sección, NO uses los apellidos.
4. En el apartado de motivación incluye ejemplos de actividades que el estudiante disfruta si las hay y estructuras de inglés que ha aprendido en aprendizaje.
5. Las frases aprendidas en inglés entre comillas y las traducciones seguidas en español entre paréntesis (Solo las frases aprendidas que estén en inglés deben ser traducidas a español entre paréntesis, nada más debe ir entre paréntesis) Todo el texto aparte siempre en español.
6. Asegúrate de que el informe refleje con precisión el progreso, carácter y aptitudes del estudiante.
7. Escribe en tercera persona, evitando declaraciones en primera persona.
8. Enfócate en información relevante para el rendimiento en clase, evitando comentarios demasiado personales.
9. Sé tacto al abordar problemas, siempre proponiendo soluciones.
10. Asegúrate de que la evaluación coincida con el contenido escrito. No hables de la nota concreta, solo justifícala.
11. Usa lenguaje positivo y propone soluciones al abordar problemas.
12. Para el informe final del año, incluye una evaluación general y recomendaciones de práctica para el verano.
13. Para las clases de Babies, enfócate en las reacciones e indicadores de comprensión.
14. Para las clases de T&T, aborda el comportamiento, hábitos de trabajo y rendimiento en todas las habilidades.
15. No menciones verano o otros tiempos del año ya que no sabes en que trimestre está el alumno, tampoco menciones que no lo sabes. Tampoco menciones notas concretas aunque sí justificalas.
16. Crucial que no te inventes ningún dato que no te he proporcionado. Como asumir el numero de alumnos o el género del profesor. Solo usa lo que sabes.
17. Decir entrar al aula en vez de ‘’ingresar al aula’’, no decir "exitosamente", no hablar del alumno como un "recurso" o usar ninguna expresión latina, solo usar español de España.
18. Solo una vez dar alguna pequeña oración de ánimo como: sigue así, bien hecho, well done!, awesome, excellent, way to go!.
{ "19. Si el curso es mousy o linda, no hablar de 'práctica gramatical avanzada' ya que son pequeños." if 'mousy' in student.category.lower() or 'linda' in student.category.lower() else "" }
'''

    descripcion_tarea = f"""
Escribe un informe detallado para el estudiante basado en sus datos de rendimiento, sin inventar datos.
Sigue estas pautas de la Definición de Hecho:
{dod}


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
    "Nota_de_prueba_oral": "<(Aquí solo puedes responder una de estas 4 sin inventartelo): Aceptable. Entiende la pregunta, pero es necesario darle el inicio de la palabra para que responda utilizando un término aislado.
Bueno. Entiende la pregunta y responde con una palabra, aunque en ocasiones es necesario ayudarle con el inicio de la misma.
Muy bueno. Entiende la pregunta y responde utilizando la palabra adecuada, casi sin ayuda.
Excelente. Responde adecuadamente a la pregunta realizada por el profesor, ya sea con una sola palabra o con la estructura completa, sin necesidad de que se le ayude.>",
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
        "Comment": "Elisa ha demostrado una buena comprensión de las estructuras básicas del ingl��s, utilizando frases como \\\"I like to play with my friends\\\" (Me gusta jugar con mis amigos). Aunque su uso de palabras clave ha sido adecuado, hay margen para el fortalecimiento de estructuras complejas y la expansión de su vocabulario. Elisa no duda en formular preguntas cuando encuentra dificultades, lo que refleja su constructiva curiosidad. Continúa esforzándose por comunicarse en inglés y su pronunciación ha mejorado notablemente. Un enfoque más centrado en la práctica oral y auditiva la beneficiaría aún más."
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

"""
    
    descripcion_tarea += f"""{datos_estudiante}
**Importante**:
- REDACTA LO MÁS HUMANO POSIBLE COMO UN BUEN PROFESOR/PROFESORA
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
    with open('names.txt', 'a') as file:
        file.write(f'\n{student.data.get('student_name', '')}')

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
    My_Way: str
    Nota_de_prueba_oral: str  # Solo se necesita el comentario
    Nota_de_prueba_escrita: str  # Incluida para "Tweens"
    Deberes: str  # Añadido Homework sin calificación
    Evaluación_general: str    # Solo se necesita el comentario
    Nota_Global: str  # Añadido Global Score sin calificación

'''bb lo detecta como'''

def generar_reporte_tweens(student):

    print(student.data.get('student_name', ''))


    # print(student.student_name)
    # for attr, value in vars(student).items():
    #     setattr(student, attr, str(value) if value is not None else '')

    courses_with_written_test = ['B&B', 'Ben&Brenda', 'Tweens', 'Teens']

    student_data = {
        k: str(v).split()[0] if k == 'Nombre alumno' and v is not None else str(v)
        for k, v in student.data.items()
        if k != 'Nombre grupo' and k != 'Profesora' and v is not None  # Exclude 'Nombre grupo' and None values
    }

    # Determine if the category includes written test
    courses_with_written_test = ['B&B', 'Ben&Brenda', 'Tweens', 'Teens']
    include_written_test = student.category in courses_with_written_test

    # Prepare data to pass to LLM
    datos_estudiante = {k: v for k, v in student_data.items() if v.strip()}

    

    # datos_estudiante = []

    # if student.student_name.strip():
    #     datos_estudiante.append(f"- Nombre: {student.student_name.split()[0]}")
    # if student.oral_test_score != '':
    #     datos_estudiante.append(f"- Puntuación de prueba oral: {student.oral_test_score}")

    # if student.written_test_score != '':
    #     datos_estudiante.append(f"- Puntuación de prueba escrita: {student.written_test_score if student.written_test_score != 0 else 'no disponible de momento'}. No menciones la nota específica")

    # if student.enters_happy.strip():
    #     datos_estudiante.append(f"- Entra contento a clase: {student.enters_happy}")
    # if student.my_way.strip():
    #     datos_estudiante.append(f"- My Way comment: {student.my_way}")
    # if student.positive_attitude.strip():
    #     datos_estudiante.append(f"- Actitud positiva: {student.positive_attitude}")
    # if student.enthusiasm.strip():
    #     datos_estudiante.append(f"- Entusiasmo: {student.enthusiasm}")
    # if student.initiative.strip():
    #     datos_estudiante.append(f"- Toma iniciativa: {student.initiative}")
    # if student.differentiator.strip():
    #     datos_estudiante.append(f"- Dato diferenciador: {student.differentiator}")
    # if student.behavior_improvement_points.strip():
    #     datos_estudiante.append(f"- Puntos a mejorar en comportamiento: {student.behavior_improvement_points}")
    # if student.behavior_strong_points.strip():
    #     datos_estudiante.append(f"- Puntos fuertes en comportamiento: {student.behavior_strong_points}")
    # if student.has_friends_in_class.strip():
    #     datos_estudiante.append(f"- Tiene amigos en clase: {student.has_friends_in_class}")
    # if student.gets_distracted.strip():
    #     datos_estudiante.append(f"- Se distrae: {student.gets_distracted}")
    # if student.collaborates_with_peers.strip():
    #     datos_estudiante.append(f"- Colabora con compañeros: {student.collaborates_with_peers}")
    # if student.respects_turns.strip():
    #     datos_estudiante.append(f"- Respeta turnos de palabra: {student.respects_turns}")
    # if student.cares_for_materials.strip():
    #     datos_estudiante.append(f"- Cuida el material: {student.cares_for_materials}")
    # if student.misbehavior_action.strip():
    #     datos_estudiante.append(f"- Acciones en caso de mal comportamiento: {student.misbehavior_action}")
    # if student.participates.strip():
    #     datos_estudiante.append(f"- Participa: {student.participates}")
    # if student.preferred_activities.strip():
    #     datos_estudiante.append(f"- Actividades preferidas: {student.preferred_activities}")
    # if student.good_pronunciation.strip():
    #     datos_estudiante.append(f"- Buena pronunciación: {student.good_pronunciation}")
    # if student.efforts_to_communicate.strip():
    #     datos_estudiante.append(f"- Se esfuerza por comunicarse en inglés: {student.efforts_to_communicate}")
    # if student.confident_expression.strip():
    #     datos_estudiante.append(f"- Se expresa con seguridad: {student.confident_expression}")
    # if student.asks_questions.strip():
    #     datos_estudiante.append(f"- Pregunta dudas: {student.asks_questions}")
    # if student.helps_teacher.strip():
    #     datos_estudiante.append(f"- Ayuda a la profe: {student.helps_teacher}")
    # if student.follows_instructions.strip():
    #     datos_estudiante.append(f"- Sigue instrucciones: {student.follows_instructions}")
    # if student.understands.strip():
    #     datos_estudiante.append(f"- Comprende: {student.understands}")
    # if student.uses_keywords.strip():
    #     datos_estudiante.append(f"- Usa palabras clave: {student.uses_keywords}")
    # if student.makes_complete_structures.strip():
    #     datos_estudiante.append(f"- Hace estructuras completas: {student.makes_complete_structures}")
    # if student.example_sentences.strip():
    #     datos_estudiante.append(f"- Ejemplo de oraciones que hace en inglés (único al que le siguen paréntesis): {student.example_sentences}")
    # if student.learning_strong_points.strip():
    #     datos_estudiante.append(f"- Puntos fuertes de rendimiento: {student.learning_strong_points}")
    # if student.learning_improvement_points.strip():
    #     datos_estudiante.append(f"- Puntos a mejorar en rendimiento: {student.learning_improvement_points}")
    # if student.homework.strip():
    #     datos_estudiante.append(f"- Deberes: {student.homework}")

    # Unir todas las líneas filtradas

    dod = f'''1. Personaliza el informe y refleja el carácter y estilo de aprendizaje del estudiante.
2. Cada sección debe tener al menos 300 caracteres.
3. Usa el nombre del estudiante al menos una vez en cada sección, NO uses los apellidos.
4. Incluye ejemplos de actividades que el estudiante disfruta y estructuras de inglés que ha aprendido.
5. No hace falta que las incluyas, pero si las hay, las frases aprendidas en inglés entre comillas y las traducciones seguidas en español entre paréntesis (Solo las frases aprendidas que estén en inglés deben ser traducidas a español entre paréntesis, nada más debe ir entre paréntesis) Todo el texto aparte siempre en español.
6. Asegúrate de que el informe refleje con precisión el progreso, carácter y aptitudes del estudiante.
7. Escribe en tercera persona, evitando declaraciones en primera persona.
8. Enfócate en información relevante para el rendimiento en clase, evitando comentarios demasiado personales.
9. Sé tacto al abordar problemas, siempre proponiendo soluciones.
10. Asegúrate de que la evaluación coincida con el contenido escrito. No hables de la nota concreta, solo justifícala.
11. Usa lenguaje positivo y propone soluciones al abordar problemas.
12. Para el informe final del año, incluye una evaluación general y recomendaciones de práctica para el verano.
13. Para las clases de Babies, enfócate en las reacciones e indicadores de comprensión.
14. Para las clases de T&T, aborda el comportamiento, hábitos de trabajo y rendimiento en todas las habilidades.
15. No menciones verano o otros tiempos del año ya que no sabes en que trimestre está el alumno, tampoco menciones que no lo sabes. Tampoco menciones notas concretas aunque sí justificalas.
16. Crucial que no te inventes ningún dato que no te he proporcionado. Como asumir el numero de alumnos o el género del profesor. Solo usa lo que sabes.
17. Decir entrar al aula en vez de ‘’ingresar al aula’’, no decir "exitosamente", no hablar del alumno como un "recurso" o usar ninguna expresión latina, solo usar español de España.
18. Solo una vez dar alguna pequeña oración de ánimo como: sigue así, bien hecho, well done!, awesome, excellent, way to go!.
'''

    # Construir la parte inicial del prompt con las calificaciones
    descripcion_tarea = f"""
Escribe un informe detallado para el estudiante basado en sus datos de rendimiento, sin inventar datos.
Sigue estas pautas de la Definición de Hecho:
{dod}

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
    "My_Way": "<¿Cuáles son sus habilidades más fuertes?  aqui resume el tiempo activo en "My Way". >",
     "Nota_de_prueba_oral": "<(Aquí solo puedes responder una de estas 4 sin inventartelo): Aceptable. Entiende la pregunta, pero es necesario darle el inicio de la palabra para que responda utilizando un término aislado.
Bueno. Entiende la pregunta y responde con una palabra, aunque en ocasiones es necesario ayudarle con el inicio de la misma.
Muy bueno. Entiende la pregunta y responde utilizando la palabra adecuada, casi sin ayuda.
Excelente. Responde adecuadamente a la pregunta realizada por el profesor, ya sea con una sola palabra o con la estructura completa, sin necesidad de que se le ayude.>",
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
        "Comment": "Carlos comprende bien los conceptos enseñados y es capaz de usar palabras clave y estructuras completas. Su progreso es notable."
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
    descripcion_tarea += f"""{datos_estudiante}
**Importante**:
- REDACTA LO MÁS HUMANO POSIBLE COMO UN BUEN PROFESOR/PROFESORA
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
    if informe.startswith('```'):
        # Remove markdown code block formatting if present
        informe = informe.split('```')[1]
        if informe.startswith('json'):
            informe = informe[4:]
        informe = informe.strip()
    with open('names.txt', 'a') as file:
        file.write(f'\n{student.data.get('student_name', '')}')


    try:
        # Convertir la respuesta a formato JSON si es válida
        report = json.loads(informe)
    except json.JSONDecodeError:
        # Manejar el caso donde la respuesta no es JSON válido
        print("Error: La respuesta no es JSON válido.")
        report = {}
    return report