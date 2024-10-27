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
        change_group_selector = 'span.change_link'  
        if self.page.locator(change_group_selector).is_visible():
            self.page.click(change_group_selector)
            self.page.wait_for_load_state('networkidle')
            print("Navigated back to group selection.")

        self.select_school(school)
        self.select_course(course)
        self.select_group(professor)
        self.click_begin()
        self.navigate_to_term_reports()

        

    def enter_report(self, student_name, term, report):
        print(student_name)
        student_row = self.page.locator(f'tr:has(td.td_left:has-text("Diego"))')
        print(student_row)
        term_column = 1 if term == 1 else (2 if term == 2 else 3)
        edit_button = student_row.locator(f'td.td_center:nth-child({term_column + 1}) .edit_camp')
        edit_button.wait_for(timeout=10000)
        edit_button.click()

        self.page.wait_for_selector('.input_comment_tr', timeout=10000)

        sections = self.page.locator('div.label_tr_skill, div.label_tr')
        section_count = sections.count()

        for i in range(section_count):
            section = sections.nth(i)
            section_title = (section.inner_text()).strip()
            print(section_title)

            comment_text = ""
            select_value = None

            # Determine the appropriate comment text and select value
            if "Audio Listening Frequency" in section_title:
                select_value = "Sufficient"
            elif "Motivation" in section_title:
                section_key = 'Motivación_y_Participación'
            elif "Learning" in section_title:
                section_key = 'Aprendizaje'
            elif "Behaviour" in section_title:
                section_key = 'Comportamiento'
            elif "Oral Test Score" in section_title:
                section_key = 'Nota_de_prueba_oral'
            elif "General Assessment" in section_title:
                section_key = 'Evaluación_general'
            else:
                section_key = None

            if section_key:
                section_data = report.get(section_key, {})
                if isinstance(section_data, dict):
                    comment_text = section_data.get('Comment', "Sin comentario")
                    select_value = section_data.get('Rating')
                else:
                    comment_text = section_data

            # Interact with the select element if applicable
            if select_value:
                select_locator = section.locator('xpath=following::select[contains(@class, "select_tr")][1]')
                select_locator.select_option(label=select_value)
                print(f"Selected '{select_value}' for section '{section_title}'")

            # Fill in the comment if applicable
            if comment_text:
                textarea_locator = section.locator('xpath=following::textarea[contains(@class, "input_comment_tr")][1]')
                textarea_locator.fill(comment_text)
                print(f"Added comment for '{section_title}': {comment_text}")

        # Save the report
        save_button_selector = 'div.homework_buttons .whitebutton2'
        # Uncomment the next line to click the save button
        # await self.page.click(save_button_selector)
        
        time.sleep(3)
        self.page.go_back()
        self.page.wait_for_load_state('networkidle')
        print("Reporte guardado exitosamente.")

    def close(self):
        self.browser.close()
        self.playwright.stop()