import time
from playwright.sync_api import sync_playwright
import pandas as pd
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os
import json
from playwright.sync_api import sync_playwright

URL = "https://myclassroom.kidsandus.es"
EXCEL_FILE = "students.xlsx"

os.environ["OPENAI_API_KEY"] = "sk-proj-NjHbqyLxpNxiSaFScgZ6T3BlbkFJiQMnjU87TfIHSBZPSsMR"
os.environ["SERPER_API_KEY"] = "88ae5974658b41cd2af65d4064455f9b9b3f57e4"
os.environ['CLAUDE_API_KEY'] = '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'

llm4o = ChatOpenAI(model="gpt-4o")
llm4o_mini = ChatOpenAI(model="gpt-4o-mini")

class StudentData:
    def __init__(self, row):
        self.name = row['Nombre completo']
        self.school = 'Valdebebas'  # Asumiendo que esto no está proporcionado en la hoja de Excel
        self.course = row['Cursos']
        self.group = ''  # Asumiendo que esto no está proporcionado en la hoja de Excel
        self.term = row.get('TERM 1', '')  # Asumiendo que TERM 1 es el predeterminado, ajusta según sea necesario
        self.schedule = row['Horario']
        self.term1 = row['TERM 1']
        self.term2 = row.get('TERM 2', '')  # En caso de que TERM 2 esté vacío o falte
        self.term3 = row.get('TERM 3', '')  # En caso de que TERM 3 esté vacío o falte
        self.participates = row['Participa']
        self.enters_happy = row['Entra contento a clase']
        self.positive_attitude = row['Actitud positiva']
        self.enthusiasm = row['Entusiasmo']
        self.takes_initiative = row['Toma iniciativa']
        self.preferred_activities = row['Actividades preferidas']
        self.understands = ''
        self.professor = 'Julia'  
        self.absences = 0  # Asumiendo que esto no está proporcionado en la hoja de Excel
        self.listening_frequency = 'Suficiente'  # Asumiendo que esto no está proporcionado en la hoja de Excel
        self.oral_test_score = ''  # Asumiendo que esto no está proporcionado en la hoja de Excel
        self.writing_score = ''  # Asumiendo que esto no está proporcionado en la hoja de Excel
        self.homework_score = ''  # Asumiendo que esto no está proporcionado en la hoja de Excel

        # Campos adicionales según las columnas de tu hoja de Excel
        self.uses_key_words = ''
        self.makes_complete_structures = row['Hace estructuras completas']
        self.example_sentences = row['Ejemplo de oraciones que hace']
        self.good_pronunciation = row['Buena pronunciación']
        self.efforts_to_communicate = row['Se esfuerza por comunicarse en inglés']
        self.confident_expression = row['Se expresa con seguridad']
        self.asks_questions = row['Pregunta dudas']
        self.helps_teacher = row['Ayuda a la profe']
        self.has_friends_in_class = row['Tiene amigos en clase']
        self.gets_distracted = row['Se distrae']
        self.collaborates_with_peers = row['Colabora con compañeros']
        self.follows_instructions = row['Sigue instrucciones']
        self.respects_turns = row['Respeta turnos palabra']
        self.cares_for_materials = row['Cuida material']

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
        expected_output="json"  # Especifica que la salida debe ser en formato JSON
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

    # Inicia la tarea y almacena la salida JSON
    reporte_salida = equipo.kickoff()
    print(reporte_salida)
    reporte_salida = json.loads(reporte_salida)
    print(reporte_salida)
    # Reformatar el JSON para que coincida con la estructura del informe
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

    # Guardar la salida JSON formateada en un archivo
    with open(f"{student.name}_reporte.json", "w") as f:
        json.dump(informe_formateado, f, indent=4)

    return informe_formateado

class ReportAutomation:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)  # Let Playwright manage the Chromium binary
        self.page = self.browser.new_page()


    def login(self):
        self.page.goto(URL)
        self.page.fill('#login_user', self.username)
        self.page.fill('#login_pass', self.password)
        self.page.click('#login_button')
        self.page.wait_for_load_state('networkidle')

    def select_school(self, school_name):
        school_selector = f'.li_school:has-text("{school_name}")'
        self.page.click(school_selector)

    def select_course(self, course_name):
        course_selector = f'.li_course:has-text("{course_name}")'
        self.page.click(course_selector)

    def select_group(self, professor):
        group_selector = f'.li_group'
        elements = self.page.query_selector_all(group_selector)
        print(elements)
        
        for element in elements:
            text = element.inner_text()
            print(f"Checking element with text: {text}")  # Debugging line
            if professor.lower() in text.lower():
                element.click()
                break


    def click_begin(self):
        self.page.click('#selector_button')
        self.page.wait_for_load_state('networkidle')

    def navigate_to_term_reports(self):
        self.page.click('.hamb')
        self.page.click('.menu_obj2')
        self.page.wait_for_load_state('networkidle')

    def navigate_to_reports(self, school, course, professor):
        self.select_school(school)
        self.select_course(course)
        self.select_group(professor)
        self.click_begin()
        self.navigate_to_term_reports()

    def enter_report(self, student_name, term, report):
        student_row = self.page.locator(f'tr:has-text("{student_name}")')
        term_column = 1 if term == 1 else (2 if term == 2 else 3)
        edit_button = student_row.locator(f'td:nth-child({term_column + 1}) .edit-icon')
        edit_button.click()

        self.page.wait_for_selector('.report-input')

        sections = [
            'motivación-participación',
            'aprendizaje',
            'comportamiento',
            'nota-de-prueba-oral',
            'evaluación-general'
        ]

        for section in sections:
            self.page.fill(f'.{section}', report[section.replace(' ', '_')])

        # self.page.click('.save-report-button')
        self.page.wait_for_load_state('networkidle')

        # Finalizar el informe
        self.page.click('.finish-report-button')
        self.page.wait_for_load_state('networkidle')

    def close(self):
        self.browser.close()
        self.playwright.stop()


def load_students():
    df = pd.read_excel(EXCEL_FILE)
    return [StudentData(row) for _, row in df.iterrows()]

def main():
    username = 'danielaaccetta'
    password = '1739'

    automation = ReportAutomation(username, password)

    try:
        automation.login()

        for student in load_students():
            automation.navigate_to_reports(student.school, student.course, student.professor)
            report = generar_reporte(student)
            
            automation.enter_report(student.name, student.term, report)
            
            print(f"Reporte enviado para {student.name}")
            time.sleep(2) 

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
    finally:
        automation.close()

if __name__ == "__main__":
    main()
