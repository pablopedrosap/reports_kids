import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import pandas as pd
import io
from report_generator import generar_reporte, generar_reporte_tweens
from report_automation import ReportAutomation
import json

app = Flask(__name__)

URL = "https://myclassroom.kidsandus.es"
ALLOWED_EXTENSIONS = {'xlsx'}
PROCESSED_STUDENTS_FILE = "processed_students.json"

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

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
            username = request.form.get('username')
            password = request.form.get('password')

            file_content = file.read()
            df_dict = pd.read_excel(io.BytesIO(file_content), sheet_name=None, header=None)  # Read without headers

            category_column_names = {
                'Tweens': [
                    'Centro', 'Nombre grupo', 'Curso', 'Profesora', 'Nombre alumno', 'Audio Listening Frequency',
                    'Oral Test Score', 'Comentario oral test', 'Written Test Score', 'Comentario written test', 'My Way',
                    'Behaviour: rating', 'Behaviour: Entra contento a clase', 'Behaviour: Actitud positiva',
                    'Behaviour: Entusiasmo', 'Behaviour: Toma iniciativa', 'Behaviour: Dato diferenciador',
                    'Behaviour: puntos a mejorar', 'Behaviour: puntos fuertes', 'Behaviour: Tiene amigos en clase',
                    'Behaviour: Se distrae', 'Behaviour: Colabora con compañeros', 'Behaviour: Respeta turnos palabra',
                    'Behaviour: Cuida material', 'Behaviour: qué se ha hecho si tiene mal comportamiento',
                    'Behaviour: puntos a mejorar', 'Behaviour: puntos fuertes', 'Work: rating', 'Work: Participa',
                    'Work: Actividades preferidas', 'Work: Buena pronunciación',
                    'Work: Se esfuerza por comunicarse en inglés', 'Work: Se expresa con seguridad', 'Work: Pregunta dudas',
                    'Work: Ayuda a la profe', 'Work: Sigue instrucciones', 'Performance: rating', 'Perfomance: Comprende',
                    'Perfomance: Usa palabaras clave', 'Perfomance: Hace estructuras completas',
                    'Perfomance: Ejemplo de oraciones que hace', 'Perfomance: puede deletrear correctamente',
                    'Perfomance: puntos fuertes', 'Perfomance:  puntos a mejorar', 'Homework', 'Comentario Homework'
                ],
                'B&B': [
                    'Centro', 'Nombre grupo', 'Curso', 'Profesora', 'Nombre alumno', 'Oral Test Score',
                    'Comentario oral test', 'Written Test Score', 'Comentario written test', 'Motivation & Participation: rating',
                    'Motivation & Participation: Participa', 'Motivation & Participation: Entra contento a clase',
                    'Motivation & Participation: Actitud positiva', 'Motivation & Participation: Entusiasmo',
                    'Motivation & Participation: Toma iniciativa', 'Motivation & Participation: canta las canciones',
                    'Motivation & Participation: Dato diferenciador', 'Motivation & Participation: puntos a mejorar',
                    'Motivation & Participation: puntos fuertes', 'Motivation & Participation: Actividades preferidas',
                    'Learning: rating', 'Learning: Comprende ', 'Learning: Usa palabaras clave',
                    'Learning: Hace estructuras completas', 'Learning: Ejemplo de oraciones que hace',
                    'Learning: Buena pronunciación', 'Learning: Se esfuerza por comunicarse en inglés',
                    'Learning: Se expresa con seguridad', 'Learning: puede deletrear correctamente',
                    'Learning: puntos fuertes', 'Learning: puntos a mejorar', 'Learning: Pregunta dudas',
                    'Behaviour: rating', 'Behaviour: Ayuda a la profe', 'Behaviour: Tiene amigos en clase',
                    'Behaviour: Se distrae', 'Behaviour: Colabora con compañeros', 'Behaviour: Sigue instrucciones',
                    'Behaviour: Respeta turnos palabra', 'Behaviour: Cuida material',
                    'Behaviour: qué se ha hecho si tiene mal comportamiento', 'Behaviour: puntos a mejorar',
                    'Behaviour: puntos fuertes'
                ],
                'default': [
                    "Centro", "Nombre grupo", "Curso", "Profesora", "Nombre alumno",
                    "Audio Listening Frequency", "Oral Test Score", "Comentario oral test", "Written Test Score",
                    "Comentario written test", "Motivation & Participation: rating", "Motivation & Participation: Participa",
                    "Motivation & Participation: Entra contento a clase", "Motivation & Participation: Actitud positiva",
                    "Motivation & Participation: Entusiasmo", "Motivation & Participation: Toma iniciativa",
                    "Motivation & Participation: baila las canciones", "Motivation & Participation: puntos a mejorar",
                    "Motivation & Participation: puntos fuertes", "Motivation & Participation: Actividades preferidas",
                    "Learning: rating", "Learning: Comprende", "Learning: Usa palabras clave",
                    "Learning: Hace estructuras completas", "Learning: Ejemplo de oraciones que hace",
                    "Learning: Buena pronunciación", "Learning: Se esfuerza por comunicarse en inglés",
                    "Learning: Se expresa con seguridad", "Learning: puntos fuertes", "Learning: puntos a mejorar",
                    "Learning: Pregunta dudas", "Behaviour: rating", "Behaviour: Ayuda a la profe",
                    "Behaviour: Tiene amigos en clase", "Behaviour: Se distrae (0 no se distrae y 10 se distrae mucho)",
                    "Behaviour: Colabora con compañeros", "Behaviour: Sigue instrucciones", "Behaviour: Respeta turnos palabra",
                    "Behaviour: Cuida material", "Behaviour: qué se ha hecho si tiene mal comportamiento",
                    "Behaviour: puntos a mejorar", "Behaviour: puntos fuertes"
                ]
            }

            # Process reports for each sheet
            process_reports(df_dict, username, password, category_column_names)

            return "Reports generated and uploaded successfully."
    return render_template('upload.html')

def load_processed_students():
    """Load processed student names from a text file."""
    if os.path.exists('names.txt'):
        with open('names.txt', 'r') as file:
            # Read each line, strip any whitespace, and add to the set
            return set(line.strip() for line in file)
    return set()

def save_processed_students(processed_students):
    """Save processed student names to a text file."""
    with open(PROCESSED_STUDENTS_FILE, 'w') as file:
        for student_name in processed_students:
            file.write(f"{student_name}\n")

def process_reports(df_dict, username, password, category_column_names):
    processed_students = load_processed_students()
    automation = ReportAutomation(username, password)
    try:
        automation.login()
        current_group = None

        for category, df in df_dict.items():
            print(f"Processing category: {category}")

            # Get the column names for this category
            if category in category_column_names:
                column_names = category_column_names[category]
            else:
                column_names = category_column_names['default']

            # Drop completely empty rows
            df = df.dropna(how='all')

            # Find the header row index where 'Centro' appears in the first column
            header_row_index = df[df.iloc[:, 0] == 'Centro'].index
            if len(header_row_index) == 0:
                print(f"Header 'Centro' not found in sheet {category}")
                continue
            header_row_index = header_row_index[0]

            # Set the DataFrame's column names to the header row and drop header rows
            df.columns = df.iloc[header_row_index]
            df = df.iloc[header_row_index + 1:]
            df = df[df.iloc[:, 0] != 'Centro']
            df.reset_index(drop=True, inplace=True)

            # Ensure `column_names` matches the actual number of columns in `df`
            actual_columns = len(df.columns)
            if actual_columns > len(column_names):
                # Add placeholders for extra columns
                extended_column_names = column_names + [f"Extra_{i}" for i in range(1, actual_columns - len(column_names) + 1)]
            else:
                extended_column_names = column_names[:actual_columns]

            # Assign the adjusted column names to `df`
            df.columns = extended_column_names

            # Process each row as student data
            for _, row in df.iterrows():
                student = StudentData(row, category)

                # Check if the student has already been processed
                if student.student_name in processed_students:
                    print(f"Skipping already processed student: {student.student_name}")
                    continue

                # Navigate if changing groups
                if student.group_name != current_group:
                    current_group = student.group_name
                    automation.navigate_to_reports(student.center, student.course, student.group_name)

                scores = automation.extract_scores(student.student_name, student.term, student.category)

                # Set the extracted scores in the student object
                student.oral_test_score = scores.get('oral_test_score')
                student.written_test_score = scores.get('written_test_score')
                student.homework_score = scores.get('homework_score')
                print(f"Assigned scores for {student.student_name}: {vars(student)}")

                # Generate and send report
                print(student.category)
                if 'tweens' in str(student.category.lower()):
                    report = generar_reporte_tweens(student)
                else:
                    report = generar_reporte(student) 
                print("Generated Report:", report)
                automation.enter_report(student.student_name, student.term, report, student.category)

                # Add student to processed list
                processed_students.add(student.student_name)

        # Save updated list of processed students at the end of processing
        save_processed_students(processed_students)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        automation.close()

class StudentData:
    def __init__(self, row, category):
        self.term = 1
        self.center = row.get('Centro', '').split()[0]
        self.group_name = row.get('Nombre grupo', '')
        self.course = row.get('Curso', '')
        self.professor = row.get('Profesora', '')
        self.student_name = row.get('Nombre alumno', '')
        if "1to1" in self.student_name:
            self.student_name = self.student_name.split("1to1", 1)[0].strip()
            print(f"Modified student_name: {self.student_name}")
        self.audio_listening_frequency = row.get('Audio Listening Frequency', '')
        self.oral_test_score = row.get('Oral Test Score', '')
        self.oral_test_comment = row.get('Comentario oral test', '')
        self.written_test_score = row.get('Written Test Score', '')
        self.written_test_comment = row.get('Comentario written test', '')

        self.global_score = ''
        self.homework_score = ''
        self.global_score_comment = ''

        self.my_way = row.get('My Way', '')


        # Motivation & Participation Section (default category)
        self.motivation_rating = row.get('Motivation & Participation: rating', '')
        self.participates = row.get('Motivation & Participation: Participa', '')
        self.enters_happy = row.get('Motivation & Participation: Entra contento a clase', '')
        self.positive_attitude = row.get('Motivation & Participation: Actitud positiva', '')
        self.enthusiasm = row.get('Motivation & Participation: Entusiasmo', '')
        self.initiative = row.get('Motivation & Participation: Toma iniciativa', '')
        self.differentiator = row.get('Motivation & Participation: Dato diferenciador', '')
        self.motivation_improvement_points = row.get('Motivation & Participation: puntos a mejorar', '')
        self.motivation_strong_points = row.get('Motivation & Participation: puntos fuertes', '')
        self.preferred_activities = row.get('Motivation & Participation: Actividades preferidas', '')

        # Additional fields for 'B&B' category
        self.sings_songs = row.get('Motivation & Participation: canta las canciones', '')
        self.dances_songs = row.get('Motivation & Participation: baila las canciones', '')

        # Learning Section
        self.learning_rating = row.get('Learning: rating', '')
        self.understands = row.get('Learning: Comprende', '')
        self.uses_keywords = row.get('Learning: Usa palabras clave', '') or row.get('Learning: Usa palabaras clave', '')
        self.makes_complete_structures = row.get('Learning: Hace estructuras completas', '')
        self.example_sentences = row.get('Learning: Ejemplo de oraciones que hace', '')
        self.good_pronunciation = row.get('Learning: Buena pronunciación', '')
        self.efforts_to_communicate = row.get('Learning: Se esfuerza por comunicarse en inglés', '')
        self.confident_expression = row.get('Learning: Se expresa con seguridad', '')
        self.spells_correctly = row.get('Learning: puede deletrear correctamente', '')
        self.learning_strong_points = row.get('Learning: puntos fuertes', '')
        self.learning_improvement_points = row.get('Learning: puntos a mejorar', '')
        self.asks_questions = row.get('Learning: Pregunta dudas', '')

        # Behaviour Section
        self.behavior_rating = row.get('Behaviour: rating', '')
        self.helps_teacher = row.get('Behaviour: Ayuda a la profe', '')
        self.has_friends_in_class = row.get('Behaviour: Tiene amigos en clase', '')
        self.gets_distracted = row.get('Behaviour: Se distrae', '')
        self.collaborates_with_peers = row.get('Behaviour: Colabora con compañeros', '')
        self.follows_instructions = row.get('Behaviour: Sigue instrucciones', '')
        self.respects_turns = row.get('Behaviour: Respeta turnos palabra', '')
        self.cares_for_materials = row.get('Behaviour: Cuida material', '')
        self.misbehavior_action = row.get('Behaviour: qué se ha hecho si tiene mal comportamiento', '')
        self.behavior_improvement_points = row.get('Behaviour: puntos a mejorar', '')
        self.behavior_strong_points = row.get('Behaviour: puntos fuertes', '')

        # Work Section (for 'tweens' category)
        self.work_rating = row.get('Work: rating', '')
        self.work_participates = row.get('Work: Participa', '')
        self.work_preferred_activities = row.get('Work: Actividades preferidas', '')
        self.work_good_pronunciation = row.get('Work: Buena pronunciación', '')
        self.work_efforts_to_communicate = row.get('Work: Se esfuerza por comunicarse en inglés', '')
        self.work_confident_expression = row.get('Work: Se expresa con seguridad', '')
        self.work_asks_questions = row.get('Work: Pregunta dudas', '')
        self.work_helps_teacher = row.get('Work: Ayuda a la profe', '')
        self.work_follows_instructions = row.get('Work: Sigue instrucciones', '')

        # Performance Section (for 'tweens' category)
        self.performance_rating = row.get('Performance: rating', '')
        self.performance_understands = row.get('Perfomance: Comprende', '')
        self.performance_uses_keywords = row.get('Perfomance: Usa palabaras clave', '')
        self.performance_makes_complete_structures = row.get('Perfomance: Hace estructuras completas', '')
        self.performance_example_sentences = row.get('Perfomance: Ejemplo de oraciones que hace', '')
        self.performance_spells_correctly = row.get('Perfomance: puede deletrear correctamente', '')
        self.performance_strong_points = row.get('Perfomance: puntos fuertes', '')
        self.performance_improvement_points = row.get('Perfomance:  puntos a mejorar', '')

        # Homework Section
        self.homework = row.get('Homework', '')
        self.homework_comment = row.get('Comentario Homework', '')

        # Category (Sheet name)
        self.category = category

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
