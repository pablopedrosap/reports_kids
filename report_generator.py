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

llm4o = ChatOpenAI(model="gpt-4")
llm4o_mini = ChatOpenAI(model="gpt-4o-mini")


def generar_reporte(student):
    agente_escritor = Agent(
        role="Escritor de informes",
        goal="Escribe informes detallados y personalizados de los estudiantes siguiendo la Definición de Hecho",
        backstory="Eres un educador experimentado que escribe informes perspicaces sobre el progreso de los estudiantes.",
        allow_delegation=False,
        llm=llm4o_mini,
    )
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
    Escribe un informe detallado para {student.name} basado en sus datos de rendimiento, no te inventes datos.
    Sigue estas pautas de la Definición de Hecho:
    {dod}

    El JSON final solo debe incluir las siguientes secciones:
    1. Motivación y Participación
    2. Aprendizaje
    3. Comportamiento
    4. Nota de prueba oral
    5. Evaluación general

    Usando los siguientes datos (solo los que no están en blanco):
    
    - Nombre: {student.name}
    - Curso: {student.course}
    - Escuela: {student.school}
    - Horario: {student.schedule}
    - Frecuencia de escucha de audio: {student.audio_listening_frequency}
    - Nota de prueba oral: {student.oral_test_score}
    - Comentario de prueba oral: {student.oral_test_comment}
    - Nota de prueba escrita: {student.written_test_score}
    - Comentario de prueba escrita: {student.written_test_comment}
    - Participa: {student.participates}
    - Entra contento a clase: {student.enters_happy}
    - Actitud positiva: {student.positive_attitude}
    - Entusiasmo: {student.enthusiasm}
    - Toma iniciativa: {student.takes_initiative}
    - Baila las canciones: {student.dances_to_songs}
    - Dato diferenciador: {student.differentiator}
    - Puntos a mejorar: {student.improvement_points}
    - Puntos fuertes: {student.strong_points}
    - Actividades preferidas: {student.preferred_activities}
    - Comprende: {student.understands}
    - Usa palabras clave: {student.uses_keywords}
    - Hace estructuras completas: {student.makes_complete_structures}
    - Ejemplo de oraciones que hace: {student.example_sentences}
    - Buena pronunciación: {student.good_pronunciation}
    - Se esfuerza por comunicarse en inglés: {student.efforts_to_communicate}
    - Se expresa con seguridad: {student.confident_expression}
    - Puede deletrear correctamente: {student.spells_correctly}
    - Puntos fuertes de aprendizaje: {student.learning_strong_points}
    - Puntos a mejorar en el aprendizaje: {student.learning_improvement_points}
    - Pregunta dudas: {student.asks_questions}
    - Comportamiento: {student.behavior_rating}
    - Ayuda a la profe: {student.helps_teacher}
    - Tiene amigos en clase: {student.has_friends_in_class}
    - Se distrae: {student.gets_distracted}
    - Colabora con compañeros: {student.collaborates_with_peers}
    - Sigue instrucciones: {student.follows_instructions}
    - Respeta turnos de palabra: {student.respects_turns}
    - Cuida el material: {student.cares_for_materials}
    - Acciones en caso de mal comportamiento: {student.misbehavior_action}
    - Puntos fuertes de comportamiento: {student.behavior_strong_points}
    - Puntos a mejorar en comportamiento: {student.behavior_improvement_points}
    """
    
    tarea_escritor = Task(
        description=descripcion_tarea,
        agent=agente_escritor,
        verbose=True,
        expected_output="json"
    )
    
    escritor = Crew(
        agents=[agente_escritor],
        tasks=[tarea_escritor]
    )

    reporte_salida = escritor.kickoff()
    print(reporte_salida)

    agente_revisor = Agent(
        role="Revisor de informes",
        goal=f"Dado el informe: {reporte_salida}. Revisa y aprueba los informes de los estudiantes para garantizar la precisión, calidad y adherencia a la Definición de Hecho.",
        backstory="Eres un educador senior con años de experiencia en la revisión de informes de estudiantes.",
        allow_delegation=False,
        llm=llm4o_mini,
    )

    tarea_revisor = Task(
        description=f"Revisa y mejora el informe generado, asegurando que cubra todas las secciones requeridas, refleje con precisión el rendimiento del estudiante y cumpla con todos los puntos de la Definición de Hecho: {dod}.",
        agent=agente_revisor,
        verbose=True,
        output_json=ReportModel,
        expected_output="json"
    )

    revisor = Crew(
        agents=[agente_revisor],
        tasks=[tarea_revisor]
    )
    reporte_salida = revisor.kickoff()

    print(reporte_salida)
    reporte_salida = json.dumps(reporte_salida)
    print(reporte_salida)
    
    informe_formateado = {
        "Data": {
            "Motivación y Participación": reporte_salida.get('Motivación y Participación', ''),
            "Aprendizaje": reporte_salida.get('Aprendizaje', ''),
            "Comportamiento": reporte_salida.get('Comportamiento', ''),
            "Nota de prueba oral": reporte_salida.get('Nota de prueba oral', ''),
            "Evaluación general": reporte_salida.get('Evaluación general', '')
        }
    }

    return informe_formateado