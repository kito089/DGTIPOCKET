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
print(ida)

tc = bd.llamar("boleta_tc({0})".format(ida[0][0]))
m = bd.llamar("boleta_m({0})".format(ida[0][0]))
e = bd.llamar("boleta_e({0})".format(ida[0][0]))

bd.exit()

datosG = ["21301061550046@cetis155.edu.mx","5A","MATUTINO",nombr,"PROGRAMACIÓN"]
datosC = conv(tc,e,m)

boleta(datosC, datosG)
