from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import json
from pydantic import BaseModel

class ReportModel(BaseModel):
    Motivación_y_Participación: str
    Aprendizaje: str
    Comportamiento: str
    Nota_de_prueba_oral: str
    Evaluación_general: str

llm4o = ChatOpenAI(model="gpt-4o")
llm4o_mini = ChatOpenAI(model="gpt-4o-mini")

def generar_reporte(student):

    dod = '''1. Personaliza el informe y refleja el carácter y estilo de aprendizaje del estudiante.
    2. Cada sección debe tener al menos 300 caracteres.
    3. Usa el nombre del estudiante al menos una vez en cada sección, no uses los apellidos.
    4. Incluye ejemplos de actividades que el estudiante disfruta y estructuras de inglés que ha aprendido.
    5. Las estructuras aprendidas en inglés entre comillas y las traducciones segidas en español entre paréntesis.
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

    El JSON final debe incluir las siguientes secciones con exactamente estos nombres de clave:
    1. Motivación_y_Participación
    2. Aprendizaje
    3. Comportamiento
    4. Nota_de_prueba_oral
    5. Evaluación_general

    **Ahora, utilizando los datos proporcionados a continuación para el estudiante, genera el informe siguiendo el estilo del ejemplo anterior pero variando la estructura para evitar repeticiones.**

    **Datos del estudiante:**
    - Nombre: {student.student_name}
    - Curso: {student.course}
    - Centro: {student.center}
    - Nombre del grupo: {student.group_name}
    - Profesora: {student.professor}
    - Termino: {student.term}
    - Frecuencia de escucha de audio: {student.audio_listening_frequency}
    - Nota de prueba oral: {student.oral_test_score}
    - Comentario de prueba oral: {student.oral_test_comment}
    - Nota de prueba escrita: {student.written_test_score}
    - Comentario de prueba escrita: {student.written_test_comment}

    - Calificación de comportamiento: {student.behavior_rating}
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

    - Calificación de trabajo: {student.work_rating}
    - Participa: {student.participates}
    - Actividades preferidas: {student.preferred_activities}
    - Buena pronunciación: {student.good_pronunciation}
    - Se esfuerza por comunicarse en inglés: {student.efforts_to_communicate}
    - Se expresa con seguridad: {student.confident_expression}
    - Pregunta dudas: {student.asks_questions}
    - Ayuda a la profe: {student.helps_teacher}
    - Sigue instrucciones: {student.follows_instructions}

    - Calificación de rendimiento: {student.performance_rating}
    - Comprende: {student.understands}
    - Usa palabras clave: {student.uses_keywords}
    - Hace estructuras completas: {student.makes_complete_structures}
    - Ejemplo de oraciones que hace: {student.example_sentences}
    - Puede deletrear correctamente: {student.spells_correctly}
    - Puntos fuertes de rendimiento: {student.strong_points_performance}
    - Puntos a mejorar en rendimiento: {student.improvement_points_performance}

    - Deberes: {student.homework}
    - Comentario de deberes: {student.homework_comment}

    **Importante**:
    - Asegúrate de que el informe final esté en formato JSON válido.    
    - Utiliza comillas dobles para las claves y los valores.
    - Si necesitas incluir comillas dentro de un valor, escápalas usando \\\".

    **Instrucciones para el informe:**

    1. **Motivación_y_Participación**: Describe el nivel de participación y motivación del estudiante en la clase, utilizando los datos sobre si participa, entra contento, muestra entusiasmo, y toma iniciativa. Incluye actividades preferidas y cualquier característica única que lo distinga (dato diferenciador).
    
    2. **Aprendizaje**: Evalúa las habilidades de aprendizaje del estudiante, incluyendo comprensión, uso de palabras clave, estructuras completas, y esfuerzo por comunicarse en inglés. Menciona ejemplos de frases si están disponibles y resalta tanto los puntos fuertes como áreas de mejora en aprendizaje.

    3. **Comportamiento**: Proporciona una descripción del comportamiento en clase, incluyendo respeto a turnos de palabra, colaboración con compañeros, si ayuda a la profesora, y si sigue instrucciones. Usa la calificación de comportamiento y puntos fuertes y a mejorar en comportamiento.

    4. **Nota_de_prueba_oral**: Explica la nota obtenida en la prueba oral, destacando fortalezas y cualquier área en la que pueda mejorar, especialmente en pronunciación y expresión oral.

    5. **Evaluación_general**: Haz una valoración general del rendimiento del estudiante, resumiendo sus fortalezas y sugiriendo cualquier recomendación para continuar desarrollando sus habilidades en el idioma inglés.

    Asegúrate de que el informe siga el estilo del ejemplo pero varía la estructura para que no sea repetitivo y cada informe sea único.

    """
    response = llm4o.generate_responses([descripcion_tarea])
    json_output = response[0].text.strip()

    try:
        # Convert the response to JSON format if it's valid
        report = json.loads(json_output)
    except json.JSONDecodeError:
        # Handle case where response isn't valid JSON
        print("Error: La respuesta no es JSON válido.")
        report = {}

    return report

