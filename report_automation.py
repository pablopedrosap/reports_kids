from playwright.sync_api import sync_playwright
import time


class ReportAutomation:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
        executable_path="/Users/pablopedrosa/Library/Caches/ms-playwright/chromium-1140/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
        headless=False
        )
        self.page = self.browser.new_page()
        

    def login(self):
        self.page.goto("https://myclassroom.kidsandus.es")
        self.page.fill('#login_user', self.username)
        self.page.fill('#login_pass', self.password)
        self.page.click('#login_button')
        self.page.wait_for_load_state('networkidle')

    def select_school(self, school_name):
        school_name = school_name.split(' ')[0]
        print(school_name)
        school_selector = f'.li_school:has-text("{school_name}")'
        self.page.click(school_selector)

    def select_course(self, course_name):
        course_selector = f'.li_course:has-text("{course_name}")'
        self.page.click(course_selector)

    def select_group(self, professor):
        group_selector = '.li_group'
        self.page.wait_for_selector(group_selector, timeout=30000)  # Wait for the elements to be visible
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
        self.page.wait_for_selector('.hamb', timeout=30000)  # Adjust the selector to the correct button
        self.page.click('.hamb')  # Click on the dropdown menu to make it visible

        # Wait for the specific "Term Reports" option
        term_reports_selector = 'div.menu_obj2:has-text("Term Reports")'
        self.page.wait_for_selector(term_reports_selector, timeout=30000)  # Ensure "Term Reports" is visible

        # Click on the "Term Reports" button
        self.page.click(term_reports_selector)
        self.page.wait_for_load_state('networkidle')


    def navigate_to_reports(self, school, course, group):
        print(school, course, group)

        print(school)
        
        change_group_selector = 'span.change_link'  
        if self.page.locator(change_group_selector).is_visible():
            self.page.click(change_group_selector)
            self.page.wait_for_load_state('networkidle')
            print("Navigated back to group selection.")

        self.select_school(school)
        self.select_course(course)
        self.select_group(group)
        self.click_begin()
        self.navigate_to_term_reports()

    def extract_scores(self, student_name, term, category):
        print(f"Extracting scores for {student_name}")


        student_row = self.page.locator(f'tr:has(td.td_left:has-text("{student_name}"))')
        term_column = 1 if term == 1 else (2 if term == 2 else 3)
        term_column = 1
        edit_button = student_row.locator(f'td.td_center:nth-child({term_column + 1}) .edit_camp')
        edit_button.wait_for(timeout=30000)
        edit_button.click()

        self.page.wait_for_selector('.input_comment_tr, .textarea_div', timeout=30000)

        # Initialize scores dictionary
        scores = {}

        # Define section mappings based on category
        section_mappings = {
            'default': {
                "Oral Test Score": 'oral_test_score',
                "Written Test Score": 'written_test_score',
                "Homework": 'homework_score'
            },
            'Tweens': {
                "Oral Test Score": 'oral_test_score',
                "Written Test Score": 'written_test_score',
                "Homework": 'homework_score',
                "Global Score": 'global_score'
            },
            'B&B': {
                "Oral Test Score": 'oral_test_score',
                "Written Test Score": 'written_test_score'
            }
        }

        # Get the mapping for the current category
        mappings = section_mappings.get(category, section_mappings['default'])

        # Locate all sections
        sections = self.page.locator('div.label_tr_skill, div.label_tr')
        section_count = sections.count()

        for i in range(section_count):
            section = sections.nth(i)
            section_title = section.inner_text().strip()

            for key, attr_name in mappings.items():
                if key in section_title:
                    # Locate the input field for the score
                    input_field = section.locator('xpath=following-sibling::input[@type="number"][1]')
                    value = input_field.get_attribute('value')

                    # Store the value in the scores dictionary
                    scores[attr_name] = value

                    # Extract the comment associated with that section
                    textarea_locator = section.locator('xpath=following::textarea[contains(@class, "input_comment_tr") or contains(@class, "textarea_div")][1]')
                    comment_text = textarea_locator.input_value()
                    scores[f"{attr_name}_comment"] = comment_text

                    break  # No need to check other keys for this section

        # Go back to the previous page
        self.page.go_back()
        self.page.wait_for_load_state('networkidle')

        print(f"Extracted scores: {scores}")
        return scores

    def enter_report(self, student_name, term, report, category):
        print(student_name)
        student_row = self.page.locator(f'tr:has(td.td_left:has-text("{student_name}"))')
        print(student_row)
        term_column = 1 if term == 1 else (2 if term == 2 else 3)
        term_column = 1
        edit_button = student_row.locator(f'td.td_center:nth-child({term_column + 1}) .edit_camp')
        edit_button.wait_for(timeout=30000)
        edit_button.click()

        self.page.wait_for_selector('.input_comment_tr, .textarea_div', timeout=30000)

        # Define section mappings based on category
        section_mappings = {
            'default': {
                "Audio Listening Frequency": "Audio Listening Frequency",
                "Motivation": "Motivación_y_Participación",
                "Learning": "Aprendizaje",
                "Behaviour": "Comportamiento",
                "Oral Test Score": "Nota_de_prueba_oral",
                "Written Test Score": "Nota_de_prueba_escrita",
                "General Assessment": "Evaluación_general"
            },
            'tweens': {
                "Audio Listening Frequency": "Audio Listening Frequency",
                "Behaviour": "Comportamiento",
                "Work": "Trabajo",
                "Performance": "Rendimiento",
                "My Way": "My_Way",
                "Global Score": "Nota_Global",
                "Oral Test Score": "Nota_de_prueba_oral",
                "Written Test Score": "Nota_de_prueba_escrita",
                "Homework": "Deberes",
                "General Assessment": "Evaluación_general"
            },
            'b&b': {
                "Motivation": "Motivación_y_Participación",
                "Learning": "Aprendizaje",
                "Behaviour": "Comportamiento",
                "Oral Test Score": "Nota_de_prueba_oral",
                "Written Test Score": "Nota_de_prueba_escrita",
                "General Assessment": "Evaluación_general"
            }
        }

        # Get the mapping for the current category
        print(category)
        if 'tweens' in category.lower() or 'teens' in category.lower():
            category = 'tweens' 
        mappings = section_mappings.get(category.lower(), section_mappings['default'])
        print(mappings)
        print('909999900')
        # Adjust the section selector if necessary
        sections = self.page.locator('div.label_tr_skill, div.label_tr')
        section_count = sections.count()

        for i in range(section_count):
            section = sections.nth(i)
            section_title = (section.inner_text()).strip()
            print(f"Processing section: {section_title}")

            comment_text = ""
            select_value = None
            section_key = None

            # Map the section title to the report key
            for key, report_key in mappings.items():
                if key in section_title:
                    section_key = report_key
                    break

            if section_key:
   
                section_data = report.get(section_key, {})
                if isinstance(section_data, dict):
                    comment_text = section_data.get('Comment', "Sin comentario")
                    select_value = section_data.get('Rating')
                else:
                    comment_text = section_data

                # Interact with the select element if applicable
                if select_value:
                    if section_key == 'Audio Listening Frequency' and select_value == 'Insufficient':
                        select_value = 'Sufficient'
                        print(f"Updated 'Audio Listening Frequency' rating to '{select_value}'")

                    select_value = 'Very good' if select_value == 'Very Good' else select_value
                    select_locator = section.locator('xpath=following::select[contains(@class, "select_tr")][1]')
                    select_locator.select_option(label=select_value)
                    print(f"Selected '{select_value}' for section '{section_title}'")
                # Fill in the comment if applicable
                if comment_text:
                    textarea_locator = section.locator('xpath=following::textarea[contains(@class, "input_comment_tr") or contains(@class, "textarea_div")][1]')
                    textarea_locator.fill(comment_text)
                    print(f"Added comment for '{section_title}': {comment_text}")

            else:
                print(f"No mapping found for section '{section_title}'. Skipping.")

        # Save the report
        save_button_selector = 'div.homework_buttons .whitebutton2'
        self.page.click(save_button_selector)

        time.sleep(1)
        self.page.go_back()
        self.page.wait_for_load_state('networkidle')
        print("Reporte guardado exitosamente.")


    def close(self):
        self.browser.close()
        self.playwright.stop()