from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, json, traceback

CHROMEDRIVER_PATH = r"E:\chromedriver\chromedriver-win64\chromedriver-win64\chromedriver.exe"

def generar_cookies_secop():
    chrome_options = Options()
    # Headless mode
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service(CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(60)

    try:
        print("🔄 Navegando a la página de login...")
        driver.get("https://community.secop.gov.co/STS/Users/Login/Index?SkinName=CCE")
        
        # Esperar a que la página cargue completamente
        wait = WebDriverWait(driver, 20)
        
        # Esperar a que los campos estén presentes y visibles
        print("⏳ Esperando campos de login...")
        username_field = wait.until(EC.presence_of_element_located((By.ID, "txtUserName")))
        password_field = wait.until(EC.presence_of_element_located((By.ID, "txtPassword")))
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "btnLoginButton")))
        
        # Pequeña pausa para asegurar que la página está lista
        time.sleep(2)
        
        # Limpiar campos antes de escribir
        username_field.clear()
        password_field.clear()
        
        print("✍️ Ingresando credenciales...")
        username_field.send_keys("CirkonT")
        time.sleep(0.5)
        password_field.send_keys("122535Sa*")
        time.sleep(0.5)
        
        print("🔘 Haciendo clic en login...")
        login_button.click()
        
        # Esperar a que la URL cambie (indica que el login fue exitoso)
        print("⏳ Esperando respuesta del login...")
        time.sleep(5)
        
        current_url = driver.current_url
        print(f"📍 URL tras login: {current_url}")
        
        # Verificar si seguimos en la página de login
        if "Login" in current_url:
            print("⚠️ ADVERTENCIA: Parece que el login falló. Aún estamos en la página de login.")
            
            # Intentar tomar screenshot para debug
            try:
                driver.save_screenshot("login_error.png")
                print("📸 Screenshot guardado como 'login_error.png'")
            except:
                pass
            
            # Intentar obtener mensaje de error si existe
            try:
                error_msg = driver.find_element(By.CLASS_NAME, "error-message")
                print(f"❌ Mensaje de error: {error_msg.text}")
            except:
                print("❌ No se pudo obtener el login. Verifica las credenciales.")
        else:
            print("✅ Login exitoso!")
            
            time.sleep(30)
            # Navegar a la página deseada
            print("🔄 Navegando a OpportunityDossierWorkspace...")
            driver.get("https://www.secop.gov.co/CO1BusinessLine/Tendering/OpportunityDossierWorkspace/Index")
            time.sleep(5)
            
            print(f"📍 URL después del cambio: {driver.current_url}")
        
        # Obtener cookies (incluso si el login falló, para debug)
        print("\n🍪 Obteniendo cookies...")

        time.sleep(30)

        cookies_selenium = driver.get_cookies()

        print("🍪 Cookies obtenidas:")
        for cookie in cookies_selenium:
            print(cookie)
    
        cookies = {}
        for c in cookies_selenium:
            cookies[c["name"]] = c["value"]

        print("\n✅ COOKIES GENERADAS:\n")
        print(json.dumps(cookies, indent=4))

        with open("cookies_secop.json", "w", encoding="utf-8") as f:
            json.dump(cookies, f, indent=4)
        
        return cookies


    except Exception as e:
        print(f"\n❌ Error: {e}")
        traceback.print_exc()
        return None

    finally:
        print("\n🔒 Cerrando navegador...")
        driver.quit()
        print("✅ Proceso terminado")