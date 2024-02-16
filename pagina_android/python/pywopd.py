from docxtpl import DocxTemplate
from decimal import Decimal
from docx import Document
import os
import subprocess
from datetime import datetime

def fecha_actual():
    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Definir los nombres de los meses en español
    meses = [
        "ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO",
        "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"
    ]

    # Obtener los componentes de la fecha
    dia = fecha_actual.day
    mes = meses[fecha_actual.month - 1]  # Restamos 1 porque los índices de la lista comienzan en 0
    año = fecha_actual.year

    # Imprimir la fecha en el formato deseado
    return f"A LOS {dia} DIAS DEL MES DE {mes} DEL AÑO DOS MIL {str(año)[2:]}"

def conv(tc,e,m):
    tcl = [list(tupla) for tupla in tc]
    ml = [list(tupla) for tupla in m]
    el = [list(tupla) for tupla in e]

    tcl2 = []
    el2 = []

    for i in range(len(tcl)):
        for j in range(len(tcl[i])):
            if tcl[i][j] is None:
                tcl[i][j] = ""
    for i in range(len(ml)):
        for j in range(len(ml[i])):
            if ml[i][j] is None:
                ml[i][j] = ""
    for i in range(len(el)):
        for j in range(len(el[i])):
            if el[i][j] is None:
                el[i][j] = ""

    for t1 in tcl:
        tcl2.append([])
        for t in t1:
            if isinstance(t, str):
                tcl2[-1].append(t)
            else:
                if t.is_integer():
                    tcl2[-1].append(int(t))
                else:
                    tcl2[-1].append(format(float(t), '.1f'))

    for e1 in el:
        el2.append([])
        for e in e1:
            if isinstance(e, str):
                el2[-1].append(e)
            else:
                if e.is_integer():
                    el2[-1].append(int(e))
                else:
                    el2[-1].append(format(float(e), '.1f'))

    #tcl = [[int(elemento) if isinstance(elemento, (int, float)) else format(float(elemento), '.1f') if isinstance(elemento, Decimal) else elemento for elemento in sublista] for sublista in tcl]
    #el = [[int(elemento) if isinstance(elemento, (int, float)) else format(float(elemento), '.1f') if isinstance(elemento, Decimal) else elemento for elemento in sublista] for sublista in el]

    datosC = tcl2+ml+el2
    return datosC

def genHAdocx(datosC, datosG, avances):
    doc = DocxTemplate(os.path.expanduser('~/DGTIPOCKET/editar_word/plantilla_HA_mamalon.docx'))

    control = datosG[0].replace("@cetis155.edu.mx","")

    ava = avances
    if int(control[1]) > 1:
        avances.append("404","12",p,p,p,"44",p)
    else:
        avances.append("340","20",p,p,p,"31",p)
    context = { 
        'curp' : datosG[1],
        'control' : control,
        'nombre' : datosG[3],
        'carrera': datosG[2],
        'fecha': fecha_actual(),
        'a': avances,
        'ha': datosC
    }
        
    doc.render(context)
    doc.save(os.path.expanduser('~/DGTIPOCKET/editar_word/'+datosG[3].replace(" ","_")+'.docx'))

def genboletadocx(datosC, datosG):
    doc = DocxTemplate(os.path.expanduser('~/DGTIPOCKET/editar_word/plantilla_boleta_mamalona.docx'))

    nombre=datosG[3][0]+" "+datosG[3][1]

    control = datosG[0].replace("@cetis155.edu.mx","")
    gen = control[0]+control[1]
    nombr = ""
    for i in range(len(datosG[3])):
        nombr = nombr +datosG[3][i]+" "
    
    print("datos c: ", datosC)

    context = { 
        'control' : control,
        'nombre' : nombr,
        'semestre' : datosG[1][0],
        'carre' : datosG[4],
        'turno' : datosG[2],
        'grupo' : datosG[1],
        'gen' : "20"+gen+"-"+"20"+str(int(gen)+3),
        'boleta': datosC
    }
        
    doc.render(context)
    print(nombre)
    doc.save(os.path.expanduser('~/DGTIPOCKET/editar_word/'+nombre.replace(" ","_")+'.docx'))

def docx2pdf(input):
    command = ['abiword', '--to=pdf', input]

    try:
        subprocess.run(command, check=True)
        os.remove(input)
        print(f'Se ha convertido correctamente.')
    except subprocess.CalledProcessError as e:
        print(f'Error al convertir el archivo: {e}')