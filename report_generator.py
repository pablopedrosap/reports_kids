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

    example_student = {
        'name': 'María',
        'course': 'Pam&Paul',
        'oral_test_score': '8.5',
        'participates': 'Sí',
        'enters_happy': 'Sí',
        'positive_attitude': 'Sí',
        'enthusiasm': 'Sí',
        'takes_initiative': 'A veces',
        'dances_to_songs': 'Sí',
        'differentiator': 'Es muy creativa en las actividades',
        'improvement_points': 'Debe mejorar su pronunciación en inglés',
        'strong_points': 'Gran comprensión lectora',
        'preferred_activities': 'Le gustan los juegos de roles',
        'understands': 'Sí',
        'uses_keywords': 'Sí',
        'makes_complete_structures': 'A veces',
        'example_sentences': '"I like to play soccer" (Me gusta jugar al fútbol)',
        'good_pronunciation': 'A veces',
        'efforts_to_communicate': 'Sí',
        'confident_expression': 'Sí',
        'spells_correctly': 'Sí',
        'learning_strong_points': 'Buena comprensión auditiva',
        'learning_improvement_points': 'Pronunciación',
        'asks_questions': 'Sí',
        'behavior_rating': 'Excelente',
        'helps_teacher': 'Sí',
        'has_friends_in_class': 'Sí',
        'gets_distracted': 'No',
        'collaborates_with_peers': 'Sí',
        'follows_instructions': 'Sí',
        'respects_turns': 'Sí',
        'cares_for_materials': 'Sí',
        'misbehavior_action': '',
        'behavior_strong_points': 'Siempre dispuesta a ayudar',
        'behavior_improvement_points': '',
    }

    # Incluir el ejemplo en la descripción de la tarea
    descripcion_tarea = f"""
    Escribe un informe detallado para {student.name} basado en sus datos de rendimiento, no te inventes datos.
    Sigue estas pautas de la Definición de Hecho:
    {dod}

    El JSON final debe incluir las siguientes secciones con exactamente estos nombres de clave:
    1. Motivación_y_Participación
    2. Aprendizaje
    3. Comportamiento
    4. Nota_de_prueba_oral
    5. Evaluación_general

    A continuación, se proporciona un ejemplo de datos de un estudiante y el informe ideal correspondiente:

    **Datos del estudiante de ejemplo:**

    - Nombre: {example_student['name']}
    - Curso: {example_student['course']}
    - Nota de prueba oral: {example_student['oral_test_score']}
    - Participa: {example_student['participates']}
    - Entra contento a clase: {example_student['enters_happy']}
    - Actitud positiva: {example_student['positive_attitude']}
    - Entusiasmo: {example_student['enthusiasm']}
    - Toma iniciativa: {example_student['takes_initiative']}
    - Baila las canciones: {example_student['dances_to_songs']}
    - Dato diferenciador: {example_student['differentiator']}
    - Puntos a mejorar: {example_student['improvement_points']}
    - Puntos fuertes: {example_student['strong_points']}
    - Actividades preferidas: {example_student['preferred_activities']}
    - Comprende: {example_student['understands']}
    - Usa palabras clave: {example_student['uses_keywords']}
    - Hace estructuras completas: {example_student['makes_complete_structures']}
    - Ejemplo de oraciones que hace: {example_student['example_sentences']}
    - Buena pronunciación: {example_student['good_pronunciation']}
    - Se esfuerza por comunicarse en inglés: {example_student['efforts_to_communicate']}
    - Se expresa con seguridad: {example_student['confident_expression']}
    - Puede deletrear correctamente: {example_student['spells_correctly']}
    - Puntos fuertes de aprendizaje: {example_student['learning_strong_points']}
    - Puntos a mejorar en el aprendizaje: {example_student['learning_improvement_points']}
    - Pregunta dudas: {example_student['asks_questions']}
    - Comportamiento: {example_student['behavior_rating']}
    - Ayuda a la profe: {example_student['helps_teacher']}
    - Tiene amigos en clase: {example_student['has_friends_in_class']}
    - Se distrae: {example_student['gets_distracted']}
    - Colabora con compañeros: {example_student['collaborates_with_peers']}
    - Sigue instrucciones: {example_student['follows_instructions']}
    - Respeta turnos de palabra: {example_student['respects_turns']}
    - Cuida el material: {example_student['cares_for_materials']}
    - Acciones en caso de mal comportamiento: {example_student['misbehavior_action']}
    - Puntos fuertes de comportamiento: {example_student['behavior_strong_points']}
    - Puntos a mejorar en comportamiento: {example_student['behavior_improvement_points']}

    **Informe ideal para el estudiante de ejemplo:**

    {{
    "Motivación_y_Participación": {
        "Rating": "Excellent",
        "Comment": "María muestra una motivación excepcional en clase. Siempre entra contenta y participa activamente en todas las actividades. Su entusiasmo es contagioso y, aunque a veces toma la iniciativa, siempre aporta ideas creativas. Disfruta especialmente de los juegos de roles, donde puede expresar su imaginación. María baila las canciones con alegría, lo que anima a sus compañeros a unirse."
    },
    "Aprendizaje": {
        "Rating": "Good",
        "Comment": "María tiene una gran comprensión auditiva y lectora. Utiliza palabras clave y, aunque a veces no forma estructuras completas, se esfuerza por comunicarse en inglés. Un ejemplo de sus oraciones es 'Me gusta jugar'. Su pronunciación puede mejorar, pero muestra confianza al expresarse. Es capaz de deletrear correctamente y siempre está dispuesta a aprender."
    },
    "Comportamiento": {
        "Rating": "Excellent",
        "Comment": "El comportamiento de María es excelente. Siempre ayuda a la profesora y colabora bien con sus compañeros. Respeta los turnos de palabra y sigue las instrucciones sin problemas. No se distrae en clase y cuida el material. Está siempre dispuesta a ayudar, lo que la convierte en un valioso miembro del aula."
    },
    "Nota_de_prueba_oral": "María ha obtenido una nota de 8.5 en su prueba oral, reflejando su esfuerzo y dedicación. Aunque su pronunciación puede mejorar, su comprensión y expresión oral son sólidas. Pregunta dudas cuando es necesario, lo que demuestra su interés por el aprendizaje.",
    "Evaluación_general": "En general, María ha tenido un desempeño excelente este año. Se recomienda que durante el verano continúe practicando su pronunciación en inglés y participe en actividades que le permitan seguir desarrollando su creatividad y habilidades comunicativas. Con su actitud positiva y entusiasmo, estamos seguros de que continuará teniendo éxito en su aprendizaje del inglés."
}}
    **Importante**:
    - Asegúrate de que el informe final esté en formato JSON válido.    
    - Utiliza comillas dobles para las claves y los valores.
    - Si necesitas incluir comillas dentro de un valor, escápalas usando \\\".


    **Ahora, utilizando los datos proporcionados a continuación para {student.name}, genera el informe siguiendo el estilo del ejemplo anterior pero variando estructura ya que no puede ser nada repetitivo.**

    **Datos del estudiante:**

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
    reporte_salida = ''
    reporte_salida = escritor.kickoff()
    print(reporte_salida)
    reporte_final = json.loads(str(reporte_salida))
    print(reporte_final)

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

    # print(str(revisor.kickoff()))
    # reporte_final = json.loads(str(revisor.kickoff()))
    # print(reporte_final)
    
#     reporte_final =json.loads(str({
#     "Motivación_y_Participación": "Pablo muestra una motivación excepcional en clase y siempre entra contento, lo que crea un ambiente positivo. Su entusiasmo es contagioso, y se involucra activamente en todas las actividades. Disfruta especialmente de cantar y bailar las canciones, lo que no solo le ayuda a aprender, sino que también anima a sus compañeros a participar. Pablo toma la iniciativa en las actividades y siempre está dispuesto a colaborar con la profesora y sus amigos, lo que refuerza su aprendizaje en grupo.",
#     "Aprendizaje": "Pablo presenta un rendimiento sobresaliente en su aprendizaje del inglés. Tiene una comprensión excepcional y utiliza palabras clave con confianza. Se esfuerza por comunicarse en inglés y es capaz de formar estructuras completas, como demuestra con oraciones como \"I am three\" (Tengo tres años). Su pronunciación es buena, aunque puede mejorarse aún más. Pablo demuestra una gran habilidad para seguir instrucciones y hacer preguntas cuando tiene dudas, lo que refleja su deseo de aprender y entender.",
#     "Comportamiento": "El comportamiento de Pablo es ejemplar en el aula. Siempre ayuda a la profesora y colabora eficazmente con sus compañeros, lo que contribuye a un ambiente de aprendizaje armonioso. Respeta los turnos de palabra y sigue las instrucciones sin dificultad. Aunque a veces se distrae, generalmente se mantiene enfocado en las actividades. Su capacidad para cuidar el material es buena y se puede mejorar aún más con un poco más de atención hacia los recursos del aula.",
#     "Nota_de_prueba_oral": "Pablo ha obtenido una nota de 9.1 en su prueba oral, lo que refleja su dedicación y esfuerzo en el aprendizaje del inglés. Su buena pronunciación y seguridad al expresarse son evidentes, y su capacidad para usar estructuras completas le ayuda a comunicar sus ideas con claridad. Esto muestra que está bien preparado y comprometido con su aprendizaje.",
#     "Evaluación_general": "En general, Pablo ha tenido un desempeño excelente durante el curso. Se recomienda que durante el verano continúe participando en actividades que involucren canto y baile, ya que estas le ayudan a mejorar su pronunciación y fluidez. Con su actitud positiva y su entusiasmo por aprender, Pablo está bien posicionado para seguir avanzando en su aprendizaje del inglés."
# }))

    return reporte_final