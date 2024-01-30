import sys
import numpy as np
sys.path.append('C:/Users/jezar/Downloads/DGTIPOCKET/')
from pagina_android.python.pywopd import *
from pagina_android.python.bd import *
import xlrd

# # Ruta al archivo Excel (xls)
# archivo_excel = r'C:\Users\jezar\Downloads\DGTIPOCKET\editar_word\detalle_calificaciones-arreglo.xls'

# # Abrir el archivo Excel
# libro_trabajo = xlrd.open_workbook(archivo_excel)

# # Seleccionar una hoja específica (por índice)
# hoja = libro_trabajo.sheet_by_index(0)

# # Obtener el número de filas y columnas
# num_filas = hoja.nrows
# num_columnas = hoja.ncols

# # Iterar sobre las filas y columnas
# for fila in range(num_filas):
#     for columna in range(num_columnas):
#         # Obtener el valor de la celda
#         valor = hoja.cell_value(fila, columna)
#         print(valor)

# # Cerrar el archivo Excel (xls)
# libro_trabajo.release_resources()

# import chardet

# def determinar_codificacion(archivo_path):
#     with open(archivo_path, 'rb') as archivo_binario:
#         resultado = chardet.detect(archivo_binario.read())
#     return resultado['encoding']

# # Ruta al archivo HTML
# archivo_html = r'C:\Users\jezar\Downloads\DGTIPOCKET\editar_word\detalle_calificaciones-copia.xls'

# # Determinar la codificación del archivo
# codificacion = determinar_codificacion(archivo_html)

# print(f"La codificación del archivo es: {codificacion}")

from bs4 import BeautifulSoup

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
    
# Cargar el archivo HTML
with open(r'C:\Users\jezar\Downloads\detalle_calificaciones (3).xls', 'r', encoding='MacRoman') as archivo_html:
    contenido_html = archivo_html.read()

# Crear un objeto BeautifulSoup
soup = BeautifulSoup(contenido_html, 'html.parser')

# Encontrar la tabla en el HTML
tabla = soup.find('table')
pri = True

# Verificar si se encontró la tabla
if tabla:
    # Iterar sobre las filas y columnas de la tabla
    db = Coneccion()
    for fila in tabla.find_all('tr'):
        # Obtener los datos de las celdas
        datos_celda = [celda.text.strip() for celda in fila.find_all(['th', 'td'])]
        if pri:
            if datos_celda != ['CLV_CENTRO', 'PLANTEL', 'CARRERA', 'GENERACION', 'TURNO', 'SEMESTRE', 'GRUPO', 'NO CONTROL', 'NOMBRE', 'PATERNO', 'MATERNO', 'CURP', 'NOMBRE ASIGNATURA', 'PARCIAL 1', 'PARCIAL 2', 'PARCIAL 3', 'CALIFICACION', 'PERIODO', 'FIRMADO', 'FIRMA', 'ASISTENCIAS 1', 'ASISTENCIAS 2', 'ASISTENCIAS 3', 'TOTAL ASISTENICIAS', 'TIPO ACREDITACION']:
                print("Formato del excel no compatible")
                break
        else:
            #print(datos_celda)
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
                print("alumnos en la bd")
                #break


            idm = db.seleccion("materias","idmaterias","nombre = '"+datos_celda[12]+"'")
            mat = True
            if not(len(idm) > 0):
                idm = db.seleccion("submodulos","idsubmodulos","nombre = '"+datos_celda[12]+"'")
                mat = False
                if not(len(idm) > 0):
                    mod = db.seleccion("modulos","idmodulos","nombre = '"+datos_celda[12]+"'")
            if (len(idm) > 0):
                al = db.seleccion("alumnos","idalumnos","no_control = '"+datos_celda[7]+"'")[0][0]
                #al = 0
                if (int(datos_celda[7][1]) <= 2 and len(idm) > 1) or len(idm) > 0:
                    idm = idm[0][0]
                else:
                    idm = idm[0][1] 
                print(idm)
                datos = [datos_celda[13],datos_celda[14],datos_celda[15],datos_celda[20],datos_celda[21],datos_celda[22],
                        datos_celda[17],datos_celda[24],str(idm),str(al)]
                print(datos)
                pre = db.seleccion("evaluacion_tc","idevaluacion_tc","periodo = '{}' and acreditacion = '{}' and materias_idmaterias = '{}' and alumnos_idalumnos = '{}'".format(datos_celda[17],datos_celda[24],idm,al))
                print(pre)
                if len(pre) > 0:
                    db.actualizarRegistro("evaluacion_tc",str(pre[0][0]),datos)
                else:
                    pre = db.seleccion("evaluacion_e","*","periodo = '{}' and acreditacion = '{}' and submodulos_idsubmodulos = '{}' and alumnos_idalumnos = '{}'".format(datos_celda[17],datos_celda[24],idm,al))
                    if len(pre) > 0:
                        db.actualizarRegistro("evaluacion_e",str(pre[0][0]),datos)
                    else:
                        if mat:
                            db.insertarRegistro("evaluacion_tc",datos)
                        else:
                            db.insertarRegistro("evaluacion_e",datos)
            elif len(mod) > 0:
                #al = db.seleccion("alumnos","idalumnos","no_control = '"+datos_celda[7]+"'")
                print("modulo encontrado: ",datos_celda[12])
            else:
                print("materia no encontrada: ", datos_celda[12])
                break
        pri = False
    db.exit()
else:
    print("No se encontró ninguna tabla en el xls.")