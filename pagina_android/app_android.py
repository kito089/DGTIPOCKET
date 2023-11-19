from flask import Flask, render_template,redirect,url_for, request, session
from authlib.integrations.flask_client import OAuth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
import google.auth.exceptions
import os
import os.path
from python.bd import *
import datetime
import json

# decorator for routes that should be accessible only by logged in users
from python.funciones_auth import login_required

# dotenv setup
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/DGTIPOCKET/pagina_android')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

app = Flask(__name__)

app.secret_key = os.getenv("APP_SECRET_KEY")

oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id= os.getenv("GOOGLE_CLIENT_ID"),
    client_secret= os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_url='https://accounts.google.com/o/oauth2/auth',#auth_url,
    # authorize_params=None,
    # authorize_callback=None,
    # authorize_response=None,
    token_url='https://oauth2.googleapis.com/token',
    # token_params=None,
    # token_response=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    #--userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile https://www.googleapis.com/auth/calendar.readonly'},
)

# Definir una ruta para la página principal
@app.route('/')
@login_required
def index():
    bd = Coneccion()
    noticias = bd.obtenerTablas("noticias")
    avisos = bd.obtenerTablas("avisos")
    concursos = bd.obtenerTablas("concursos")
    bd.exit()
    print("---------------sesion")
    print(dict(session))
    parametros = dict(session)['profile']
    toks = dict(session)['tok_info']

    print("session token")
    print(toks)
    
    #archivo = str(parametros['grado']) + str(parametros['grupo']) 

    return render_template('indexapp.html', parametros = parametros,noticias=noticias, avisos=avisos, concursos=concursos)#,archivo=archivo)

@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    return google.authorize_redirect(url_for('authorize', _external=True), access_type='offline', prompt='consent')

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    tokens = {'client_id':os.getenv("GOOGLE_CLIENT_ID"),'client_secret': os.getenv("GOOGLE_CLIENT_SECRET"), 'token_uri': 'https://oauth2.googleapis.com/token'}
    # tokens = {
    #     'token': token['access_token'],
    #     'refresh_token': 'your_refresh_token',
    #     'token_uri': 'https://oauth2.googleapis.com/token',
    #     'client_id': os.getenv("GOOGLE_CLIENT_ID"),
    #     'client_secret': os.getenv("GOOGLE_CLIENT_SECRET"),
    #     'scopes': token['scope'].split(),
    #     'expiry': 'expiry_timestamp',
    #     'id_token': token['id_token'],
    # }
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    session['profile'] = user_info
    token.pop('userinfo')
    tokens.update(token)
    session['tok_info'] = tokens
    print("---------------toks")
    print(tokens)
    with open("token.txt", "w") as tok:
        tok.write(str(tokens))
    print("fin")
    #session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/terminar')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('login'))

@app.route('/planteles')
def planteles1():
    parametros = dict(session)['profile']
    return render_template('plantelesapp.html', parametros = parametros)

@app.route('/terminar')
@login_required
def terinar():
    parametros = dict(session)['profile']
    print("-----------------------para")
    print(parametros)
    bd = Coneccion()
    no = parametros['email'].replace("@cetis155.edu.mx","")
    print("-----------Control")
    print(no)
    grado =  bd.seleccion("alumnos", "grado","no_control = "+str(no))
    bd.exit()
    print("------------ grado y grupo")
    print(grado)
    if grado:
        grupo = bd.seleccion("grupo","letra","idgrupo = "+str(bd.seleccion("alumnos","grupo_idgrupo","no_control = "+str(no))[0][0]))[0][0]
        print(grupo)
        parametros.update({'grado':grado[0][0], 'grupo':grupo})
        session['profile'] = parametros
        return redirect(url_for("index"))  
    return render_template('terminarR.html', parametros = parametros)


@app.route('/insertainfo', methods=['GET', 'POST'])
@login_required
def insertainfo():
    parametros = dict(session)['profile']
    if request.method == 'POST':
        datos = []
        bd = Coneccion()
        no = parametros['email'].replace("@cetis155.edu.mx","")
        print("-----------Control")
        print(no)
        datos.append(no)
        datos.append(request.form['curp'])
        datos.append(request.form['grado'])
        print("------------------grupo :v")
        print(str(bd.seleccion("grupo","idgrupo","letra = '"+str(request.form['grupo'])+"'")[0][0]))
        datos.append(str(bd.seleccion("grupo","idgrupo","letra = '"+str(request.form['grupo'])+"'")[0][0]))
        print(datos)
        #bd.insertarRegistro("alumnos",datos)
        bd.exit()
        return redirect(url_for("index"))

    return redirect(url_for("index"))

@app.route('/a')
def a():
    parametros = dict(session)['profile']
    return render_template('a.html', parametros = parametros)

@app.route('/tutorias')
def tutorias():
    parametros = dict(session)['profile']
    return render_template('tutoriasapp.html', parametros = parametros)

@app.route('/pagos')
def pagos():
    parametros = dict(session)['profile']
    return render_template('pagos.html', parametros = parametros)

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
    horario = str(parametros['grado']) + str(parametros['grupo']) 
    print("------------------")
    print(horario)
    return render_template('agenda.html', parametros = parametros,archivo=horario)

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

@app.route('/insnot/<string:nom>', methods=['GET', 'POST'])
def agregar_noticia(nom=None):
    if request.method == 'POST':
        datos = []
        datos.append(request.form['titulo'+nom])
        datos.append(request.form['descripcion'+nom])
        if nom == "noticias" or nom == "concursos":
            datos.append(request.form['img'+nom])
        datos.append(request.form['fecha'+nom])
        print("----------nom")
        print(nom)
        bd = Coneccion()
        bd.insertarRegistro(nom, datos)
        bd.exit()
    
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
    app.run(debug=True, ssl_context='adhoc', threaded=True)
