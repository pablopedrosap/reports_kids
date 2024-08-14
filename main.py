
import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import pandas as pd
import io
from report_generator import generar_reporte
from report_automation import ReportAutomation

app = Flask(__name__)

URL = "https://myclassroom.kidsandus.es"
ALLOWED_EXTENSIONS = {'xlsx'}

os.environ["OPENAI_API_KEY"] = "sk-proj-NjHbqyLxpNxiSaFScgZ6T3BlbkFJiQMnjU87TfIHSBZPSsMR"
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
            
            # Read the file directly into memory
            file_content = file.read()
            df = pd.read_excel(io.BytesIO(file_content))
            
            # Process reports
            process_reports(df, username, password)
            
            return "Reports generated and uploaded successfully."
    return render_template('upload.html')

def process_reports(df, username, password):
    automation = ReportAutomation(username, password)
    try:
        automation.login()
        for _, row in df.iterrows():
            student = StudentData(row)
            automation.navigate_to_reports(student.school, student.course, student.professor)
            report = generar_reporte(student)
            automation.enter_report(student.name, student.term, report)
            print(f"Report sent for {student.name}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        automation.close()

class StudentData:
    def __init__(self, row):
        self.name = row['Nombre completo']
        self.school = 'Valdebebas'
        self.course = row['Cursos']
        self.group = ''
        self.term = row.get('TERM 1', '')
        self.schedule = row['Horario']
        self.term1 = row['TERM 1']
        self.term2 = row.get('TERM 2', '')
        self.term3 = row.get('TERM 3', '')
        self.participates = row['Participa']
        self.enters_happy = row['Entra contento a clase']
        self.positive_attitude = row['Actitud positiva']
        self.enthusiasm = row['Entusiasmo']
        self.takes_initiative = row['Toma iniciativa']
        self.preferred_activities = row['Actividades preferidas']
        self.understands = ''
        self.professor = 'Julia'
        self.absences = 0
        self.listening_frequency = 'Suficiente'
        self.oral_test_score = ''
        self.writing_score = ''
        self.homework_score = ''
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
