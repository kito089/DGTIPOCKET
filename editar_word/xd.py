import sys
sys.path.append('C:/Users/jezar/Downloads/DGTIPOCKET/')
from pagina_android.python.pywopd import *
from pagina_android.python.bd import *

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
#print(datosC)

##########################################################################
nombre=datosG[3][0]+" "+datosG[3][1]

controlx = datosG[0].replace("@cetis155.edu.mx","")
gen = controlx[0]+controlx[1]
nombr = ""
for i in range(len(datosG[3])):
    nombr = nombr +datosG[3][i]+" "

data = { 
    '[control]' : str(controlx),
    '[nombre]' : str(nombr),
    '[semestre]' : str(datosG[1][0]),
    '[carre]' : str(datosG[4]),
    '[turno]' : str(datosG[2]),
    '[grupo]' : str(datosG[1]),
    '[gen]' : str("20"+gen+"-"+"20"+str(int(gen)+3)),
    '[boleta]': str(datosC)
}
##########################################################################

import subprocess

def docx2pdf(input, output):
    command = ['abiword', '--to=pdf', input]

    try:
        subprocess.run(command, check=True)
        print(f'Se ha convertido "{input}" a "{output}" correctamente.')
    except subprocess.CalledProcessError as e:
        print(f'Error al convertir el archivo: {e}')
