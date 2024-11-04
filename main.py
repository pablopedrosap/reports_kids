
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import pandas as pd
import io
from report_generator import generar_reporte
from report_automation import ReportAutomation
import json

app = Flask(__name__)


URL = "https://myclassroom.kidsandus.es"
ALLOWED_EXTENSIONS = {'xlsx'}

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPER_API_KEY"] = "88ae5974658b41cd2af65d4064455f9b9b3f57e4"
os.environ['CLAUDE_API_KEY'] = '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'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            username = request.form.get('username')
            password = request.form.get('password')

            # Leer todas las hojas del archivo Excel, omitiendo la primera fila
            file_content = file.read()
            df_dict = pd.read_excel(io.BytesIO(file_content), sheet_name=None, header=1)  # Empezar desde la segunda fila

            # Procesar informes para cada hoja (categoría)
            process_reports(df_dict, username, password)

            return "Reports generated and uploaded successfully."
    return render_template('upload.html')

def process_reports(df_dict, username, password):
    automation = ReportAutomation(username, password)
    try:
        automation.login()

        current_group = None
        for category, df in df_dict.items():
            # Eliminar filas completamente vacías
            df = df.dropna(how='all')   
            
            # Eliminar filas duplicadas de cabeceras
            df = df[~df.iloc[:, 0].str.contains('Centro', na=False)]

            # Limpiar espacios en blanco en los nombres de las columnas
            df.columns = df.columns.str.strip()  
            print(df)
            
            print(f"Procesando la categoría: {category}")
            for _, row in df.iterrows():
                student = StudentData(row, category)
                if student.group_name != current_group:
                    # Update the current group and navigate
                    current_group = student.group_name
                    automation.navigate_to_reports(student.center, student.course, student.group_name)
                
                report = generar_reporte(student)
                print(report)
                # report = json.loads('''{
                #     "Motivación_y_Participación": {
                #         "Rating": "Excellent",
                #         "Comment": "Pablo muestra una motivación sobresaliente en clase. Siempre entra contento y participa con gran entusiasmo en todas las actividades. Su actitud positiva es evidente, y no duda en tomar la iniciativa al proponer ideas y participar en dinámicas grupales. Pablo disfruta especialmente de cantar y bailar las canciones, lo cual fomenta un ambiente alegre y dinámico en el aula. Su capacidad para involucrarse en las actividades lo convierte en un líder natural entre sus compañeros."
                #     },
                #     "Aprendizaje": {
                #         "Rating": "Very good",
                #         "Comment": "En términos de aprendizaje, Pablo ha demostrado una comprensión excepcional. Utiliza estructuras completas en sus oraciones, como 'I am three' (Tengo tres años), lo que refleja su dominio del vocabulario y la gramática básica. Su capacidad para comprender instrucciones y usar palabras clave es notable, lo que le permite participar activamente en las discusiones. Aunque su pronunciación es buena, hay espacio para seguir mejorando, pero su esfuerzo por comunicarse en inglés es admirable."
                #     },
                #     "Comportamiento": {
                #         "Rating": "Very good",
                #         "Comment": "El comportamiento de Pablo es ejemplar. Siempre ayuda a la profesora y colabora de manera efectiva con sus compañeros. Respeta los turnos de palabra y sigue las instrucciones sin problemas, lo que contribuye a un ambiente de aprendizaje positivo. Aunque, en ocasiones, puede distraerse, su capacidad para regresar a la actividad es rápida. Este comportamiento proactivo y su disposición para ayudar lo hacen un alumno valioso en el aula."
                #     },
                #     "Nota_de_prueba_oral": "Pablo ha obtenido una nota de 9.1 en su prueba oral, lo que refleja su dedicación y habilidades de comunicación. Su buena pronunciación, junto con su confianza al hablar, le permite expresarse con claridad. Además, pregunta dudas cuando es necesario, demostrando su interés en profundizar su comprensión del idioma.",
                #     "Evaluación_general": "En general, Pablo ha tenido un desempeño excelente durante este año escolar. Se recomienda que durante el verano continúe practicando su pronunciación y participe en actividades que le permitan seguir desarrollando su seguridad al comunicarse en inglés. Su actitud positiva y su entusiasmo son cruciales para su éxito continuo en el aprendizaje del idioma."
                # }''')
                
                automation.enter_report(student.student_name, student.term, report)
                print(f"Report sent for {student.student_name} in {category}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        automation.close()

class StudentData:
    def __init__(self, row, category):
        self.term=1
        self.center = row.get('Centro', '')
        self.group_name = row.get('Nombre grupo', '')
        self.course = row.get('Curso', '')
        self.professor = row.get('Profesora', '')
        self.student_name = row.get('Nombre alumno', '')
        self.audio_listening_frequency = row.get('Audio Listening Frequency', '')
        self.oral_test_score = row.get('Oral Test Score', '')
        self.oral_test_comment = row.get('Comentario oral test', '')
        self.written_test_score = row.get('Written Test Score', '')
        self.written_test_comment = row.get('Comentario written test', '')
        
        # Behaviour Section
        self.behavior_rating = row.get('Behaviour: rating', '')
        self.enters_happy = row.get('Behaviour: Entra contento a clase', '')
        self.positive_attitude = row.get('Behaviour: Actitud positiva', '')
        self.enthusiasm = row.get('Behaviour: Entusiasmo', '')
        self.initiative = row.get('Behaviour: Toma iniciativa', '')
        self.differentiator = row.get('Behaviour: Dato diferenciador', '')
        self.behavior_improvement_points = row.get('Behaviour: puntos a mejorar', '')
        self.behavior_strong_points = row.get('Behaviour: puntos fuertes', '')
        self.has_friends_in_class = row.get('Behaviour: Tiene amigos en clase', '')
        self.gets_distracted = row.get('Behaviour: Se distrae', '')
        self.collaborates_with_peers = row.get('Behaviour: Colabora con compañeros', '')
        self.respects_turns = row.get('Behaviour: Respeta turnos palabra', '')
        self.cares_for_materials = row.get('Behaviour: Cuida material', '')
        self.misbehavior_action = row.get('Behaviour: qué se ha hecho si tiene mal comportamiento', '')

        # Work Section
        self.work_rating = row.get('Work: rating', '')
        self.participates = row.get('Work: Participa', '')
        self.preferred_activities = row.get('Work: Actividades preferidas', '')
        self.good_pronunciation = row.get('Work: Buena pronunciación', '')
        self.efforts_to_communicate = row.get('Work: Se esfuerza por comunicarse en inglés', '')
        self.confident_expression = row.get('Work: Se expresa con seguridad', '')
        self.asks_questions = row.get('Work: Pregunta dudas', '')
        self.helps_teacher = row.get('Work: Ayuda a la profe', '')
        self.follows_instructions = row.get('Work: Sigue instrucciones', '')

        # Performance Section
        self.performance_rating = row.get('Performance: rating', '')
        self.understands = row.get('Perfomance: Comprende', '')
        self.uses_keywords = row.get('Perfomance: Usa palabaras clave', '')
        self.makes_complete_structures = row.get('Perfomance: Hace estructuras completas', '')
        self.example_sentences = row.get('Perfomance: Ejemplo de oraciones que hace', '')
        self.spells_correctly = row.get('Perfomance: puede deletrear correctamente', '')
        self.strong_points_performance = row.get('Perfomance: puntos fuertes', '')
        self.improvement_points_performance = row.get('Perfomance: puntos a mejorar', '')

        # Homework Section
        self.homework = row.get('Homework', '')
        self.homework_comment = row.get('Comentario Homework', '')

        # Category (Sheet name)©
        self.category = category


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))



'''
Stripe Payment: Franchise completes payment via Stripe.
Send File to Dockerized Service: Slack bot sends the file to a Dockerized service running on Google Cloud Run.
Process File with Playwright: The Docker container, equipped with Playwright, processes the Excel file, generates the report by interacting with a webpage.
Generate Report on Webpage: Playwright automates the generation of the report within the webpage.
'''



