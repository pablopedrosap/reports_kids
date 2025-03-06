from dotenv import load_dotenv
import os
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import io
from report_generator import generar_reporte, generar_reporte_tweens
from report_automation import ReportAutomation
import json
import os
from pydantic import BaseModel
from openai import OpenAI
from typing import Optional
import numpy as np

load_dotenv()  # This loads the .env file

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flashing messages

URL = "https://myclassroom.kidsandus.es"
ALLOWED_EXTENSIONS = {'xlsx'}
PROCESSED_STUDENTS_FILE = "all_students.txt"

# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_KEY='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'
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not set in environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import os

def save_all_reports_to_pdf(reports, output_file="Consolidated_Report.pdf"):
    """
    Save all student reports to a professional PDF format.
    
    :param reports: List of tuples (StudentData, Report as JSON or str)
    :param output_file: Name of the output PDF file
    """
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)  # Ensure the reports directory exists
    output_path = os.path.join(output_dir, output_file)
    
    # Initialize PDF document
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []  # To collect PDF elements
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = ParagraphStyle(name="Heading", fontSize=12, spaceAfter=10, bold=True)
    normal_style = styles['BodyText']
    
    # Add Title
    elements.append(Paragraph("Consolidated Student Reports", title_style))
    elements.append(Spacer(1, 12))
    
    for student, report in reports:
        # Add Student Header
        elements.append(Paragraph(f"Report for {student.data.get('student_name', 'N/A')}", heading_style))
        
        # General Information Table
        general_info = [
            ["Teacher", student.data.get('Profesora', 'N/A')],
            ["Group Name", student.data.get('Nombre grupo', 'N/A')],
            ["Category", student.category]
        ]
        table = Table(general_info, colWidths=[150, 300])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))
        
        # Report Details Section
        elements.append(Paragraph("Report Details:", heading_style))
        if isinstance(report, str):
            elements.append(Paragraph(report, normal_style))
        else:
            for section, details in report.items():
                elements.append(Paragraph(f"{section.replace('_', ' ').capitalize()}:", heading_style))
                if isinstance(details, dict):
                    for key, value in details.items():
                        elements.append(Paragraph(f"{key.capitalize()}: {value}", normal_style))
                else:
                    elements.append(Paragraph(str(details), normal_style))
                elements.append(Spacer(1, 6))
        
        # Add a spacer between reports
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("<hr width='100%'/>", normal_style))  # Horizontal line

    # Build the 
    doc.build(elements)
    print(f"Consolidated report saved as: {output_path}")


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            flash("No file part in the request.")
            return redirect(request.url)
        
        files = request.files.getlist('file')  # Retrieve all files with the name 'file'
        if not files or len(files) == 0:
            flash("No files selected for uploading.")
            return redirect(request.url)
        
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Username and password are required.")
            return redirect(request.url)

        all_reports = []  # Initialize a list to collect reports from all files
        errors = []  # To collect any errors during processing

        for file in files:
            if file.filename == '':
                errors.append("One of the files has no selected filename.")
                continue
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                try:
                    file_content = file.read()
                    df_dict = pd.read_excel(io.BytesIO(file_content), sheet_name=None, header=None)  # Read without headers
                    print(f"Processing file: {filename}")
                    reports = process_reports(df_dict, username, password)
                    all_reports.extend(reports)
                    flash(f"Successfully processed file: {filename}")
                except Exception as e:
                    error_message = f"Error processing file {filename}: {str(e)}"
                    print(error_message)
                    errors.append(error_message)
            else:
                errors.append(f"File {file.filename} has an invalid extension.")
        
        if all_reports:
            try:
                save_all_reports_to_pdf(all_reports)
                flash("All reports generated and consolidated successfully.")
            except Exception as e:
                error_message = f"Error saving consolidated reports: {str(e)}"
                print(error_message)
                errors.append(error_message)
        
        if errors:
            for error in errors:
                flash(error)
            return redirect(request.url)
        
        return "Reports generated and uploaded successfully."
    
    return render_template('upload.html')  # Ensure your upload.html supports multiple file uploads

def load_column_mapping(filepath="column_mapping.json"):
    """
    Load column mapping from a JSON configuration file.
    
    :param filepath: Path to the JSON file containing column mappings
    :return: Dictionary containing column mappings
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Column mapping file not found: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def load_processed_students():
    """Load processed student names from a text file."""
    if os.path.exists(PROCESSED_STUDENTS_FILE):
        with open(PROCESSED_STUDENTS_FILE, 'r') as file:
            # Read each line, strip any whitespace, and add to the set
            return set(line.strip() for line in file)
    return set()


def map_columns(df, column_mapping):
    """
    Map the DataFrame's columns to standardized keys based on the column_mapping.

    :param df: pandas DataFrame with the original columns
    :param column_mapping: dict mapping standardized keys to possible column names
    :return: dict mapping standardized keys to actual DataFrame column names
    """
    mapping = {}
    for key, possible_columns in column_mapping.items():
        for col in df.columns:
            if str(col).strip().lower() in [pc.lower() for pc in possible_columns]:
                mapping[key] = col
                break
    return mapping

def sanitize_student_data(student_dict):
    """
    Sanitize student data by stripping whitespace and handling data types.

    :param student_dict: Dictionary containing student data
    :return: Sanitized dictionary
    """
    sanitized_data = {}
    for key, value in student_dict.items():
        if isinstance(value, float):
            if pd.isna(value):
                sanitized_data[key] = ''
            elif value.is_integer():
                sanitized_data[key] = int(value)
            else:
                sanitized_data[key] = value  # Keep as float if not integer
        elif isinstance(value, str):
            sanitized_data[key] = value.strip()
        else:
            sanitized_data[key] = value
    return sanitized_data


def process_reports(df_dict, username, password):
    """
    Process reports from the given dictionary of DataFrames.

    :param df_dict: Dictionary where keys are sheet names (categories) and values are DataFrames
    :param username: Username for authentication
    :param password: Password for authentication
    :return: List of tuples containing StudentData and generated reports
    """
    processed_students = load_processed_students()

    automation = ReportAutomation(username, password)
    all_reports = []  # To collect all reports
    try:
        automation.login()
        current_group = None

        for category, df in df_dict.items():
            print(f"Processing category: {category}")

            # Drop completely empty rows
            df.replace('', np.nan, inplace=True)

            # Now drop rows where all elements are NaN
            df = df.dropna(how='all')
            invalid_rows = ['ANIMAL PLANET 1', 'FAIRY TAIL 1']  # Add any other invalid titles here
            df = df[~df.iloc[:, 0].astype(str).isin(invalid_rows)]

            # Limit the search to the first three rows for the header
            max_header_search_rows = 3
            header_found = False
            for potential_header_row in range(max_header_search_rows):
                if df.shape[0] <= potential_header_row:
                    break  # Not enough rows to search
                first_cell = str(df.iloc[potential_header_row, 0]).strip().lower()
                if 'centro' in first_cell:
                    header_row_index = potential_header_row
                    header_found = True
                    break

            if not header_found:
                print(f"Header containing 'Centro' not found within the first {max_header_search_rows} rows in sheet {category}")
                continue

            # Set the DataFrame's column names to the header row and drop header rows above
            df.columns = df.iloc[header_row_index]
            df = df.iloc[header_row_index + 1:]
            df = df[df.iloc[:, 0].astype(str).str.lower() != 'centro']
            df.reset_index(drop=True, inplace=True)

            # Log unmapped columns if necessary (optional)
            # print(f"Columns in {category}: {df.columns.tolist()}")

            # Process each row as student data
            for _, row in df.iterrows():
                student_dict = row.to_dict()
                student_dict = sanitize_student_data(student_dict)
                # Apply necessary filters
                center = student_dict.get('Centro', '')
                if pd.isna(center):
                    center = 'Valdebebas'
                    # continue

                course_field = str(student_dict.get('Curso', ''))

                if 'animal planet' in course_field.lower():
                    course_field = course_field
                # elif 'fairy tale' in course_field.lower():
                #     course_field = 'Tweens 2'
                else:
                    try:
                        if not course_field or any(x.lower() in course_field.lower() for x in ['fffff', '1fffff', 'anfffff']):
                            print('Skipping invalid course')
                            continue
                    except:
                        pass
                
                student_name = student_dict.get('Nombre alumno', '').strip()  

                if not student_name:
                    print("Skipping student with no name.")
                    continue

                if student_name in processed_students:
                    print(f"Skipping already processed student: {student_name}")
                    continue

                # Navigate if changing groups
                group_name = student_dict.get('Nombre grupo', '')
                if group_name != current_group:
                    current_group = group_name
                    automation.navigate_to_reports(center.split()[0], student_dict.get('Curso', ''), group_name)

                # Extract scores
                scores = automation.extract_scores(student_name, student_dict.get('term', 2), category)

                anterior_trimestre = scores

                # Update student_dict with extracted scores
                # student_dict[''] = scores.get('oral_test_score', '')
                # student_dict['written_test_score'] = scores.get('written_test_score', '')
                # student_dict['homework_score'] = scores.get('homework_score', '')

                # # Create a StudentData instance with the sanitized dictionary
                student = StudentData(student_dict, category)

                # Generate and send report
                if 'tweens' in category.lower() or 'teens' in category.lower():
                    report = generar_reporte_tweens(student, anterior_trimestre)
                else:
                    report = generar_reporte(student, anterior_trimestre)
                print("Generated Report:", report)
                all_reports.append((student, report))
                automation.enter_report(student_name, student_dict.get('term', 2), report, category)

                # Mark as processed
                with open('all_students.txt', 'a') as file:
                    file.write(f"{student_dict}\n\n\n")

                with open('all_reports.txt', 'a') as file:
                    file.write(f"{report}\n\n\n")

                processed_students.add(student_name)

        # Save updated list of processed students at the end of processing

    except Exception as e:
        print(f"An error occurred: {e}")
        raise e  # Re-raise the exception to handle it in the calling function
    finally:
        automation.close()

    return all_reports  # Return the collected reports

class StudentData:
    def __init__(self, data_dict, category):
        self.data = data_dict  # Store all student data as a dictionary
        self.category = category

        # if "1to1" or "1to2" in self.data['student_name']:
        #     save self.data['student_name'] in todo students
        #     pass 
        #     # next student
        # self.data[''] = self.data.get('Nombre alumno', '').split("1to1")[0].split("1to2")[0].strip()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
