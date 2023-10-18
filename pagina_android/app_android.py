from flask import Flask, render_template,redirect,url_for, request, session
from authlib.integrations.flask_client import OAuth
import os
from python.bd import *

app = Flask(__name__)
app.secret_key = os.urandom(24)

oauth = OAuth(app)

oauth.register(
    name='google',
    client_id='TU_ID_DE_CLIENTE',
    client_secret='TU_SECRETO_DE_CLIENTE',
    access_token_url='',
    access_token_params='',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='',
    client_kwargs=None
)

# Definir una ruta para la página principal
@app.route('/')
def index():
    if 'google_token' in session:
        resp = oauth.google.get('userinfo')
        user_info = resp.json()
        return 'Hola, ' + user_info['name']
    return render_template('indexapp.html')

@app.route('/sesion')
def sesion():
    return render_template('inicioSapp.html')

@app.route('/login')
def login():
    return oauth.google.authorize_redirect(redirect_uri=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/authorized')
def authorized():
    token = oauth.google.authorize_access_token()
    session['google_token'] = (token, '')
    return redirect(url_for('index'))

@app.route('/registro')
def registro():
    return render_template('Registroapp.html')

@app.route('/planteles')
def planteles():
    return render_template('plantelesapp.html')

@app.route('/tutorias')
def tutorias():
    return render_template('tutoriasapp.html')

@app.route('/clubs')
def clubs():
    return render_template('clubapp.html')
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
