from playwright.sync_api import sync_playwright

# Reemplaza con la URL real y las credenciales correspondientes
LOGIN_URL = "https://www.kidsandusschools.com/"  
USUARIO = "coordibarajas"
CONTRASENYA = "2425"
course = 'petfs'
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False para ver la ejecución
    page = browser.new_page()
    
    # Navegar a la página de login
    page.goto(LOGIN_URL)
    
    # Completar el formulario de login (ajusta los selectores si es necesario)
    page.fill("#txtUsuari", USUARIO)
    page.fill("#txtContrasenya", CONTRASENYA)
    page.click("#btnEnviar")
    
    # Esperar a que se complete el login (por ejemplo, espera un elemento que aparezca tras el login)
    page.wait_for_load_state("networkidle")
    

    page.click("text=Planificación", force=True)
    # page.screenshot(path="before_hover.png")

    page.wait_for_timeout(1000)

    # Print all elements that match "Grupos"
    grupos_elements = page.locator("text=Grupos")
    count = grupos_elements.count()
    # Try clicking a visible one
    if grupos_elements.nth(3).is_visible():
            grupos_elements.nth(3).click()
            clicked = True
        
    # If none were visible, force-click the last one
    if not clicked:
        print("No visible 'Grupos' found, forcing click on last element.")
        grupos_elements.last.click(force=True)

    page.wait_for_selector("#dNivell", state="visible", timeout=5000)
    
    # Define the levels to select: PET Fs, CAE, FCE Fs, CPE, 1 and 2.
    # These values correspond to the <option> values in the HTML.
    levels = {
        "PETfs": "48",
        "CAE": "50",
        "FCEfs": "49",
        "CPE": "51",
        "1": "15",
        "2": "16"
    }
    
    # Iterate through the levels and select each one.
    for level_text, option_value in levels.items():
        if level_text.lower() in course.lower():
            print(f"Selecting level {level_text} (value {option_value})")
            page.select_option("#dNivell", option_value)
            # Wait briefly for any onchange JavaScript to process the selection.
            page.wait_for_timeout(1000)
    
    # Final wait to observe the result
    page.wait_for_timeout(3000)
    browser.close()