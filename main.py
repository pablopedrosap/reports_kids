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

class ReportAutomation:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def login(self):
        self.page.goto(URL)
        # TODO: Add login selectors and actions
        self.page.fill('selector_for_username', self.username)
        self.page.fill('selector_for_password', self.password)
        self.page.click('selector_for_login_button')

    def navigate_to_reports(self, school, course, group):
        # TODO: Add navigation selectors and actions
        self.page.click('selector_for_school_dropdown')
        self.page.click(f'selector_for_school_option_{school}')
        # Similar steps for course and group
        self.page.click('selector_for_begin_button')
        self.page.click('selector_for_term_reports')

    def enter_report(self, student, report):
        # TODO: Add report entry selectors and actions
        self.page.fill(f'selector_for_student_{student.name}', report)
        self.page.click('selector_for_save_button')

    def close(self):
        self.browser.close()
        self.playwright.stop()

def generate_report(student):
    writer_agent = Agent(
        role="Report Writer",
        goal="Write detailed and personalized student reports",
        backstory="You are an experienced educator who writes insightful reports on student progress.",
        allow_delegation=False
    )
    reviewer_agent = Agent(
        role="Report Reviewer",
        goal="Review and approve student reports for accuracy and quality",
        backstory="You are a senior educator with years of experience in reviewing student reports.",
        allow_delegation=False
    )

    crew = Crew(
        agents=[writer_agent, reviewer_agent],
        tasks=[
            Task(
                description=f"Write a detailed report for {student.name} based on their performance data.",
                agent=writer_agent
            ),
            Task(
                description="Review and approve the generated report, suggesting improvements if necessary.",
                agent=reviewer_agent
            )
        ]
    )

    return crew.kickoff()

def load_students():
    df = pd.read_excel(EXCEL_FILE)
    return [StudentData(row) for _, row in df.iterrows()]

def main():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    automation = ReportAutomation(username, password)
    students = load_students()

    try:
        automation.login()

        for student in students:
            automation.navigate_to_reports(student.school, student.course, "group_placeholder")
            report = generate_report(student)
            automation.enter_report(student, report)
            print(f"Report submitted for {student.name}")
            time.sleep(2)  # Pause to avoid overwhelming the server

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        automation.close()

if __name__ == "__main__":
    main()