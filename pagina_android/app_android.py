from flask import Flask, render_template,redirect,url_for, request, session
from authlib.integrations.flask_client import OAuth
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
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

# XDDDDDDDD
# Session config
app.secret_key = os.getenv("APP_SECRET_KEY")

FLOW_SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
CLIENT_SECRETS_FILE = os.path.expanduser('~/DGTIPOCKET/pagina_android/credentials.json')
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, FLOW_SCOPES)
auth_url, _ = flow.authorization_url(prompt='consent')

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
    client_kwargs={'scope': 'openid email profile https://www.googleapis.com/auth/calendar'},
)

# Definir una ruta para la página principal
@app.route('/')
@login_required
def index():
    bd = Coneccion()
    noticias = bd.obtenerTablas("noticias")
    bd.exit()
    print("---------------sesion")
    print(dict(session))
    parametros = dict(session)['profile']
    toks = dict(session)['tok_info']

    print("session token")
    print(toks)

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = Credentials.from_authorized_user_info(toks, SCOPES)
    print("----------creds")
    print(creds)

    if not creds:
        print("-------------not creds")
    if not creds.valid:
        print("----------------not creds valid")

    # if not creds or not creds.valid:
    #     print("token no valido por alguna razon :v")
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         # flow = InstalledAppFlow.from_client_secrets_file(
    #         #     "credentials.json", SCOPES
    #         # )
    #         # creds = flow.run_local_server(port=0)
    #         print("no hay un refresh token")        

    # try:
    #     service = build("calendar", "v3", credentials=creds)

    #     # Call the Calendar API
    #     now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    #     print("Getting the upcoming 10 events")
    #     events_result = (
    #         service.events().list(
    #             calendarId="primary",
    #             timeMin=now,
    #             maxResults=10,
    #             singleEvents=True,
    #             orderBy="startTime",
    #         ).execute()
    #     )
    #     events = events_result.get("items", [])

    #     if not events:
    #         print("No upcoming events found.")

    #     # Prints the start and name of the next 10 events
    #     for event in events:
    #         start = event["start"].get("dateTime", event["start"].get("date"))
    #         print(start, event["summary"])

    #     print("---------------events?")
    #     print(events)

    # except HttpError as error:
    #     print(f"An error occurred: {error}")

    return render_template('indexapp.html', parametros = parametros,noticias=noticias)

@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    tokens = {'client_id':os.getenv("GOOGLE_CLIENT_ID"),'client_secret': os.getenv("GOOGLE_CLIENT_SECRET"),'refresh_token':token.get('refresh_token'), 'access_token':token.get('access_token'), 'token_uri': 'https://oauth2.googleapis.com/token'}

    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    session['profile'] = user_info
    session['tok_info'] = tokens
    print("---------------toks")
    print(tokens)
    # with open("token.txt", "w") as tok:
    #     tok.write(str(token))
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
    return render_template('terminarR.html', parametros = parametros)


@app.route('/insertainfo', methods=['GET', 'POST'])
@login_required
def insertainfo():
    if request.method == 'POST':
        
        curp=request.form['curp']
        grado=request.form['grado']
        grupo=request.form['grupo']
        parametros = dict(session)['profile']
        session['profile'] = parametros.update({'curp': curp,'grado':grado,'grupo':grupo})
        parametros = dict(session)['profile']
        print("=========== nuevos parametros")
        print(parametros)
        return redirect(url_for("index"))

        
    
    para = dict(session)['profile']
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
