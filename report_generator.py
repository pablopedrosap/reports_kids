from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import json
from pydantic import BaseModel
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

class ReportSection(BaseModel):
    Rating: str
    Comment: str

# Define the main ReportModel
class ReportModel(BaseModel):
    Motivación_y_Participación: ReportSection
    Aprendizaje: ReportSection
    Comportamiento: ReportSection
    Nota_de_prueba_oral: str  # Only comment is needed
    Evaluación_general: str    # Only comment is needed

llm4o = ChatOpenAI(model="gpt-4o")
llm4o_mini = ChatOpenAI(model="gpt-4o-mini")

def generar_reporte(student):
    print(student)
    print(student.student_name)

    dod = '''1. Personaliza el informe y refleja el carácter y estilo de aprendizaje del estudiante.
    2. Cada sección debe tener al menos 300 caracteres.
    3. Usa el nombre del estudiante al menos una vez en cada sección, no uses los apellidos.
    4. Incluye ejemplos de actividades que el estudiante disfruta y estructuras de inglés que ha aprendido.
    5. Las frases aprendidas en inglés entre comillas y las traducciones segidas en español entre paréntesis (Solo las frases aprendidas que estén en ingles deben ser traducidas entre paréntesis, nada más entre paréntesis.).
    6. Asegúrate de que el informe refleje con precisión el progreso, carácter y aptitudes del estudiante.
    7. Escribe en tercera persona, evitando declaraciones en primera persona.
    8. Enfócate en información relevante para el rendimiento en clase, evitando comentarios demasiado personales.
    9. Sé tacto al abordar problemas, siempre proponiendo soluciones.
    10. Asegúrate de que la evaluación (excelente, muy bien, bien, satisfactorio, deficiente) coincida con el contenido escrito. No hables de la nota concreta, solo justifícala.
    11. Usa lenguaje positivo y propone soluciones al abordar problemas.
    12. Para el informe final del año, incluye una evaluación general y recomendaciones de práctica para el verano.
    13. Para las clases de Babies, enfócate en las reacciones e indicadores de comprensión.
    14. Para las clases de T&T, aborda el comportamiento, hábitos de trabajo y rendimiento en todas las habilidades.'''

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
        "Comment": "Elisa ha demostrado una buena comprensión de las estructuras básicas del inglés, utilizando frases como 'I like to play with my friends' (Me gusta jugar con mis amigos). Aunque su uso de palabras clave ha sido adecuado, hay margen para el fortalecimiento de estructuras complejas y la expansión de su vocabulario. Elisa no duda en formular preguntas cuando encuentra dificultades, lo que refleja su constructiva curiosidad. Continúa esforzándose por comunicarse en inglés y su pronunciación ha mejorado notablemente. Un enfoque más centrado en la práctica oral y auditiva la beneficiaría aún más."
    }},
    "Comportamiento": {{
        "Rating": "Excellent",
        "Comment": "El comportamiento de Elisa en clase es ejemplar. Respeta los turnos de palabra de manera consistente y demuestra gran colaboración con sus compañeros, lo que provoca un entorno armónico y productivo. Su capacidad para ayudar a sus compañeros y colaborar con la profesora, como cuando organiza materiales, es uno de sus puntos más destacados. Elisa sigue las instrucciones con precisión y cuida el material con esmero, manteniendo siempre en mente el bienestar común de su grupo de estudio. Esta actitud positiva y cooperativa la convierte en un miembro indispensable para su grupo de clase."
    }},
    "Nota_de_prueba_oral": "Aunque los datos de la prueba oral de Elisa no están disponibles, su creciente habilidad para articular sus pensamientos en inglés sugiere que está progresando bien en esta área. Se recomienda continuar practicando inglés conversacional, permitiéndole ganar más confianza en sus habilidades orales.",
    "Evaluación_general": "El rendimiento general de Elisa durante este término ha sido notable. Su comportamiento proactivo y positivo se traduce directamente en sus experiencias de aprendizaje. Se evidencia un buen uso de estructuras básicas del inglés, aunque podría beneficiarse de más práctica en el uso de frases complejas y enriquecimiento de vocabulario. Sugiero que durante el verano, Elisa continúe exponiéndose al inglés mediante audiolibros y conversaciones con hablantes nativos. Con estas estrategias, Elisa podrá seguir desarrollando sus habilidades lingüísticas y mantener su entusiasmo por el idioma en el futuro académico."
}}
    **

    **Ahora, utilizando los datos proporcionados a continuación para el estudiante, genera el informe siguiendo el estilo del ejemplo anterior pero variando la estructura para evitar repeticiones.**

    **Datos del estudiante: ESENCIAL QUE SOLO USES DATOS DE AQUÍ Y NO TE INVENTES NINGÚN DATO NO PRESENTE**
- Nombre: {student.student_name}
- Nota de prueba oral: {student.oral_test_score}
- Comentario de prueba oral: {student.oral_test_comment}
- Comentario de prueba escrita: {student.written_test_comment}

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
- Comentario de deberes: {student.homework_comment}

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
        # Convert the response to JSON format if it's valid
        report = json.loads(informe)
        
    except json.JSONDecodeError:
        # Handle case where response isn't valid JSON
        print("Error: La respuesta no es JSON válido.")
        report = {}

    return report

