from flask import Flask, render_template,redirect,url_for, request
import pymysql
from python.bd import *

app = Flask(__name__)

# Definir una ruta para la página principal
@app.route('/')
def index():
    return render_template('indexapp.html')

@app.route('/sesion')
def sesion():
    return render_template('inicioSapp.html')

@app.route('/registro')
def registro():
    return render_template('Registroapp.html')

@app.route('/planteles')
def planteles():
    return render_template('plantelesapp.html')

@app.route('/tutorias')
def tutorias():
    return render_template('tutoriasapp.html')

@app.route('/funciones')
def funciones():
    return render_template('funcionesapp.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/noticias')
def noticias():
    bd = Coneccion()
    noticias = bd.obtenerTablas("noticias")
    bd.exit()
    return render_template('noticiasapp.html', noticias=noticias)

@app.route('/insnot', methods=['GET', 'POST'])
def agregar_noticia():
    if request.method == 'POST':
        datos = []
        datos.append(request.form['titulo'])
        datos.append(request.form['descripcion'])
        datos.append(request.form['img'])
        datos.append(request.form['fecha'])

        bd = Coneccion()
        bd.insertarRegistro("noticias", datos)
        bd.exit()
        return redirect(url_for('noticias'))
    return render_template('insnot.html')

if __name__ == '__main__':
    app.run(debug=True)
