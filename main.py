
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
PROCESSED_STUDENTS_FILE = "processed_students.json"

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

            # Read all sheets from the Excel file without specifying headers
            file_content = file.read()
            df_dict = pd.read_excel(io.BytesIO(file_content), sheet_name=None, header=None)  # Read without headers

            # Define consistent column names
            column_names = [
                "Centro", "Nombre grupo", "Curso", "Profesora", "Nombre alumno", 
                "Audio Listening Frequency", "Oral Test Score", "Comentario oral test",
                "Motivation & Participation: rating", "Motivation & Participation: Participa",
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

            # Process reports for each sheet
            process_reports(df_dict, username, password, column_names)

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

def process_reports(df_dict, username, password, column_names):
    processed_students = load_processed_students()
    automation = ReportAutomation(username, password)
    try:
        automation.login()
        current_group = None

        for category, df in df_dict.items():
            print(f"Processing category: {category}")

            # Drop completely empty rows
            df = df.dropna(how='all')

            # Find the header row index where 'Centro' appears in the first column
            header_row_index = df[df.iloc[:, 0] == 'Centro'].index
            if len(header_row_index) == 0:
                print(f"Header 'Centro' not found in sheet {category}")
                continue  # Skip this sheet if header not found
            header_row_index = header_row_index[0]  # Get the first occurrence

            # Set the DataFrame's column names to the header row
            df.columns = df.iloc[header_row_index]
            # Drop all rows up to and including the header row
            df = df.iloc[header_row_index + 1:]

            # Remove any rows that are duplicate headers within the data
            df = df[df.iloc[:, 0] != 'Centro']

            # Reset index
            df.reset_index(drop=True, inplace=True)

            # Assign consistent column names (truncate if fewer columns)
            df.columns = column_names[:len(df.columns)]

            # Print headers for debugging
            print("Headers after processing:")
            print(df.columns)

            # Process each row as student data
            for _, row in df.iterrows():
                student = StudentData(row, category)
                print("Student Data:", vars(student))

                # Navigate if changing groups
                if student.student_name in processed_students:
                    print(f"Skipping already processed student: {student.student_name}")
                    continue
                if student.group_name != current_group:
                    current_group = student.group_name
                    automation.navigate_to_reports(student.center, student.course, student.group_name)

                # Generate and send report
                report = generar_reporte(student)
                # report = '''{'Motivación_y_Participación': {'Rating': 'Very Good', 'Comment': 'Elisa muestra una participación activa y entusiasta en clase. Se destaca por su energía positiva, entrando siempre con entusiasmo que contagia a sus compañeros. Aunque a veces puede dispersarse, Elisa compensa esto con una notable disposición para iniciar actividades, especialmente aquellas que implican explorar nuevos términos en inglés. Se siente particularmente atraída por actividades grupales, donde puede interactuar y compartir ideas con su grupo de amigos. Su carácter extrovertido y curioso la distingue como una presencia vibrante en cada sesión.'}, 
                # 'Aprendizaje': {'Rating': 'Very Good', 'Comment': 'Elisa ha demostrado una buena comprensión de las estructuras básicas del inglés, utilizando frases como "I like to play with my friends" (Me gusta jugar con mis amigos). Aunque su uso de palabras clave ha sido adecuado, hay margen para el fortalecimiento de estructuras complejas y la expansión de su vocabulario. Elisa no duda en formular preguntas cuando encuentra dificultades, lo que refleja su constructiva curiosidad. Continúa esforzándose por comunicarse en inglés y su pronunciación ha mejorado notablemente. Un enfoque más centrado en la práctica oral y auditiva la beneficiaría aún más.'}, 
                # 'Comportamiento': {'Rating': 'Excellent', 'Comment': 'El comportamiento de Elisa en clase es ejemplar. Respeta los turnos de palabra de manera consistente y demuestra gran colaboración con sus compañeros, lo que provoca un entorno armónico y productivo. Su capacidad para ayudar a sus compañeros y colaborar con la profesora, como cuando organiza materiales, es uno de sus puntos más destacados. Elisa sigue las instrucciones con precisión y cuida el material con esmero, manteniendo siempre en mente el bienestar común de su grupo de estudio. Esta actitud positiva y cooperativa la convierte en un miembro indispensable para su grupo de clase.'}, 
                # 'Nota_de_prueba_oral': 'Aunque los datos de la prueba oral de Elisa no están disponibles, su creciente habilidad para articular sus pensamientos en inglés sugiere que está progresando bien en esta área. Se recomienda continuar practicando inglés conversacional mediante el uso de frases "I can help you" (Puedo ayudarte) y "What is your name?" (¿Cuál es tu nombre?), permitiéndole ganar más confianza en sus habilidades orales.', 
                # 'Evaluación_general': 'El rendimiento general de Elisa durante este término ha sido notable. Su comportamiento proactivo y positivo se traduce directamente en sus experiencias de aprendizaje. Se evidencia un buen uso de estructuras básicas del inglés, aunque podría beneficiarse de más práctica en el uso de frases complejas y enriquecimiento de vocabulario. Sugiero que durante el verano, Elisa continúe exponiéndose al inglés mediante audiolibros y conversaciones con hablantes nativos. Con estas estrategias, Elisa podrá seguir desarrollando sus habilidades lingüísticas y mantener su entusiasmo por el idioma en el futuro académico.'}'''
                # report = json.loads(report)
                print("Generated Report:", report)
                automation.enter_report(student.student_name, student.term, report)
                print(f"Report sent for {student.student_name} in {category}")
                processed_students.add(student.student_name)
            save_processed_students(processed_students)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        automation.close()

class StudentData:
    def __init__(self, row, category):
        self.term = 1  # Set this dynamically if needed
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

        # Motivation & Participation Section
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

        # Learning Section
        self.learning_rating = row.get('Learning: rating', '')
        self.understands = row.get('Learning: Comprende', '')
        self.uses_keywords = row.get('Learning: Usa palabras clave', '')
        self.makes_complete_structures = row.get('Learning: Hace estructuras completas', '')
        self.example_sentences = row.get('Learning: Ejemplo de oraciones que hace', '')
        self.good_pronunciation = row.get('Learning: Buena pronunciación', '')
        self.efforts_to_communicate = row.get('Learning: Se esfuerza por comunicarse en inglés', '')
        self.confident_expression = row.get('Learning: Se expresa con seguridad', '')
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

        # Homework Section
        self.homework = row.get('Homework', '')
        self.homework_comment = row.get('Comentario Homework', '')

        # Category (Sheet name)
        self.category = category


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))




