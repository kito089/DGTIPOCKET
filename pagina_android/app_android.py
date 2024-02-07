from flask import Flask, render_template,redirect,url_for, request, session, send_file, send_from_directory
import requests
import json
import time

from io import BytesIO
import matplotlib.pyplot as plt
import base64
from bs4 import BeautifulSoup

from python.bd import *
from python.pywopd import *
from python.funciones_auth import *

import os
import os.path
from dotenv import load_dotenv

from pip._vendor import cachecontrol
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

#project_folder = os.path.expanduser('~/DGTIPOCKET/pagina_android')
#project_folder = 'C:/Users/jezar/Downloads/DGTIPOCKET/pagina_android'
project_folder = '/home/kito089/kito089/prepa/prototipos/DGTIPOCKET/pagina_android'
load_dotenv(os.path.join(project_folder, '.env'))

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = 'C:/Users/jezar/Downloads/DGTIPOCKET/editar_word'
app.config['UPLOAD_FOLDER'] = '/home/kito089/kito089/prepa/prototipos/DGTIPOCKET/editar_word'
#app.config['UPLOAD_FOLDER'] = os.path.expanduser('~/DGTIPOCKET/editar_word')
app.config['ALLOWED_EXTENSIONS'] = set()
app.secret_key = os.getenv("APP_SECRET_KEY")

client_secrets_file = os.path.join(project_folder, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["openid", "https://www.googleapis.com/auth/userinfo.email", 
            "https://www.googleapis.com/auth/userinfo.profile", 
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/drive.readonly", 
            "https://www.googleapis.com/auth/drive.file"],
    redirect_uri="https://127.0.0.1:5000/authorize"
)

@app.route('/')
@login_required
def index():
    bd = Coneccion()
    noticias = bd.obtenerTablas("noticias")
    avisos = bd.obtenerTablas("avisos")
    concursos = bd.obtenerTablas("concursos")
    bd.exit()
    parametros = dict(session)['profile']

    if parametros['persona'] == 'maestro':
        return render_template('autoridades/funcionesMaestros.html', parametros=parametros, noticias=noticias, avisos=avisos)
    elif parametros['persona'] == 'programador':
        return render_template('autoridades/indexP.html', parametros = parametros,noticias=noticias, avisos=avisos, concursos=concursos)
    else:
        return render_template('indexapp.html', parametros = parametros,noticias=noticias, avisos=avisos, concursos=concursos)

###         INISIO DE SESION        ###

@app.route('/carga')
def carga():
    return render_template("intro.html")

@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    print("state-------",state)
    return redirect(authorization_url)

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

@app.route("/authorize")
def authorize():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        print("State does not match!")

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=os.getenv("GOOGLE_CLIENT_ID"), 
        clock_skew_in_seconds=60
    )

    session['credentials'] = credentials_to_dict(credentials)
    #session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    print("sesion --------",session)
    print("--------------------------------------")
    print(id_info['email'][0])
    if str.isnumeric(id_info['email'][0]):
        id_info.update({'persona':'alumno'})
        session['profile'] = id_info
        return redirect('/terminar')
    else:
        id_info.update({'persona':'maestro'})
        session['profile'] = id_info
        return redirect('/m')

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

###         PRIMER REGISTRO DE SESION       ###

@app.route('/terminar')
@login_required
def terinar():
    parametros = dict(session)['profile']
    bd = Coneccion()
    no = parametros['email'].replace("@cetis155.edu.mx","")
    curp =  bd.seleccion("alumnos", "curp","no_control = "+str(no))
    grado =  bd.seleccion("alumnos", "grado","no_control = "+str(no))
    bd.exit()
    
    if len(grado)>0 and len(curp)>0:
        bd = Coneccion()
        grupo = bd.seleccion("grupo","letra","idgrupo = "+str(bd.seleccion("alumnos","grupo_idgrupo","no_control = "+str(no))[0][0]))[0][0]
        bd.exit()
        print(grupo)
        parametros.update({'curp': curp[0][0],'grado':grado[0][0], 'grupo':grupo})
        session['profile'] = parametros
        return redirect(url_for("index"))  
    return render_template('inisioSesion/terminarR.html', parametros = parametros)

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

# @app.route('/logout')
# def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect(url_for('carga'))

###         FUNCIONES DE SESION         ###

@app.route('/config')
def config():
    parametros = dict(session)['profile']
    return render_template('inisioSesion/config.html', parametros = parametros)

@app.route('/menu')
def menu():
    parametros = dict(session)['profile']
    return render_template('inisioSesion/menu.html', parametros = parametros)

@app.route('/funciones')
def funciones():
    parametros = dict(session)['profile']
    return render_template('inisioSesion/funcionesapp.html', parametros = parametros)

###         FUNCIONES SIMPLES       ###

@app.route('/agenda')
def agenda():
    parametros = dict(session)['profile']
    horario = str(parametros['grado']) + str(parametros['grupo']) 
    print("------------------")
    print(horario)
    return render_template('funciones/agenda.html', parametros = parametros,archivo=horario)

@app.route('/pagos')
def pagos():
    parametros = dict(session)['profile']
    return render_template('funciones/pagos.html', parametros = parametros)

@app.route('/servicio')
def servicio():
    parametros = dict(session)['profile']
    return render_template('funciones/servicio.html', parametros = parametros)

@app.route('/historial')
def historial():
    plot_url = generate_plot()
    parametros = dict(session)['profile']
    return render_template('funciones/historial.html', parametros = parametros,plot_url=plot_url)

@app.route('/actualizar_info', methods = ['POST', 'GET'])
def actualizar():
    parametros = dict(session)['profile']
    db = Coneccion()
    datos = db.seleccion("alumnos","*","no_control = '"+parametros['email'].replace("@cetis155.edu.mx","")+"'")[0]
    print(datos)
    db.exit
    if request.method == 'POST':
        for i in range(3):
            datos[i+2] = request.form['A'+str(i)]
        db = Coneccion()
        db.actualizarRegistro("alumnos",datos[0],datos[1:])
        db.exit
        return redirect(url_for("logout"))
    db = Coneccion()
    grupos = db.seleccion("grupo","idgrupo, letra","true")
    db.exit()
    return render_template('inisioSesion/cambio.html', parametros=parametros, grupos = grupos)
    
#######################################################################################
@app.route('/planteles')                                                              #
def planteles1():                                                                     #
    parametros = dict(session)['profile']                                             #
    return render_template('funciones/plantelesapp.html', parametros = parametros)    #
                                                                                      #
@app.route('/organigrama')                                                            #
def organigrama():                                                                    #
    parametros = dict(session)['profile']                                             #
    return render_template('funciones/organigrama.html', parametros = parametros)     #
#######################################################################################

###         FUNCIONES DETALLADAS        ###

@app.route('/descargar/<string:archivo>')
def descargar(archivo):
    try:
        return send_file(archivo, as_attachment=True)
    finally:
        if os.path.exists(archivo):
            os.remove(archivo)
            print(f'Archivo {archivo} eliminado correctamente.')

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

    genboletadocx(datosC, datosG)
    word = os.path.expanduser('~/DGTIPOCKET/editar_word/'+nombr[0]+"_"+nombr[1]+'.docx')
    docx2pdf(word)
    pdf = os.path.expanduser('~/DGTIPOCKET/editar_word/'+nombr[0]+"_"+nombr[1]+'.pdf')
    
    return redirect(url_for("/descargar", archivo = pdf))
    # try:
    #     return send_file(pdf, as_attachment=True)
    # finally:
    #     if os.path.exists(pdf):
    #         os.remove(pdf)
    #         print(f'Archivo {pdf} eliminado correctamente.')

@app.route('/tabla/<string:table>')
def tabla(table):
    parametros = dict(session)['profile']
    bd = Coneccion()
    atributos = bd.obtenerAtributos(table)
    datos = bd.obtenerTablas(table)
    tab2 = ""

    if "_id" in atributos[-1]:
        for a in atributos[-1]:
            if a != "_":
                tab2 += a
            else:
                break

        atributos.pop(-1)
        atributos.append(tab2)

        for dato in datos:
            dato.append(bd.seleccion(tab2, "nombre", "id"+str(tab2)+"="+str(dato[-1]))[0][0])
            dato.pop(-2)
    bd.exit()
    return render_template('autoridades/funcionesAut/tabla.html', parametros = parametros, atributos = atributos, datos = datos, table = table)

@app.route('/clubs')
def clubs():
    parametros = dict(session)['profile']
    bd = Coneccion()
    clubs = bd.obtenerTablas("clubs")
    bd.exit()
    return render_template('funciones/clubapp.html', parametros = parametros, clubs=clubs)

@app.route('/chamilo')
def chamilo():
    parametros = dict(session)['profile']
    return render_template('funciones/chamilo.html', parametros = parametros)

@app.route('/tutorias')
def tutorias():
    parametros = dict(session)['profile']
    bd = Coneccion()
    tut = bd.obtenerTablas("tutorias")
    tuto = []
    for i in tut:
        tuto.append([])
        for j in tut:
            if str(j).isdigit():
                tuto.append(bd.seleccion("materias","nombre","idmaterias = "+str(j))[0][0])
            else:
                tuto.append(j)
    bd.exit()
    return render_template('funciones/tutoriasapp.html', parametros = parametros, tutorias = tuto)

@app.route('/noticias')                         #pendiente css
def noticias():
    bd = Coneccion()
    noticias = bd.obtenerTablas("noticias")
    bd.exit()
    parametros = dict(session)['profile']
    return render_template('funciones/noticiasapp.html', noticias=noticias, parametros = parametros)

@app.route('/descargarDrive/<string:idC>/<string:nom>')
def descargarDrive(idC, nom):
    credentials = google.oauth2.credentials.Credentials(**session['credentials'])
    drive = build("drive", "v3", credentials=credentials)
    print("entre al servicio uwu")

    file_path = file_path = f"{app.config['UPLOAD_FOLDER']}/{nom}"
    try:
        request = drive.files().get_media(fileId=idC)
        with io.FileIO(file_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while not done:
                status, done = downloader.next_chunk()

        print(f"File '{nom}' downloaded and saved to '{file_path}'.")
        # Asegúrate de que la función descargar no sea llamada aquí
    except Exception as e:
        print(f"Error during file download: {e}")
        # Maneja cualquier error que pueda ocurrir durante la descarga

    # Si necesitas hacer algo más después de descargar, agrégalo aquí

    return send_from_directory(app.config['UPLOAD_FOLDER'], nom, as_attachment=True)

@app.route('/cuadernillo')
@creds_required
def cuadernillo():
    parametros = dict(session)['profile']
    try:
        credentials = google.oauth2.credentials.Credentials(**session['credentials'])
        drive = build("drive", "v3", credentials=credentials)
        print("entre al servicio uwu")
        #'https://drive.google.com/drive/folders/1qTATX3XvoeQUGmlDSyNwZtcQehbuxRAR?usp=sharing'
        folder_id = '1qTATX3XvoeQUGmlDSyNwZtcQehbuxRAR'

        # Lista de archivos en el folder
        results = drive.files().list(q=f"'{folder_id}' in parents", 
                                       fields="files(id, name, mimeType, thumbnailLink, webViewLink)").execute()
        files = results.get('files', [])
        if not files:
            print('No files found in the specified folder.')
            return render_template('funciones/cuadernillo.html', parametros = parametros, cuadernillos = "Vacio")
        else:
            print('Files in the folder:')
            print(files)
            cuadernillos = []
            bd = Coneccion()
            for file in files:
                gg = bd.seleccion("cuadernillos","grado, grupo_idgrupo","nombre = '"+str(file['name'])+"' and idcuad = '"+str(file['id'])+"'")[0]
                print(gg)
                if len(gg) > 0:
                    le = bd.seleccion("grupo","letra","idgrupo = '"+str(gg[1])+"'")
                    print("le: ",le, len(le))
                    if (int(gg[0]) == int(parametros['grado']) or int(parametros['grado']) == 0) and (len(le[0]) > 0 or str(gg[1]) == "None"):
                        print("condiciones cumplidas :D")
                        ruta = f"{app.config['UPLOAD_FOLDER']}/{file['name']}"
                        cuadernillos.append([file['thumbnailLink'], file['name'], file['webViewLink'], file['id'], ruta])
                else:
                    print("cuadernillo no agregado a la bd")
            bd.exit()
            print("cuadernillos: ",cuadernillos)
            return render_template('funciones/cuadernillo.html', parametros = parametros, cuadernillos=cuadernillos)
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f"An error occurred: {error}")
        return f"An error occurred: {error}"

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

    return render_template('autoridades/indexMaestros.html', parametros = parametros,noticias=noticias, avisos=avisos, concursos=concursos)#,archivo=archivo)

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

    return render_template('autoridades/indexP.html', parametros = parametros,noticias=noticias, avisos=avisos, concursos=concursos)#,archivo=archivo)

@app.route('/Mconfig')
def Mconfig():
    parametros = dict(session)['profile']
    return render_template('autoridades/configMaestros.html', parametros = parametros)

@app.route('/Mfunciones')
def Mfunciones():
    parametros = dict(session)['profile']
    return render_template('autoridades/funcionesMaestros.html', parametros = parametros)

@app.route('/insDat/<string:nom>', methods=['GET', 'POST']) ### INSERTAR NOTICIAS AVISOS CONCURSOS
def insDat(nom=None):
    parametros = dict(session)['profile']
    tab2 = ""
    comb = None
    bd = Coneccion()
    atr = bd.obtenerAtributos(nom)
    bd.exit()
    if request.method == 'POST':
        datos = []
        for i in range(len(atr)-1):
            print("obteniendo: A"+str(i))
            datos.append(request.form['A'+str(i)])
        bd = Coneccion()
        bd.insertarRegistro(nom, datos)
        bd.exit()
        if nom == "noticias" or nom == "avisos" or nom == "concursos":
            return render_template('autoridades/funcionesAut/insnot.html', parametros = parametros)
        else:
            return redirect(url_for('tabla', table = nom))
    if nom == "noticias" or nom == "avisos" or nom == "concursos":
        return render_template('autoridades/funcionesAut/insnot.html', parametros = parametros)
    else:
        if "_id" in atr[-1]:
            for a in atr[-1]:
                if a != "_":
                    tab2 += a
                else:
                    break

            atr.pop(-1)
            atr.append(tab2)

            bd = Coneccion()
            comb = bd.seleccion(tab2, "id"+tab2+",nombre", "true")
            bd.exit()
        
        return render_template('autoridades/funcionesAut/agred.html', parametros = parametros, atributos = atr, tabla= nom, comb=comb)

@app.route('/edDat/<string:tabla>/<string:ide>', methods=['POST', 'GET'])
def edDat(tabla, ide):
    parametros = dict(session)['profile']
    datos = []
    tab2 = ""
    comb = None
    bd = Coneccion()
    atr = bd.obtenerAtributos(tabla)
    bd.exit()
    if request.method == 'POST':
        for i in range(len(atr)-1):
            datos.append(request.form['A'+str(i)])
        bd = Coneccion()
        bd.actualizarRegistro(tabla,ide,datos)
        bd.exit()
        return redirect(url_for('tabla',table=tabla))
    bd = Coneccion()
    datos = bd.seleccion(tabla,"*","id"+str(tabla)+" = "+str(ide))
    bd.exit()
    if "_id" in atr[-1]:
        for a in atr[-1]:
            if a != "_":
                tab2 += a
            else:
                break

        atr.pop(-1)
        atr.append(tab2)

        bd = Coneccion()
        comb = bd.seleccion(tab2, "id"+tab2+",nombre", "true")
        bd.exit()
        datos[0].pop(-1)
        datos.append(comb[0][-1])
    return render_template('autoridades/funcionesAut/agred.html', parametros = parametros, atributos = atr, datos = datos, tabla = tabla, ide = ide, comb=comb)

@app.route("/delDat/<string:tabla>/<string:id>")
def delDat(tabla, id):
    bd = Coneccion()
    bd.eliminarRegistro(tabla, id)
    bd.exit()
    return redirect(url_for('tabla',table=tabla))

def extencion(arch):
    if '.' not in arch:
        return False
    ext = arch.rsplit('.', 1)[1].lower()
    return ext in {'xls', 'xlsx'}

@app.route("/cargaArch/<string:regis>/<string:archivo>/<string:ti>")
def cargaArch(regis, archivo, ti):
    return render_template("autoridades/funcionesAut/carga.html", regis = regis, archivo=archivo, ti=ti)

@app.route("/subirCal", methods = ['POST', 'GET'])
def subibrCal():
    parametros = dict(session)['profile']
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No se encontro el archivo"

        file = request.files['file']

        if file.filename == '':
            return "Archivo no seleccionado"

        if file and extencion(file.filename):
            file.save(f"{app.config['UPLOAD_FOLDER']}/{file.filename}")
            print("moviendo para insertar calificaciones")
            return redirect(url_for("cargaArch", regis = "Alumnos", archivo = file.filename, ti=str(1)))
        else:
            return "Extension del archivo no permitida"
    return render_template("autoridades/funcionesAut/insCal.html", parametros= parametros)

def obtGrupo(grupo, esp, turno):
    if esp == "PROGRAMACIÓN":
        if turno == "matutino":
            return str(grupo[0])+"A"
        else:
            return str(grupo[0])+"G"
    elif esp == "SOPORTE Y MANTENIMIENTO DE EQUIPO DE CÓMPUTO":
        if turno == "matutino":
            return str(grupo[0])+"B"
        else:
            return str(grupo[0])+"H"
    elif esp == "ADMINISTRACIÓN DE RECURSOS HUMANOS":
        if turno == "matutino":
            if grupo[1] == "A":
                return str(grupo[0])+"C"
            elif grupo[1] == "B":
                return str(grupo[0])+"D"
            else:
                return str(grupo[0])+"E"
        else:
            if grupo[1] == "A":
                return str(grupo[0])+"I"
            elif grupo[1] == "B":
                return str(grupo[0])+"J"
            else:
                return str(grupo[0])+"K"
    elif esp == "MANTENIMIENTO AUTOMOTRIZ":
        if turno == "matutino":
            return str(grupo[0])+"F"
        else:
            return str(grupo[0])+"L"
    else:
        return grupo

@app.route("/leerAlumnos/<string:nombre>/<string:time>")
def leerAlumnos(nombre, time):
    print("accediendo al archivo (alumnos)")
    ruta = os.path.expanduser('~/DGTIPOCKET/editar_word/'+nombre)
    with open(ruta, 'r', encoding='MacRoman') as archivo_html:
        contenido_html = archivo_html.read()
    soup = BeautifulSoup(contenido_html, 'html.parser')
    tabla = soup.find('table')
    pri = True
    #print("time : ",time)
    x = int(time)*1000
    cu = (int(time)-1)*1000 
    y = 0
    if tabla:
        db = Coneccion()
        for fila in tabla.find_all('tr'):
            datos_celda = [celda.text.strip() for celda in fila.find_all(['th', 'td'])]
            if pri:
                if datos_celda != ['CLV_CENTRO', 'PLANTEL', 'CARRERA', 'GENERACION', 'TURNO', 'SEMESTRE', 'GRUPO', 'NO CONTROL', 'NOMBRE', 'PATERNO', 'MATERNO', 'CURP', 'NOMBRE ASIGNATURA', 'PARCIAL 1', 'PARCIAL 2', 'PARCIAL 3', 'CALIFICACION', 'PERIODO', 'FIRMADO', 'FIRMA', 'ASISTENCIAS 1', 'ASISTENCIAS 2', 'ASISTENCIAS 3', 'TOTAL ASISTENICIAS', 'TIPO ACREDITACION']:
                    return "Formato del excel no compatible"
            else:
                if cu <= x and y >= cu:
                    caracteres = {"”": "Ó", "Õ": "Í", "¡": "Á", "…": "É", "⁄": "Ú", "—": "Ñ"}
                    tabCam= str.maketrans(caracteres)
                    datos_celda = [cadena.translate(tabCam) for cadena in datos_celda]
                    datos_celda[6] = obtGrupo(datos_celda[6], datos_celda[2], datos_celda[4])
                    #print(datos_celda[2],datos_celda[4],datos_celda[6],datos_celda[7],datos_celda[11],datos_celda[12],datos_celda[13],datos_celda[14],datos_celda[15],datos_celda[17],datos_celda[20],datos_celda[21],datos_celda[22],datos_celda[24])
                    if not(len(db.seleccion("alumnos","*","no_control = '"+datos_celda[7]+"'")) > 0):
                        grupo = db.seleccion("grupo","idgrupo","letra = '"+datos_celda[6][1]+"'")[0][0]
                        datos = [datos_celda[7],datos_celda[11],datos_celda[6][0],str(grupo)]
                        db.insertarRegistro("alumnos", datos)
                        print(datos)
                    else:
                        igg = db.seleccion("alumnos","idalumnos, grado, grupo_idgrupo", "no_control = '"+datos_celda[7]+"'")[0]
                        gru = db.seleccion("grupo","letra","idgrupo = '"+str(igg[2])+"'")[0][0]
                        if int(igg[1]) != int(datos_celda[6][0]):
                            db.actualizarDato("alumnos",str(igg[0]),datos_celda[6][0],"grado")
                        if str(gru) != datos_celda[6][1]:
                            db.actualizarDato("alumnos", str(igg[0]), datos_celda[6][1], "grupo")
                        print("------------------alumnos en la bd")
            if cu > x:
                print("fin de metodo: time: ", time)
                return redirect(url_for("cargaArch", regis = "Alumnos", archivo = nombre, ti = str(int(time)+1)))
            if y >= cu:
                cu += 1
                y+=1
            else:
                y+=1      
            pri = False
            #print("cu: ", cu)
            #print("y: ", y)
        db.exit()
        return redirect(url_for("cargaArch", regis = "TC", archivo = nombre, ti = str(1)))
    else:
        return "No se encontró ninguna tabla en el xls."

@app.route("/leerE/<string:nombre>/<string:time>")
def leerE(nombre, time):
    print("accediendo al archivo (especialidad)")
    ruta = os.path.expanduser('~/DGTIPOCKET/editar_word/'+nombre)
    with open(ruta, 'r', encoding='MacRoman') as archivo_html:
        contenido_html = archivo_html.read()
    soup = BeautifulSoup(contenido_html, 'html.parser')
    tabla = soup.find('table')
    pri = True
    #print("time : ",time)
    x = int(time)*1000
    cu = (int(time)-1)*1000 
    y = 0
    if tabla:
        db = Coneccion()
        for fila in tabla.find_all('tr'):
            datos_celda = [celda.text.strip() for celda in fila.find_all(['th', 'td'])]
            if pri:
                if datos_celda != ['CLV_CENTRO', 'PLANTEL', 'CARRERA', 'GENERACION', 'TURNO', 'SEMESTRE', 'GRUPO', 'NO CONTROL', 'NOMBRE', 'PATERNO', 'MATERNO', 'CURP', 'NOMBRE ASIGNATURA', 'PARCIAL 1', 'PARCIAL 2', 'PARCIAL 3', 'CALIFICACION', 'PERIODO', 'FIRMADO', 'FIRMA', 'ASISTENCIAS 1', 'ASISTENCIAS 2', 'ASISTENCIAS 3', 'TOTAL ASISTENICIAS', 'TIPO ACREDITACION']:
                    return "Formato del excel no compatible"
            else:
                if cu <= x and y >= cu:
                    caracteres = {"”": "Ó", "Õ": "Í", "¡": "Á", "…": "É", "⁄": "Ú", "—": "Ñ"}
                    tabCam= str.maketrans(caracteres)
                    datos_celda = [cadena.translate(tabCam) for cadena in datos_celda]
                    datos_celda[6] = obtGrupo(datos_celda[6], datos_celda[2], datos_celda[4])
                    #print(datos_celda[2],datos_celda[4],datos_celda[6],datos_celda[7],datos_celda[11],datos_celda[12],datos_celda[13],datos_celda[14],datos_celda[15],datos_celda[17],datos_celda[20],datos_celda[21],datos_celda[22],datos_celda[24])
                    idm = db.seleccion("submodulos","idsubmodulos","nombre = '"+datos_celda[12]+"'")
                    if (len(idm) > 0):
                        al = db.seleccion("alumnos","idalumnos","no_control = '"+datos_celda[7]+"'")[0][0]
                        if (int(datos_celda[7][1]) <= 2 and len(idm) > 1) or len(idm) > 0:
                            idm = idm[0][0]
                        else:
                            idm = idm[0][1] 
                        datos = [datos_celda[13],datos_celda[14],datos_celda[15],datos_celda[20],datos_celda[21],datos_celda[22],
                                datos_celda[17],datos_celda[24],str(idm),str(al)]
                        pre = db.seleccion("evaluacion_e","idevaluacion_e","periodo = '{}' and acreditacion = '{}' and submodulos_idsubmodulos = '{}' and alumnos_idalumnos = '{}'".format(datos_celda[17],datos_celda[24],idm,al))
                        if len(pre) > 0:
                            print("calificacion ya en la bd")
                        else:
                            db.insertarRegistro("evaluacion_e",datos)
                    else:
                        print("materia no encontrada: "+str(datos_celda[12]))
            if cu > x:
                print("fin de metodo: time: ", time)
                return redirect(url_for("cargaArch", regis = "E", archivo = nombre, ti = str(int(time)+1)))
            if y >= cu:
                cu += 1
                y+=1
            else:
                y+=1      
            pri = False
            #print("cu: ", cu)
            #print("y: ", y)
        db.exit()
        print("fin de metodo: time: ", time)
        if os.path.exists(ruta):
            os.remove(ruta)
            print(f'Archivo {ruta} eliminado correctamente.')
        return redirect(url_for("index_maestros"))
    else:
        print("No se encontró ninguna tabla en el xls.")

@app.route("/leerTC/<string:nombre>/<string:time>")
def leerTC(nombre, time):
    print("accediendo al archivo (tronco comun)")
    ruta = os.path.expanduser('~/DGTIPOCKET/editar_word/'+nombre)
    with open(ruta, 'r', encoding='MacRoman') as archivo_html:
        contenido_html = archivo_html.read()
    soup = BeautifulSoup(contenido_html, 'html.parser')
    tabla = soup.find('table')
    pri = True
    #print("time : ",time)
    x = int(time)*1000
    cu = (int(time)-1)*1000
    y=0
    if tabla:
        db = Coneccion()
        for fila in tabla.find_all('tr'):
            datos_celda = [celda.text.strip() for celda in fila.find_all(['th', 'td'])]
            if pri:
                if datos_celda != ['CLV_CENTRO', 'PLANTEL', 'CARRERA', 'GENERACION', 'TURNO', 'SEMESTRE', 'GRUPO', 'NO CONTROL', 'NOMBRE', 'PATERNO', 'MATERNO', 'CURP', 'NOMBRE ASIGNATURA', 'PARCIAL 1', 'PARCIAL 2', 'PARCIAL 3', 'CALIFICACION', 'PERIODO', 'FIRMADO', 'FIRMA', 'ASISTENCIAS 1', 'ASISTENCIAS 2', 'ASISTENCIAS 3', 'TOTAL ASISTENICIAS', 'TIPO ACREDITACION']:
                    return "Formato del excel no compatible"
            else:
                if cu <= x and y >= cu:
                    caracteres = {"”": "Ó", "Õ": "Í", "¡": "Á", "…": "É", "⁄": "Ú", "—": "Ñ"}
                    tabCam= str.maketrans(caracteres)
                    datos_celda = [cadena.translate(tabCam) for cadena in datos_celda]
                    datos_celda[6] = obtGrupo(datos_celda[6], datos_celda[2], datos_celda[4])
                    #print(datos_celda[2],datos_celda[4],datos_celda[6],datos_celda[7],datos_celda[11],datos_celda[12],datos_celda[13],datos_celda[14],datos_celda[15],datos_celda[17],datos_celda[20],datos_celda[21],datos_celda[22],datos_celda[24])
                    if cu <= x:
                        idm = db.seleccion("materias","idmaterias","nombre = '"+datos_celda[12]+"'")
                        if (len(idm) > 0):
                            al = db.seleccion("alumnos","idalumnos","no_control = '"+datos_celda[7]+"'")[0][0]
                            if (int(datos_celda[7][1]) <= 2 and len(idm) > 1) or len(idm) > 0:
                                idm = idm[0][0]
                            else:
                                idm = idm[0][1] 
                            datos = [datos_celda[13],datos_celda[14],datos_celda[15],datos_celda[20],datos_celda[21],datos_celda[22],
                                    datos_celda[17],datos_celda[24],str(idm),str(al)]
                            pre = db.seleccion("evaluacion_tc","idevaluacion_tc","periodo = '{}' and acreditacion = '{}' and materias_idmaterias = '{}' and alumnos_idalumnos = '{}'".format(datos_celda[17],datos_celda[24],idm,al))
                            if len(pre) > 0:
                                print("calificacion ya en la bd")
                            else:
                                db.insertarRegistro("evaluacion_tc",datos)
                        else:
                            print("materia no encontrada: "+str(datos_celda[12]))
            if cu > x:
                print("fin de metodo: time: ", time)
                return redirect(url_for("cargaArch", regis = "TC", archivo = nombre, ti = str(int(time)+1)))
            if y >= cu:
                cu += 1
                y+=1
            else:
                y+=1      
            pri = False
            #print("cu: ", cu)
            #print("y: ", y)
        db.exit()
        print("fin de metodo: time: ", time)
        return redirect(url_for("cargaArch", regis = "E", archivo = nombre, ti = str(1)))
    else:
        print("No se encontró ninguna tabla en el xls.")

@app.route("/driveMas", methods = ['POST', 'GET'])
@creds_required
def driveMas():
    if request.method == 'POST':
        cuader = request.files['Cuader']
        if cuader.filename == '':
            return "Archivo no seleccionado"
        if cuader:
            file_path = f"{app.config['UPLOAD_FOLDER']}/{cuader.filename}"
            cuader.save(file_path)

        try:
            credentials = google.oauth2.credentials.Credentials(**session['credentials'])
            drive = build("drive", "v3", credentials=credentials)
            print("entre al servicio uwu")

            #'https://drive.google.com/drive/folders/1qTATX3XvoeQUGmlDSyNwZtcQehbuxRAR?usp=sharing'
            folder_id = '1qTATX3XvoeQUGmlDSyNwZtcQehbuxRAR'

            file_metadata = {'name': cuader.filename, 'parents': [folder_id]}
            media = MediaFileUpload(file_path, mimetype='application/octet-stream')
            file = drive.files().create(body=file_metadata, media_body=media, fields='id').execute()
            print(f"File '{cuader.filename}' uploaded. ID: {file['id']}")

            if request.form['grupo'] == "nada":
                datos = [str(file['id']),str(cuader.filename),str(request.form['grado']), "@NULL"]
            else:
                datos = [str(file['id']),str(cuader.filename),str(request.form['grado']), str(request.form['grupo'])]
            bd = Coneccion()
            bd.insertarRegistro("cuadernillos",datos)
            bd.exit()

            if os.path.exists(file_path):
                os.remove(file_path)
                print(f'Archivo {file_path} eliminado correctamente.')
            return redirect(url_for("index_maestros"))
        except HttpError as error:
            print(f"An error occurred: {error}")
            return f"An error occurred: {error}"
        
    bd = Coneccion()
    letras = bd.obtenerTablas("grupo")
    bd.exit()
    parametros = dict(session)['profile']
    return render_template("autoridades/funcionesAut/subirDrive.html", letras = letras, parametros=parametros)

####            PRUEBAS             ####

@app.route('/a') ### ???? carlin epico papu
def a():
    parametros = dict(session)['profile']
    return render_template('pruebas/a.html', parametros = parametros)

@app.route('/a')
def pruebas():
    parametros = dict(session)['profile']
    return render_template('prueba.html', parametros = parametros)

def generate_plot():
    x = ['Fisica 2', 'CIENCIA, TECNOLOGÍA, SOCIEDAD Y VALORES', 'CÁLCULO INTEGRAL',
         'INGLÉS V', 'CONSTRUYE BASES DE DATOS PARA APLICACIONES WEB',
         'DESARROLLA APLICACIONES WEB CON CONEXIÓN A BASES DE DATOS']
    y = [5, 7, 9, 8, 10, 9]

    plt.bar(x, y, color='skyblue')
    plt.xlabel('Materias')
    plt.ylabel('Promedio')
    plt.title('Gráfico de Barras - Promedio')

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
