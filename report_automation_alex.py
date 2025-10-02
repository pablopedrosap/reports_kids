from playwright.sync_api import sync_playwright, Page
import pandas as pd
import datetime

class ReportAutomation:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = None
        self.page: Page = None  # We'll store the page object here

    def login(self):
        """
        Open browser, log in, and store the page object.
        """
        p = sync_playwright().start()
        self.browser = p.chromium.launch(headless=False, channel="chrome")
        self.page = self.browser.new_page()

        LOGIN_URL = "https://www.kidsandusschools.com/"
        self.page.goto(LOGIN_URL)
        
        self.page.fill("#txtUsuari", self.username)
        self.page.fill("#txtContrasenya", self.password)
        self.page.click("#btnEnviar")
        
        # Wait until navigation finishes or the page is idle
        self.page.wait_for_load_state("networkidle")

    def close(self):
        """Close browser."""
        if self.browser:
            self.browser.close()

    def try_click_or_last(self, locator, page, force=False):
        count = locator.count()
        for i in range(count):
            if locator.nth(i).is_visible():
                locator.nth(i).click(force=force)
                return True
        if count > 0:
            locator.last.click(force=force)
            return True
        return False

    def enter_report(self, course, group_name_original, teacher_name, student_name: str, term: int, report_data: dict, category: str, student_dict):
        """
        Reuse the existing logged-in page to:
         1. Go to Planificación -> Grupos
         2. Select the group / level
         3. Click "Evaluar"
         4. Click the student's "editar" button
         5. Fill in the form with data from report_data
         6. Click Guardar
        """
        page = self.page

        # 1) Ir a "Planificación"
        page.click("text=Planificación", force=True)
        page.wait_for_timeout(2000)

        # Hacer clic en "Grupos"
        grupos_elements = page.locator("text=Grupos")
        self.try_click_or_last(grupos_elements, page, force=True)

        # 2) Seleccionar el nivel (puedes usar algo más dinámico que '2')
        #    Si quieres basarlo en `category` o tus datos, hazlo aquí.
        levels = {
            "PETfs": "48",
            "CAE": "50",
            "FCEfs": "49",
            "CPE": "51",
            "1": "15",
            "2": "16"
        }
        for level_text, option_value in levels.items():
            if level_text.lower() in course.lower():
                page.select_option("#dNivell", option_value)
                page.wait_for_timeout(2000)
                break  # exit the loop once matched

        # 3) Seleccionar fila del horario (ejemplo)
        import re
        group_name_original
        s = group_name_original
        print(s)

        formatted = re.sub(r'(\d{1,2}\.\d{2})-(\d{1,2}\.\d{2})', r'\1 - \2', s)
        formatted = re.sub(r'([a-zA-Z]+)(\s)(\d)', r'\1  \3', formatted)

        horario_deseado = formatted
        print(formatted)
        page.wait_for_selector("table.llistatTaula tbody tr")

        filas = page.locator("table.llistatTaula tbody tr", has_text=horario_deseado)

        fila_horario = filas.filter(has_text=" ".join(teacher_name.split()[:2]))
        
        if fila_horario.count() > 0:
            fila_horario.first.click()
        else:
            print(f"No se encontró el horario '{horario_deseado}' con el profesor '{teacher_name.split()[:1]}'")

        page.wait_for_selector("#divOpac", state="hidden", timeout=20000)

        # Espera un poquito más para asegurarte de que no haya animaciones pendientes
        page.wait_for_timeout(1000)

        # Verifica que el botón 'Evaluar' esté visible y haz click forzado
        evaluar_locator = page.locator("#tdavaluar")
        if not self.try_click_or_last(evaluar_locator, page, force=True):
            # Optionally, retry after a short wait or handle the error
            page.wait_for_timeout(1000)
            self.try_click_or_last(evaluar_locator, page, force=True)

        # Esperar tabla de alumnos
        page.wait_for_selector("table.llistatTaula tbody tr", timeout=15000)

        # 5) Localizar alumno y hacer clic en editar

        parts = student_name.strip().split()
        if len(parts) < 2:
            return student_name  # No se puede separar en nombre/apellidos

        nombre = parts[0]

        nombrecom = " ".join(parts[:1])
        apellidoscom = " ".join(parts[2:])

        apellidos = " ".join(parts[1:])
        with_comma = f"{apellidos}, {nombre}"

        with_space_comma = f"{apellidos} , {nombre}"

        with_commacom = f"{apellidoscom}, {nombrecom}"
        

        try:
            try:

                page.locator(
                    f"tr:has-text('{with_comma}') input.llistatImatge[src='img/editar.png']"
                ).click()
            except:
                page.locator(
                    f"tr:has-text('{with_commacom}') input.llistatImatge[src='img/editar.png']"
                ).click()
            
    
        except:

            
            page.locator(
                f"tr:has-text('{with_space_comma}') input.llistatImatge[src='img/editar.png']"
            ).click()
            
        


        # Esperar el formulario
        page.wait_for_selector("#rdgorcomportament1", timeout=15000)

        # 6) Llenar el formulario usando tus rating_map y data
        rating_map = {
            "No suficiente": "1",
            "Suficiente":    "2",
            "Bueno":         "3",
            "Very good":     "4",  # "Muy bueno"
            "Excellent":     "5"   # "Excelente"
        }

        # ================
        # EJEMPLO DE LLENADO
        # ================
        comp_rating = report_data["Comportamiento"]["Rating"]
        comp_comment = report_data["Comportamiento"]["Comment"]
        comp_value = rating_map.get(comp_rating)
        if comp_value:
            page.click(f"#rdgorcomportament{comp_value}")
        page.fill("#txtcomportament", comp_comment)

        # TRABAJO
        trabajo_rating = report_data["Motivación_y_Participación"]["Rating"]
        trabajo_comment = report_data["Motivación_y_Participación"]["Comment"]
        trabajo_value = rating_map.get(trabajo_rating)
        if trabajo_value:
            page.click(f"#rdgortreball{trabajo_value}")
        page.fill("#txttreball", trabajo_comment)

        # RENDIMIENTO
        rendimiento_rating = report_data["Aprendizaje"]["Rating"]
        rendimiento_comment = report_data["Aprendizaje"]["Comment"]
        rendimiento_value = rating_map.get(rendimiento_rating)
        if rendimiento_value:
            page.click(f"#rdgorrendiment{rendimiento_value}")
        page.fill("#txtrendiment", rendimiento_comment)

        # EVALUACIÓN_GENERAL
        page.fill("#txtnotaGlobal", report_data["Evaluación_general"])

        page.fill("#txtnotaHomework", report_data["Deberes"])

        # Map test scores from student_dict
        def find_score(dict_data, possible_names):
            first_12_keys = list(dict_data.keys())[:12]
            for key in first_12_keys:
                if any(name.lower() in key.lower() for name in possible_names):
                    value = dict_data[key]
                    # Handle Excel date interpretation
                    if isinstance(value, (pd.Timestamp, datetime.datetime)):
                        # Convert date back to number (e.g., 9.5)
                        value = value.day + value.month/10
                    # Al final, solo devolver si es número o string numérico
                    if isinstance(value, (int, float)):
                        return str(value)
                    elif isinstance(value, str):
                        try:
                            float_val = float(value)
                            return str(float_val)
                        except ValueError:
                            return ""
                    elif pd.isna(value):
                        return ""
            return ""

        # Map Reading/Use of English to Reading field
        reading_score = find_score(student_dict, ["reading", "use of english"])

        if reading_score:
            page.fill("#cdtnotaReading", reading_score)
        
        # Map Writing/Written Test Score to Writing field
        writing_score = find_score(student_dict, ["writing", "written test"])
        if writing_score:
            page.fill("#cdtnotaWriting", writing_score)
        
        # Map Listening score
        listening_score = find_score(student_dict, ["listening"])
        if listening_score:
            page.fill("#cdtnotaListening", listening_score)
        
        # Map Speaking/Oral Test Score to Speaking field
        speaking_score = find_score(student_dict, ["speaking", "oral test"])
        if speaking_score:
            page.fill("#cdtnotaSpeaking", speaking_score)

        # 7) Guardar
        # justo después de cargar la página del informe
        page.evaluate("window.alert = () => {}")
        page.click("#btnEnviar")   # ya no aparece nada

        page.wait_for_timeout(4000)
