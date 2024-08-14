from playwright.sync_api import sync_playwright
import time

class ReportAutomation:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()

    def login(self):
        self.page.goto("https://myclassroom.kidsandus.es")
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
        for element in elements:
            text = element.inner_text()
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
            self.page.fill(f'.{section}', report['Data'][section.replace('-', ' ').title()])

        self.page.wait_for_load_state('networkidle')

        self.page.click('.finish-report-button')
        self.page.wait_for_load_state('networkidle')

    def close(self):
        self.browser.close()
        self.playwright.stop()