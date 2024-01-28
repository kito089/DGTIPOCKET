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

from bs4 import BeautifulSoup

# Cargar el archivo HTML
with open(r'C:\Users\jezar\Downloads\DGTIPOCKET\editar_word\detalle_calificaciones-copia.xls', 'r', encoding='MacRoman') as archivo_html:
    contenido_html = archivo_html.read()

# Crear un objeto BeautifulSoup
soup = BeautifulSoup(contenido_html, 'html.parser')

# Encontrar la tabla en el HTML
tabla = soup.find('table')

# Verificar si se encontró la tabla
if tabla:
    # Iterar sobre las filas y columnas de la tabla
    for fila in tabla.find_all('tr'):
        # Obtener los datos de las celdas
        datos_celda = [celda.text.strip() for celda in fila.find_all(['th', 'td'])]
        
        # Imprimir los datos de la fila
        #print(datos_celda)

        print(datos_celda[7],datos_celda[11],datos_celda[12],datos_celda[13],datos_celda[14],datos_celda[15],datos_celda[20],datos_celda[21],datos_celda[22])

else:
    print("No se encontró ninguna tabla en el HTML.")

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
    