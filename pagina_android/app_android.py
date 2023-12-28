from flask import Flask, render_template,redirect,url_for, request, session, send_file
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
from python.pywopd import *
import datetime
import json
import matplotlib.pyplot as plt

from io import BytesIO
import base64

from python.funciones_auth import login_required

from dotenv import load_dotenv

project_folder = os.path.expanduser('~/DGTIPOCKET/pagina_android')
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
    if parametros['persona'] == 'maestro':
        return render_template('indexMaestros.html', parametros=parametros, noticias=noticias, avisos=avisos)
    elif parametros['persona'] == 'programador':
        return render_template('indexP.html', parametros = parametros,noticias=noticias, avisos=avisos, concursos=concursos)#,archivo=archivo)
    else:
        return render_template('indexapp.html', parametros = parametros,noticias=noticias, avisos=avisos, concursos=concursos)#,archivo=archivo)

###         INISIO DE SESION        ###

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
    token.pop('userinfo')
    tokens.update(token)
    session['tok_info'] = tokens
    print("---------------toks")
    print(tokens)
    with open("token.txt", "w") as tok:
        tok.write(str(tokens))
    print("fin")
    #session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    if session['given_name']=='JULIO ENRIQUE' or session['name']=='HIRAM YAEL' :
        user_info.update({'persona':'programador'})
        session['profile'] = user_info
        return redirect('/p')
    elif str.isnumeric(user_info['email'][0]):
        user_info.update({'persona':'alumno'})
        session['profile'] = user_info
        return redirect('/terminar')
    
    else:
        user_info.update({'persona':'maestro'})
        session['profile'] = user_info
        return redirect('/m')

###         PRIMER REGISTRO DE SESION       ###

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
    curp =  bd.seleccion("alumnos", "curp","no_control = "+str(no))
    grado =  bd.seleccion("alumnos", "grado","no_control = "+str(no))
    bd.exit()
    print("------------ curp, grado y grupo")
    print(curp)
    print(grado)
    
    if len(grado)>0 and len(curp)>0:
        bd = Coneccion()
        grupo = bd.seleccion("grupo","letra","idgrupo = "+str(bd.seleccion("alumnos","grupo_idgrupo","no_control = "+str(no))[0][0]))[0][0]
        bd.exit()
        print(grupo)
        parametros.update({'curp': curp[0][0],'grado':grado[0][0], 'grupo':grupo})
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
        datos.append(no)
        datos.append(request.form['curp'])
        datos.append(request.form['grado'])
        datos.append(str(bd.seleccion("grupo","idgrupo","letra = '"+str(request.form['grupo'])+"'")[0][0]))
        bd.insertarRegistro("alumnos",datos)
        bd.exit()
        parametros.update({'curp':datos[1],'grado':datos[2], 'grupo':request.form['grupo']})
        session['profile'] = parametros
        return redirect(url_for("index"))

    return redirect(url_for("index"))

###     CIERRE DE SESION        ###

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('login'))

###         FUNCIONES DE SESION         ###

@app.route('/config')
def config():
    parametros = dict(session)['profile']
    return render_template('config.html', parametros = parametros)

@app.route('/menu')
def menu():
    parametros = dict(session)['profile']
    return render_template('menu.html', parametros = parametros)


@app.route('/funciones')
def funciones():
    parametros = dict(session)['profile']
    return render_template('funcionesapp.html', parametros = parametros)

###         FUNCIONES SIMPLES       ###

@app.route('/planteles')
def planteles1():
    parametros = dict(session)['profile']
    return render_template('plantelesapp.html', parametros = parametros)

@app.route('/organigrama')
def organigrama():
    parametros = dict(session)['profile']
    return render_template('organigrama.html', parametros = parametros)

@app.route('/clubs')
def clubs():
    parametros = dict(session)['profile']
    return render_template('clubapp.html', parametros = parametros)

@app.route('/tutorias')
def tutorias():
    parametros = dict(session)['profile']
    return render_template('tutoriasapp.html', parametros = parametros)

@app.route('/pagos')
def pagos():
    parametros = dict(session)['profile']
    return render_template('pagos.html', parametros = parametros)

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
    plot_url = generate_plot()
    parametros = dict(session)['profile']
    return render_template('historial.html', parametros = parametros,plot_url=plot_url)

@app.route('/cuadernillo')
def cuadernillo():
    parametros = dict(session)['profile']
    return render_template('cuadernillo.html', parametros = parametros)

###         FUNCIONES DETALLADAS        ###

@app.route('/boleta')
def boleta():
    parametros = dict(session)['profile']
    nombre = parametros["name"]
    if "�" in nombre:
        nombre = nombre.replace("�","Ñ")
    nom = nombre.split(" ")
    nombr = []
    nombr.append(nom[-2])
    nombr.append(nom[-1])
    if len(nom) == 4:
        nombr.append(nom[-4])
        nombr.append(nom[-3])
    else:
        nombr.append(nom[-3])

    bd = Coneccion()

    turesp = bd.llamar("turesp({0})".format(parametros["email"].replace("@cetis155.edu.mx","")))

    datosG = [parametros["email"],parametros["grado"]+parametros["grupo"],turesp[0][0],nombr,turesp[0][1]]

    ida = bd.seleccion("alumnos","idalumnos","no_control = {0}".format(parametros["email"].replace("@cetis155.edu.mx","")))

    tc = bd.llamar("boleta_tc({0})".format(ida[0][0]))
    m = bd.llamar("boleta_m({0})".format(ida[0][0]))
    e = bd.llamar("boleta_e({0})".format(ida[0][0]))

    bd.exit()

    datosC = conv(tc,e,m)

    genboletapdf(datosC, datosG)
    archivo = os.path.expanduser('~/DGTIPOCKET/editar_word/'+nombr[0]+"_"+nombr[1]+'.docx')
    
    return send_file(archivo, as_attachment=True)
    #ruta_docx = os.path.expanduser('~/DGTIPOCKET/editar_word/{0}.docx'.format(nombr[3][0]+"_"+nombr[3][1]))
    # word2pdf(ruta_docx)
    # ruta_pdf = os.path.expanduser('~/DGTIPOCKET/editar_word/{0}.pdf'.format(nombr[3][0]+"_"+nombr[3][1]))
    # #ruta_pdf = os.path.join(os.path.dirname(__file__), pdf_bol)

    # # Usa send_file para enviar el archivo PDF al navegador para su descarga
    # return send_file(
    #     ruta_pdf,
    #     as_attachment=True,
    #     download_name='{0}.pdf'.format(nombr),
    #     mimetype='application/pdf'
    # )

@app.route('/noticias')                         #pendiente css
def noticias():
    bd = Coneccion()
    noticias = bd.obtenerTablas("noticias")
    bd.exit()
    parametros = dict(session)['profile']
    return render_template('noticiasapp.html', noticias=noticias, parametros = parametros)

####        AUTORIDADES         ####

@app.route('/m')
@login_required
def index_maestros():
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

    return render_template('indexMaestros.html', parametros = parametros,noticias=noticias, avisos=avisos, concursos=concursos)#,archivo=archivo)
@app.route('/p')#+++++++++++++++++++++++++++++++++++++++++++++++index programador algo bien 
@login_required
def index_Programadores():
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

    return render_template('indexP.html', parametros = parametros,noticias=noticias, avisos=avisos, concursos=concursos)#,archivo=archivo)

@app.route('/Mconfig')
def Mconfig():
    parametros = dict(session)['profile']
    return render_template('configMaestros.html', parametros = parametros)

@app.route('/Mfunciones')
def Mfunciones():
    parametros = dict(session)['profile']
    return render_template('funcionesMaestros.html', parametros = parametros)

@app.route('/insnot/<string:nom>', methods=['GET', 'POST']) ### INSERTAR NOTICIAS
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

@app.route('/instaviso', methods=['GET', 'POST']) ### INSERTAR AVISOS
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

####            PRUEBAS             ####

@app.route('/a') ### ????
def a():
    parametros = dict(session)['profile']
    return render_template('a.html', parametros = parametros)

@app.route('/a')
def pruebas():
    parametros = dict(session)['profile']
    return render_template('prueba.html', parametros = parametros)

def generate_plot():
    # Datos de ejemplo
    x = ['Fisica 2', 'CIENCIA, TECNOLOGÍA, SOCIEDAD Y VALORES', 'CÁLCULO INTEGRAL',
         'INGLÉS V', 'CONSTRUYE BASES DE DATOS PARA APLICACIONES WEB',
         'DESARROLLA APLICACIONES WEB CON CONEXIÓN A BASES DE DATOS']
    y = [5, 7, 9, 8, 10, 9]

    # Crear el gráfico
    plt.plot(y)  # Solo necesitas los valores del eje y, no x
    plt.xlabel('Materias')
    plt.ylabel('Eje Y')
    plt.title('Gráfico de ejemplo  Promedio')

    # Personalizar etiquetas del eje x con rotación diagonal
    plt.xticks(range(len(x)), x, rotation=45, ha='right')

    # Guardar el gráfico en un BytesIO para mostrarlo en la página HTML
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Convertir la imagen a base64
    plot_url = base64.b64encode(img.getvalue()).decode()

    return plot_url

if __name__ == '__main__':
    app.run(debug=True, ssl_context='adhoc', threaded=True)
