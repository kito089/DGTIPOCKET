import sys
import numpy as np
sys.path.append('C:/Users/jezar/Downloads/DGTIPOCKET/')
from pagina_android.python.pywopd import *
from pagina_android.python.bd import *

bd = Coneccion()
atr = bd.obtenerAtributos("modulos")
datos = bd.obtenerTablas("modulos")

tab2 = ""
datre = []

if "_id" in atr[-1]:
    for a in atr[-1]:
        if a != "_":
            tab2 += a
        else:
            break

    atr.pop(-1)
    atr.append(tab2)

    for dato in datos:
        dato.append(bd.seleccion(tab2, "nombre", "id"+str(tab2)+"="+str(dato[-1]))[0][0])
        dato.pop(-2)

print(datos)
bd.exit()