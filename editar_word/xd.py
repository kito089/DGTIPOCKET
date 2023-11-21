import sys
sys.path.append('C:/Users/jezar/Downloads/DGTIPOCKET/')
from pagina_android.python.pywopd import *


nombre = "JULIO ENRIQUE ZARIÑAN RODDRIGUEZ"

nom = nombre.split(" ")

nombr = []
nombr.append(nom[-2])
nombr.append(nom[-1])
if len(nom) == 4:
    nombr.append(nom[-4])
    nombr.append(nom[-3])
else:
    nombr.append(nom[-3])

datosTC = [["uac","nom","1","2","3","1","2","3"],["uac","nom","1","2","3","1","2","3"],["uac","nom","1","2","3","1","2","3"],["uac","nom","1","2","3","1","2","3"]]
datosE = [["uac","nom","1","2","3","1","2","3"],["uac","nom","1","2","3","1","2","3"]]

datosC = datosTC + datosE
print(datosC)

datosG = ["21301061550046@cetis155.edu.mx","5A","MATUTINO",nombr,"PROGRAMACIÓN"]

boleta(datosC, datosG)