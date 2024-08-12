import time
from playwright.sync_api import sync_playwright
import pandas as pd
from crewai import Agent, Task, Crew

# Constants
URL = "https://myclassroom.kidsandus.es"
EXCEL_FILE = "students.xlsx"

class StudentData:
    def __init__(self, row):
        self.name = row['Name']
        self.school = row['School']
        self.course = row['Cursos']
        self.group = row['Group']
        self.term = row['Term']
        self.schedule = row['Horario']
        self.term1 = row['TERM 1']
        self.term2 = row['TERM 2']
        self.term3 = row['TERM 3']
        self.participates = row['Participa']
        self.enters_happy = row['Entra contento a clase']
        self.positive_attitude = row['Actitud positiva']
        self.enthusiasm = row['Entusiasmo']
        self.takes_initiative = row['Toma iniciativa']
        self.preferred_activities = row['Actividades preferidas']
        self.understands = row['Comprende']
        self.professor = row.get('Professor', '')
        self.absences = row.get('Absences', 0)
        self.listening_frequency = row.get('Listening Frequency', 'Suficiente')
        self.oral_test_score = row.get('Oral Test Score', '')
        self.writing_score = row.get('Writing Score', '')
        self.homework_score = row.get('Homework Score', '')

def generate_report(student):
    writer_agent = Agent(
        role="Report Writer",
        goal="Write detailed and personalized student reports following the Definition of Done",
        backstory="You are an experienced educator who writes insightful reports on student progress.",
        allow_delegation=False
    )
    
    task_description = f"""
    Write a detailed report for {student.name} based on their performance data.
    Follow these guidelines from the Definition of Done:
    1. Make the report personalized and reflect the student's character and learning style.
    2. Each section should be at least 300 characters long.
    3. Use the student's name at least once in each section.
    4. Include examples of activities the student enjoys and structures they've learned, with translations.
    5. Always provide translations for English phrases or words in parentheses.
    6. Ensure the report reflects the student's progress, character, and aptitudes accurately.
    7. Write in third person, avoiding first-person statements.
    8. Focus on relevant information for classroom performance, avoiding overly personal comments.
    9. Be tactful when addressing problems, always proposing solutions.
    10. Ensure the evaluation (excellent, very good, good, satisfactory, poor) matches the written content.
    11. Use positive language and propose solutions when addressing issues.
    12. For the final report of the year, include an overall assessment and summer practice recommendations.
    13. For Babies classes, focus on reactions and comprehension indicators.
    14. For T&T classes, address behavior, work habits, and performance in all skills.

    Include the following sections:
    1. Motivation & Participation
    2. Learning
    3. Behavior
    4. Test Results (if applicable)

    Use the following data:
    - Name: {student.name}
    - Professor: {student.professor}
    - Absences: {student.absences}
    - Listening Frequency: {student.listening_frequency}
    - Participates: {student.participates}
    - Enters happy: {student.enters_happy}
    - Positive attitude: {student.positive_attitude}
    - Enthusiasm: {student.enthusiasm}
    - Takes initiative: {student.takes_initiative}
    - Preferred activities: {student.preferred_activities}
    - Understands: {student.understands}
    - Oral Test Score: {student.oral_test_score}
    - Writing Score: {student.writing_score}
    - Homework Score: {student.homework_score}
    """
    
    writer_task = Task(
        description=task_description,
        agent=writer_agent
    )
    
    reviewer_agent = Agent(
        role="Report Reviewer",
        goal="Review and approve student reports for accuracy, quality, and adherence to the Definition of Done",
        backstory="You are a senior educator with years of experience in reviewing student reports.",
        allow_delegation=False
    )
    
    reviewer_task = Task(
        description="Review and approve the generated report, ensuring it covers all required sections, accurately reflects the student's performance, and adheres to all points in the Definition of Done.",
        agent=reviewer_agent
    )

    crew = Crew(
        agents=[writer_agent, reviewer_agent],
        tasks=[writer_task, reviewer_task]
    )

    return crew.kickoff()

class ReportAutomation:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def login(self):
        self.page.goto(URL)
        self.page.fill('#login_user', self.username)
        self.page.fill('#login_pass', self.password)
        self.page.click('.form_login button[type="submit"]')
        self.page.wait_for_load_state('networkidle')

    def select_school(self, school_name):
        school_selector = f'.li_school[data-name="{school_name}"]'
        self.page.click(school_selector)

    def select_course(self, course_name):
        course_selector = f'.li_course:has-text("{course_name}")'
        self.page.click(course_selector)

    def select_group(self, group_name):
        group_selector = f'.li_group[data-name="{group_name}"]'
        self.page.click(group_selector)

    def click_begin(self):
        self.page.click('#selector_button')
        self.page.wait_for_load_state('networkidle')

    def navigate_to_term_reports(self):
        self.page.click('a[href="termreports.html"]')
        self.page.wait_for_load_state('networkidle')

    def navigate_to_reports(self, school, course, group):
        self.select_school(school)
        self.select_course(course)
        self.select_group(group)
        self.click_begin()
        self.navigate_to_term_reports()

    def enter_report(self, student_name, term, report):
        student_row = self.page.locator(f'tr:has-text("{student_name}")')
        term_column = 1 if term == 1 else (2 if term == 2 else 3)
        edit_button = student_row.locator(f'td:nth-child({term_column + 1}) .edit-icon')
        edit_button.click()

        self.page.wait_for_selector('.report-input')

        sections = [
            'motivation-participation',
            'learning',
            'behavior',
            'test-results'
        ]

        for section in sections:
            self.page.fill(f'.{section}', report[section])

        self.page.click('.save-report-button')
        self.page.wait_for_load_state('networkidle')

        # Finish the report
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
            automation.navigate_to_reports(student.school, student.course, student.group)
            report = generate_report(student)
            
            automation.enter_report(student.name, student.term, report)
            
            print(f"Report submitted for {student.name}")
            time.sleep(2)  # Pause to avoid overwhelming the server

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        automation.close()

if __name__ == "__main__":
    main()