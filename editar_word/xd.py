# import sys
# import numpy as np
# sys.path.append('C:/Users/jezar/Downloads/DGTIPOCKET/')
# from pagina_android.python.pywopd import *
# from pagina_android.python.bd import *
# cambiar procedimientos almacenados para que evalue si es Acreditada y sumarla o si no hacer:

historial = [[1,"matematicas","A"],[2,"español","NP"],[3,"español","NA"],[4,"español","A"],[5,"fisica","NA"],[6,"ingles","A"]]
registro = []

for calificacion in historial:
    materia = calificacion[1]
    aprobada = calificacion[2] == "A"
    
    # Buscamos la materia en el registro
    materia_en_registro = next((elem for elem in registro if elem[0] == materia), None)
    
    # Si la materia está en el registro, actualizamos su estado
    if materia_en_registro:
        materia_en_registro[1] = aprobada
    else:
        # Si la materia no está en el registro, la agregamos
        registro.append([materia, aprobada])

# Contamos las materias aprobadas y reprobadas
materias_aprobadas = sum(1 for elem in registro if elem[1])
materias_reprobadas = len(registro) - materias_aprobadas

print(registro)
print(f"Materias aprobadas: {materias_aprobadas}")
print(f"Materias reprobadas: {materias_reprobadas}")