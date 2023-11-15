from flask import Flask, render_template,redirect,url_for, request, session
from authlib.integrations.flask_client import OAuth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import google.auth.transport.requests
import google.auth.exceptions
import os
from python.bd import *
from datetime import timedelta
import secrets


# decorator for routes that should be accessible only by logged in users
from python.funciones_auth import login_required

# dotenv setup
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/DGTIPOCKET/pagina_android')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

app = Flask(__name__)

# XDDDDDDDD
# Session config
app.secret_key = os.getenv("APP_SECRET_KEY")
#app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id= os.getenv("GOOGLE_CLIENT_ID"),
    client_secret= os.getenv("GOOGLE_CLIENT_SECRET"),
    #authorize_url='https://accounts.google.com/o/oauth2/auth',
    #authorize_params=None,
    #authorize_callback=None,
    #authorize_response=None,
    #token_url='https://accounts.google.com/o/oauth2/token',
    #token_params=None,
    #token_response=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    #--userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    #client_kwargs={'scope': 'openid email profile'}

    #redirect_uri=lambda: url_for('auth', _external=True),
    client_kwargs={'scope': 'openid email profile https://www.googleapis.com/auth/calendar.readonly'},
)

# Definir una ruta para la página principal
@app.route('/')
@login_required
def index():
    bd = Coneccion()
    noticias = bd.obtenerTablas("noticias")
    bd.exit()
    parametros = dict(session)['profile']
    print("sesion")
    print(dict(session))
    user_info = dict(session)['user_info']
    credentials = Credentials.from_authorized_user_info(user_info)
    if not credentials.valid:
        if credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
            except google.auth.exceptions.RefreshError:
                return redirect(url_for('login'))
        else:
            return redirect(url_for('login'))
    # Crear un servicio de la API de Google Calendar con las credenciales
    service = build('calendar', 'v3', credentials=credentials)

    # Obtener la lista de eventos del calendario
    events_result = service.events().list(calendarId='primary', maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Procesar y mostrar los eventos (puedes adaptar esta parte según tus necesidades)
    if not events:
        return 'No hay eventos próximos.'
    else:
        event_list = []
        for event in events:
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            event_list.append(f"{event['summary']} ({start_time})")

    print(event_list)

    return render_template('indexapp.html', parametros = parametros,noticias=noticias)


# @app.route("/prueba")
# def prueba():
#     print("aki: ")
#     email = dict(session)['profile']['email']
#     return 'Hola ' + email

@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    nonce = secrets.token_urlsafe(16)
    info = oauth.google.parse_id_token(token,nonce=nonce)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    # and set ur own data in the session not the profile from google
    session['profile'] = user_info
    session['user_info'] = info
    print("--------------datos")
    print(user)
    print(token)
    print(info)
    print("fin")
    #session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('login'))

@app.route('/planteles')
def planteles():
    parametros = dict(session)['profile']
    return render_template('plantelesapp.html', parametros = parametros)

@app.route('/tutorias')
def tutorias():
    parametros = dict(session)['profile']
    return render_template('tutoriasapp.html', parametros = parametros)

@app.route('/clubs')
def clubs():
    parametros = dict(session)['profile']
    return render_template('clubapp.html', parametros = parametros)

@app.route('/funciones')
def funciones():
    parametros = dict(session)['profile']
    return render_template('funcionesapp.html', parametros = parametros)

@app.route('/menu')
def menu():
    parametros = dict(session)['profile']
    return render_template('menu.html', parametros = parametros)

@app.route('/servicio')
def servicio():
    parametros = dict(session)['profile']
    return render_template('servicio.html', parametros = parametros)
@app.route('/agenda')
def agenda():
    parametros = dict(session)['profile']
    return render_template('agenda.html', parametros = parametros)

@app.route('/historial')
def historial():
    parametros = dict(session)['profile']
    return render_template('historial.html', parametros = parametros)

@app.route('/noticias')                            #pendiente css
def noticias():
    bd = Coneccion()
    noticias = bd.obtenerTablas("noticias")
    bd.exit()
    parametros = dict(session)['profile']
    return render_template('noticiasapp.html', noticias=noticias, parametros = parametros)

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
    
    parametros = dict(session)['profile']
    return render_template('insnot.html', parametros = parametros)

@app.route('/instaviso', methods=['GET', 'POST'])
def agregar_aviso():
    if request.method == 'POST':
        datos = []
        datos.append(request.form['id'])
        datos.append(request.form['titulo'])
        datos.append(request.form['descripcion'])
        datos.append(request.form['fecha'])

        bd = Coneccion()
        bd.insertarRegistro("avisos", datos)
        bd.exit()
        return redirect(url_for('index'))
    parametros = dict(session)['profile']
    return render_template('insnot.html', parametros = parametros)
    
    
@app.route('/a')
def pruebas():
    parametros = dict(session)['profile']
    return render_template('prueba.html', parametros = parametros)

if __name__ == '__main__':
    app.run(debug=True)
