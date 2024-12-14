from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pdfkit

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    "download.default_directory": "/content", 
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
})

driver = webdriver.Chrome(options=options)

try:
    driver.get("https://www.sicoes.gob.bo/portal/index.php")
    time.sleep(2)

    driver.get("https://www.sicoes.gob.bo/portal/contrataciones/busqueda/convocatorias.php?tipo=convNacional")
    time.sleep(2)

    ver_ficha_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Ver Ficha')]")
    ver_ficha_button.click()

    time.sleep(3)

    input("Resuelve el reCAPTCHA y presiona Enter cuando termines...")

    time.sleep(5)

    form_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "formulario"))
    )
    print("Formulario encontrado.")

    download_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#formulario > div > div > div.panel-body > div:nth-child(7) > button"))
    )

    if download_button.is_displayed() and download_button.is_enabled():
        download_button.click()
        print("Descarga completada")

        html_file = "pagina.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"El contenido del DOM se ha guardado en '{html_file}'.")


        pdf_file = "pagina.pdf"
        try:
            pdfkit.from_file(html_file, pdf_file)
            print(f"El archivo HTML se ha convertido a PDF y guardado como '{pdf_file}'.")
        except Exception as e:
            print(f"Ocurrió un error al convertir a PDF: {e}")
    else:
        print("El botón 'Descargar Ficha' no está visible o habilitado.")

except Exception as e:
    print(f"Ocurrió un error: {e}")
    print("Contenido del DOM para depuración:")
    print(driver.page_source)
    

    with open("pagina_error.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("El contenido del DOM se ha guardado en 'pagina_error.html'.")

finally:
    driver.quit()
