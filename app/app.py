from flask import Flask, flash, render_template,request, url_for, redirect, session
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()
app=Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')




#Vista General -----------------------------------------------------------------------------    
#Inicio Cafeteria
@app.route('/')
def inicio():
    return render_template('index.html')

#Menu publico
@app.route('/informacion')
def informacion():
    return render_template('informacion.html')

#Cerrar Sesion
@app.route('/salir')
def salir():
    session.clear()
    return render_template('index.html')

def some_async_function(start_date: str) -> str:
    try:
        from scraper import scrape_data
        obt_reporte = scrape_data(start_date)
        if obt_reporte is None:
            return ""
        return obt_reporte
    except Exception as e:
        print(f'Error in some_async_function: {e}')  
        return ""

@app.route('/obt_reporte', methods=['GET', 'POST']) 
def obt_reporte():
    result = None
    if  request.method == 'POST':
        start_date = request.form['start_date']
        result = some_async_function(start_date)
        if result is None or result == "":
            return render_template('lista_documentos.html', result=None, url=False)
        return render_template('lista_documentos.html', result=f'csv/{result}', url=True)
    else:
        return render_template('lista_documentos.html', result=None, url=False)
    

#Usuario Administrador -----------------------------------------------------------------------------    
#General
@app.route('/users')
def users():
    url = os.getenv('URL_WEB_PAGE')
    return render_template('lista_documentos.html', result=None, url=url)


if __name__=='__main__':
    app.run(port=5000, debug=True, host='0.0.0.0')
