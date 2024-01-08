# import sys
# sys.path.append('C:/Users/jezar/Downloads/DGTIPOCKET/')
# from pagina_android.python.pywopd import *
# from pagina_android.python.bd import *

# nombre = "JULIO ENRIQUE ZARI�AN RODDRIGUEZ"
# if "�" in nombre:
#     nombre = nombre.replace("�","Ñ")
# nom = nombre.split(" ")

# nombr = []
# nombr.append(nom[-2])
# nombr.append(nom[-1])
# if len(nom) == 4:
#     nombr.append(nom[-4])
#     nombr.append(nom[-3])
# else:
#     nombr.append(nom[-3])

# bd = Coneccion()

# ida = bd.seleccion("alumnos","idalumnos","no_control = 21301061550046")

# tc = bd.llamar("boleta_tc({0})".format(ida[0][0]))
# m = bd.llamar("boleta_m({0})".format(ida[0][0]))
# e = bd.llamar("boleta_e({0})".format(ida[0][0]))

# bd.exit()

# datosG = ["21301061550046@cetis155.edu.mx","5A","MATUTINO",nombr,"PROGRAMACIÓN"]
# datosC = conv(tc,e,m)
# #print(datosC)

# ##########################################################################
# nombre=datosG[3][0]+" "+datosG[3][1]

# controlx = datosG[0].replace("@cetis155.edu.mx","")
# gen = controlx[0]+controlx[1]
# nombr = ""
# for i in range(len(datosG[3])):
#     nombr = nombr +datosG[3][i]+" "

# data = { 
#     '[control]' : str(controlx),
#     '[nombre]' : str(nombr),
#     '[semestre]' : str(datosG[1][0]),
#     '[carre]' : str(datosG[4]),
#     '[turno]' : str(datosG[2]),
#     '[grupo]' : str(datosG[1]),
#     '[gen]' : str("20"+gen+"-"+"20"+str(int(gen)+3)),
#     '[boleta]': str(datosC)
# }
# ##########################################################################

# import subprocess

# def docx2pdf(input, output):
#     command = ['abiword', '--to=pdf', input]

#     try:
#         subprocess.run(command, check=True)
#         print(f'Se ha convertido "{input}" a "{output}" correctamente.')
#     except subprocess.CalledProcessError as e:
#         print(f'Error al convertir el archivo: {e}')

print(len("data:image/jpeg;base64,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"))