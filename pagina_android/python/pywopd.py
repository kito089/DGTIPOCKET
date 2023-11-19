from docxtpl import DocxTemplate
from docx2pdf import convert

def boleta(datosC, datosG):
    doc = DocxTemplate('C:/Users/jezar/Downloads/DGTIPOCKET/editar_word/plantilla_boleta_mamalona.docx')
    #doc = DocxTemplate('C:/Users/jezar/Downloads/reportTmpl.docx')

    nombre=datosG[3][0]+" "+datosG[3][1]

    control = datosG[0].replace("@cetis155.edu.mx","")
    gen = control[0]+control[1]
    nombr = ""
    for i in range(len(datosG[3])):
        nombr = nombr +datosG[3][i]+" "
    
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
    doc.save("C:/Users/jezar/Downloads/DGTIPOCKET/editar_word/"+nombre+'.docx')

def word2pdf(dir):
    inputFile = dir+'.docx'
    outputFile = dir+'.pdf'

    convert(inputFile, outputFile)