# import sys
# import numpy as np
# sys.path.append('C:/Users/jezar/Downloads/DGTIPOCKET/')
# from pagina_android.python.pywopd import *
# from pagina_android.python.bd import *
# import xlrd

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

import pymysql 

try:
    conexion = pymysql.connect(  #Se conecta a la base de datos
                
                host='localhost',
                port=3306,
                user='root',
                password='',
                db='prototipos'
            )
except pymysql.Error as e:
            print("Error en la conexión 1: {0}".format(e))

try:
    conexion2 = pymysql.connect(  
                
                host='localhost',
                port=3306,
                user='root',
                password='',
                db='root$prototipos'
            )
except pymysql.Error as e:
            print("Error en la conexión 2: {0}".format(e))