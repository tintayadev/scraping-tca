from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from get_date import get_yesterday, get_today, get_3days_after, format_date
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import os
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get(os.getenv('URL_WEB_PAGE'))
# 
def nav_next_page():
    """
    Navega hasta la ultima pagina de bienes y extrae los datos de cada bien.
    Luego, crea un reporte con los datos extraidos.
    """
    cuce =  []
    entidad =  []
    objeto_de_Contratación =  []
    subasta =  []
    fecha_Presentación =  []
    archivos =  []
    try:
        btn_next = driver.find_element(By.ID, "tablaSimple_paginate")
        ul_pagination = btn_next.find_element(By.TAG_NAME, "ul")
        li_elements = ul_pagination.find_elements(By.TAG_NAME, 'li')
        nro_tb_next = len(li_elements)
        if (nro_tb_next<2):
            limit = nro_tb_next
        else:
            limit = li_elements[-2].find_element(By.TAG_NAME, 'a').text
            limit = int(limit)-2 if int(limit)>2 else int(limit)
            
        for i in range(limit):
            table_bienes = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tablaSimple")))
            rows = table_bienes.find_elements(By.TAG_NAME, "tr")
            for indx in range(1,len(rows)):
                cols= rows[indx].find_elements(By.TAG_NAME, "td")
                cuce.append(cols[0].text)
                entidad.append(cols[1].text)
                objeto_de_Contratación.append(cols[4].text)
                subasta.append(cols[5].text)
                fecha_Presentación.append(cols[7].text)
                archivos.append(cols[9].text)
            next_buttons = driver.find_elements(By.XPATH, "//a[@aria-label='Next']")
            for btn in next_buttons:
                if btn.text=="Siguiente":
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", btn)
        return create_report(cuce,entidad,objeto_de_Contratación,subasta,fecha_Presentación,archivos)
    except Exception as e:
        print(e)
        # app.logger.debug('There is an error')
        # app.logger.debug(e)
        print("Button Buscar not found. Error:", e)
def get_date_start():
    yesterday = get_today()
    return yesterday
def get_end_date(start_date: str):
    end_date = get_3days_after(start_date)
    return end_date
def uncheck_categories_filter():
    labels_to_uncheck = ["obras", "servicios", "consultoria"]
    for label_text in labels_to_uncheck:
        checkbox = driver.find_element(By.XPATH, f".//input[@type='checkbox' and @name='{label_text}']")
        driver.execute_script("arguments[0].setAttribute('value', '')", checkbox)
def filter_by_date(str_start_date: str):
    # Filter by date
    inp_fini = driver.find_element(By.NAME, 'presentacionPropuestasDesde')
    start_date = format_date(str_start_date)
    inp_fini.clear()
    inp_fini.send_keys(start_date)
    # Filter by date
    inp_ffin = driver.find_element(By.NAME, 'presentacionPropuestasHasta')
    end_date = get_end_date(start_date)
    inp_ffin.clear()
    inp_ffin.send_keys(end_date)

def perform_search():    
    calendar_div = driver.find_element(By.CLASS_NAME, 'input-group-addon.calendar')
    calendar_div.click() 
    btn_buscar = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.btn.btn-primary.btn-sm.busquedaForm[value="Buscar"][data-form="btnConvNacionalInter"]'))
    )
    btn_buscar.click() 
def close_dialog():
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div[2]/div[5]/div/div/div[1]/button")))
    button.click()
def navigate_announcement_page():
    parent_div = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "col-md-8.banner-bottom-grid-left")))
    child_link = parent_div.find_element(By.XPATH, ".//a[@data-original-title='Convocatorias']")
    child_link.click()
def create_report(cuce,entidad,objeto_de_Contratación,subasta,fecha_Presentación,archivos):
    data = {
        "cuce": cuce,
        "entidad": entidad,
        "objeto_de_contratacion": objeto_de_Contratación,
        "subasta": subasta,
        "fecha_Presentación": fecha_Presentación,
        "archivos": archivos
    }
    df = pd.DataFrame(data)
    current_path = os.getcwd()  # Get the current working directory
    static_folder = 'app/static/csv'  # Define your static folder
    name_file = os.path.join(current_path, static_folder, f'{get_today()}.csv')  # Concatenate paths
    df.to_csv(name_file, index=False)
    print("Reporte creado")
    print(name_file)
    return f'{get_today()}.csv'

def scrape_data(start_date: str):
    result = None
    try:
        modal_dialog = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "modal-dialog"))
        )
        if modal_dialog:
            close_dialog()
            try:
                navigate_announcement_page()
                try:
                    uncheck_categories_filter()
                    filter_by_date(start_date)
                    perform_search()
                    result = nav_next_page()  
                    driver.quit()
                except Exception as e:
                    print(f"Uncheck categories failed {e}")
            except Exception as e:
                print(f"Error to navigate announcement page: {e}")
        else:
            print("Error to close dialog")
    except Exception as e:
        print(os.getenv('URL_WEB_PAGE'))
        print(f"Modal dialog is not present: {e}")
    finally:    
        return result
