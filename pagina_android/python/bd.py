import pymysql 
import numpy as np

class Coneccion:
    def __init__(self):
        try:
            self.conexion = pymysql.connect(  #Se conecta a la base de datos
                host='patotipo.mysql.pythonanywhere-services.com',
                #port=3306,
                user='patotipo',
                password='ZDHY155P',
                db='patotipo$prototipos'
                
                #host='localhost',
                #port=3306,
                #user='root',
                #password='',
                #db='prototipos'
            )
            self.cursor = self.conexion.cursor()
        except pymysql.Error as e:
            print("Error en la conexión: {0}".format(e))

    def obtenerTablas(self, tabla): #Regresa los datos de una tabla
        if self.conexion.open:
            try:
                query = "SELECT * FROM " + tabla
                self.cursor.execute(query)
                tablar = self.cursor.fetchall()
                return tablar
            except pymysql.Error as e:
                print("Error en la conexión: {0}".format(e))

    def insertarRegistro(self, tabla, datos):  #Inserta los registros de una tabla
        if self.conexion.open:
            try:
                atributos = self.obtenerAtributos(tabla)
                print("database")
                print(datos)
                print(atributos)
                print(tabla)
                atr = ""
                dat = " "
                for i in range(1, len(atributos)):
                    atr = atr + str(atributos[i]) + " ,"
                    #print(datos[i-1])
                    if "'" in datos[i-1]:
                        datos[i-1] = datos[i-1].replace("'","´")
                    dat = dat + datos[i - 1] + "' ,'"
                #print(atr)
                query = "INSERT INTO " + tabla + " (" + atr + ") VALUES (" + dat + ")"
                print(query)
                query = query.replace(" ,)", ")")
                query = query.replace(" ,')", ")")
                query = query.replace("( ", "('")
                print(query)
                self.cursor.execute(query)
                self.conexion.commit()
                #print("Datos registrados >:)")
            except pymysql.Error as e:
                print("Error en la conexión: {0}".format(e))

    def eliminarRegistro(self, tabla, pos):  #Elimina un registro de una tabla
        if self.conexion.open:
            try:
                id = self.obtenerAtributos(tabla)
                query = "DELETE FROM " + tabla + " WHERE " + str(id[0]) + " = " + str(pos)
                print(query)
                self.cursor.execute(query)
                self.conexion.commit()
                print("Datos eliminados >w<")
            except pymysql.Error as e:
                print("Error en la conexión: {0}".format(e))

    def eliminarRegistroWhere(self, tabla, wh):  #Elimina un registro de una tabla
        if self.conexion.open:
            try:
                query = "DELETE FROM " + tabla + " WHERE " + str(wh)
                print(query)
                self.cursor.execute(query)
                self.conexion.commit()
                print("Datos eliminados >w<")
            except pymysql.Error as e:
                print("Error en la conexión: {0}".format(e))

    def actualizarRegistro(self, tabla, pos, datos):  #Actualiza el registro de una tabla
        if self.conexion.open:
            try:
                atributos = self.obtenerAtributos(tabla)
                atr = ""
                for i in range(1, len(atributos)):
                    atr = atr + str(atributos[i]) + " = '" + datos[i - 1] + "' ,"
                query = "UPDATE " + tabla + " SET " + atr + "WHERE " + str(atributos[0]) + " = " + str(pos)
                query = query.replace(",W", "W")
                print(query)
                self.cursor.execute(query)
                self.conexion.commit()
                print("Tabla actualizada uwu")
            except pymysql.Error as e:
                print("Error en la conexión: {0}".format(e))

    def actualizarDato(self, tabla, pos, dato, atributo):
        if self.conexion.open:
            try:
                atributos = self.obtenerAtributos(tabla)
                query = "UPDATE "+str(tabla)+" SET "+str(atributo)+" = "+str(dato)+"WHERE "+str(atributos[0])+" = "+str(pos)
                print(query)
                self.cursor.execute(query)
                self.conexion.commit()
                print("Tabla actualizada uwu")
            except pymysql.Error as e:
                print("Error en la conexión: {0}".format(e))

    def obtenerAtributos(self, tabla): #Regresa los atributos de una tabla
        atributos = []
        if self.conexion.open:
            try:
                query = "DESCRIBE " + tabla
                self.cursor.execute(query)
                ejemplo = self.cursor.fetchall()
                y, x = np.shape(ejemplo)
                for i in range(y):
                    atributos.append(ejemplo[i][0])
                return atributos
            except pymysql.Error as e:
                print("Error en la conexión: {0}".format(e))

    def insertarRegistroConID(self, tabla, datos):  #Inserta los registros de una tabla
        if self.conexion.open:
            try:
                atributos = self.obtenerAtributos(tabla)
                atr = ""
                dat = " "
                for i in range(len(atributos)):
                    atr = atr + str(atributos[i]) + " ,"
                    if "'" in datos[i]:
                        datos[i] = datos[i].replace("'","´")
                    dat = dat + datos[i] + "' ,'"
                query = "INSERT INTO " + tabla + " (" + atr + ") VALUES (" + dat + ")"
                print(query)
                query = query.replace(" ,)", ")")
                query = query.replace(" ,')", ")")
                query = query.replace("( ", "('")
                print(query)
                self.cursor.execute(query)
                self.conexion.commit()
                #print("Datos registrados >:)")
            except pymysql.Error as e:
                print("Error en la conexión: {0}".format(e))

    def seleccion(self, tabla, atributo, wh):  #Retorna un select que pida quien lo llame
        if self.conexion.open:
            try:
                query = "SELECT "+atributo+" FROM "+tabla+" WHERE "+wh
                print(query)
                self.cursor.execute(query)
                ejemplo = self.cursor.fetchall()
                if len(ejemplo) == 1 and atributo=="contra":
                    return ejemplo[0][0].encode('utf-8')
                else:
                    return ejemplo
            except pymysql.Error as e:
                print("Error en la conexión: {0}".format(e))

    def exit(self):
        if self.conexion.open:
            try:
                self.cursor.close()
                self.conexion.close()
            except pymysql.Error as e:
                print("Error en la conexión; {0}".format(e))
#### ALTER TABLE (TABLA) AUTO_INCREMENT = 1