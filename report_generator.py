from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import json

llm4o = ChatOpenAI(model="gpt-4")
llm4o_mini = ChatOpenAI(model="gpt-3.5-turbo")

def generar_reporte(student):
    agente_escritor = Agent(
        role="Escritor de informes",
        goal="Escribe informes detallados y personalizados de los estudiantes siguiendo la Definición de Hecho",
        backstory="Eres un educador experimentado que escribe informes perspicaces sobre el progreso de los estudiantes.",
        allow_delegation=False,
        llm=llm4o_mini,
    )
    
    descripcion_tarea = f"""
    Escribe un informe detallado para {student.name} basado en sus datos de rendimiento.
    Sigue estas pautas de la Definición de Hecho:
    1. Personaliza el informe y refleja el carácter y estilo de aprendizaje del estudiante.
    2. Cada sección debe tener al menos 300 caracteres.
    3. Usa el nombre del estudiante al menos una vez en cada sección.
    4. Incluye ejemplos de actividades que el estudiante disfruta y estructuras de inglés que ha aprendido.
    5. Las estructuras aprendidas en inglés entre comillas y las traducciones segidas en español entre paréntesis.
    6. Asegúrate de que el informe refleje con precisión el progreso, carácter y aptitudes del estudiante.
    7. Escribe en tercera persona, evitando declaraciones en primera persona.
    8. Enfócate en información relevante para el rendimiento en clase, evitando comentarios demasiado personales.
    9. Sé tacto al abordar problemas, siempre proponiendo soluciones.
    10. Asegúrate de que la evaluación (excelente, muy bien, bien, satisfactorio, deficiente) coincida con el contenido escrito.
    11. Usa lenguaje positivo y propone soluciones al abordar problemas.
    12. Para el informe final del año, incluye una evaluación general y recomendaciones de práctica para el verano.
    13. Para las clases de Babies, enfócate en las reacciones e indicadores de comprensión.
    14. Para las clases de T&T, aborda el comportamiento, hábitos de trabajo y rendimiento en todas las habilidades.

    Incluye las siguientes secciones:
    1. Motivación y Participación
    2. Aprendizaje
    3. Comportamiento
    4. Nota de prueba oral
    5. Evaluación general

    Usa los siguientes datos:
    - Nombre: {student.name}
    - Profesor: {student.professor}
    - Ausencias: {student.absences}
    - Frecuencia de escucha: {student.listening_frequency}
    - Participa: {student.participates}
    - Entra contento: {student.enters_happy}
    - Actitud positiva: {student.positive_attitude}
    - Entusiasmo: {student.enthusiasm}
    - Toma iniciativa: {student.takes_initiative}
    - Actividades preferidas: {student.preferred_activities}
    - Comprende: {student.understands}
    - Nota de prueba oral: {student.oral_test_score}
    - Nota de escritura: {student.writing_score}
    - Nota de tareas: {student.homework_score}
    """
    
    tarea_escritor = Task(
        description=descripcion_tarea,
        agent=agente_escritor,
        verbose=True,
        expected_output="json"
    )
    
    agente_revisor = Agent(
        role="Revisor de informes",
        goal="Revisa y aprueba los informes de los estudiantes para garantizar la precisión, calidad y adherencia a la Definición de Hecho",
        backstory="Eres un educador senior con años de experiencia en la revisión de informes de estudiantes.",
        allow_delegation=False,
        llm=llm4o_mini,
    )
    
    tarea_revisor = Task(
        description="Revisa y aprueba el informe generado, asegurando que cubra todas las secciones requeridas, refleje con precisión el rendimiento del estudiante y cumpla con todos los puntos de la Definición de Hecho.",
        agent=agente_revisor,
        verbose=True,
        expected_output="json"
    )

    equipo = Crew(
        agents=[agente_escritor, agente_revisor],
        tasks=[tarea_escritor, tarea_revisor]
    )

    reporte_salida = equipo.kickoff()
    reporte_salida = json.loads(reporte_salida)
    
    informe_formateado = {
        "Data": {
            "Nombre": student.name,
            "Profesor": student.professor,
            "Ausencias": student.absences,
            "Frecuencia de escucha": student.listening_frequency,
            "Motivación y Participación": reporte_salida.get('Motivación y Participación', ''),
            "Aprendizaje": reporte_salida.get('Aprendizaje', ''),
            "Comportamiento": reporte_salida.get('Comportamiento', ''),
            "Nota de prueba oral": reporte_salida.get('Nota de prueba oral', ''),
            "Evaluación general": reporte_salida.get('Evaluación general', '')
        }
    }

    return informe_formateado