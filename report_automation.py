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
        group_selector = '.li_group'
        self.page.wait_for_selector(group_selector, timeout=10000)  # Wait for the elements to be visible
        elements = self.page.query_selector_all(group_selector)
        print(f"Found {len(elements)} groups.")
        
        for element in elements:
            text = element.inner_text()
            if professor.lower() in text.lower():
                element.click()
                break

    def click_begin(self):
        self.page.click('#selector_button')
        self.page.wait_for_load_state('networkidle')

    def navigate_to_term_reports(self):
    # Ensure the menu is visible and clickable
        self.page.wait_for_selector('.hamb', timeout=10000)  # Adjust the selector to the correct button
        self.page.click('.hamb')  # Click on the dropdown menu to make it visible

        # Wait for the specific "Term Reports" option
        term_reports_selector = 'div.menu_obj2:has-text("Term Reports")'
        self.page.wait_for_selector(term_reports_selector, timeout=10000)  # Ensure "Term Reports" is visible

        # Click on the "Term Reports" button
        self.page.click(term_reports_selector)
        self.page.wait_for_load_state('networkidle')


    def navigate_to_reports(self, school, course, professor):
        self.select_school(school)
        self.select_course(course)
        self.select_group(professor)
        self.click_begin()
        self.navigate_to_term_reports()

    def enter_report(self, student_name, term, report):
        print(student_name)
        student_row = self.page.locator(f'tr:has-text("{'Jimena'}")')
        print(student_row)
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