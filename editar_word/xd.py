import sys
sys.path.append('C:/Users/jezar/Downloads/DGTIPOCKET/')
from pagina_android.python.pywopd import *
from pagina_android.python.bd import *

from jinja2 import Template

nombre = "JULIO ENRIQUE ZARI�AN RODDRIGUEZ"
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

ida = bd.seleccion("alumnos","idalumnos","no_control = 21301061550046")

tc = bd.llamar("boleta_tc({0})".format(ida[0][0]))
m = bd.llamar("boleta_m({0})".format(ida[0][0]))
e = bd.llamar("boleta_e({0})".format(ida[0][0]))

bd.exit()

datosG = ["21301061550046@cetis155.edu.mx","5A","MATUTINO",nombr,"PROGRAMACIÓN"]
datosC = conv(tc,e,m)

#boleta(datosC, datosG)

nombre=datosG[3][0]+" "+datosG[3][1]

controlx = datosG[0].replace("@cetis155.edu.mx","")
gen = controlx[0]+controlx[1]
nombr = ""
for i in range(len(datosG[3])):
    nombr = nombr +datosG[3][i]+" "

data = { 
    'control' : controlx,
    'nombre' : nombr,
    'semestre' : datosG[1][0],
    'carre' : datosG[4],
    'turno' : datosG[2],
    'grupo' : datosG[1],
    'gen' : "20"+gen+"-"+"20"+str(int(gen)+3),
    'boleta': datosC
}

# Plantilla Jinja2
with open('C:/Users/jezar/Downloads/DGTIPOCKET/editar_word/algo.html', 'r', encoding='utf-8') as file:
    template_str = file.read()

# Renderizar la plantilla
print(template_str)

template = Template(template_str)
rendered_content = template.render(data)

import os
from pyhtml2pdf import converter

with open('C:/Users/jezar/Downloads/DGTIPOCKET/editar_word/ejem.html', 'w', encoding='utf-8') as file:
    file.write(rendered_content)

path = os.path.abspath('C:/Users/jezar/Downloads/DGTIPOCKET/editar_word/ejem.html')
converter.convert(f'file:///{path}', 'C:/Users/jezar/Downloads/DGTIPOCKET/editar_word/sample.pdf',  print_options={"landscape": True})