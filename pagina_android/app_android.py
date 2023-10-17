from flask import Flask, render_template,redirect,url_for, request
import pymysql


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prototipos'

# Crear una conexión a la base de datos
db = pymysql.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    db=app.config['MYSQL_DB']
)




# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Definir una ruta para la página principal
@app.route('/')
def index():
    return render_template('indexapp.html')

@app.route('/sesion')
def sesion():
    return render_template('inicioSapp.html')

@app.route('/registro')
def registro():
    return render_template('Registroapp.html')
@app.route('/planteles')
def planteles():
    return render_template('plantelesapp.html')

@app.route('/tutorias')
def tutorias():
    return render_template('tutoriasapp.html')



@app.route('/funciones')
def funciones():
    return render_template('funcionesapp.html')
@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/noticias')
def noticias():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM noticias")
    noticias = cursor.fetchall()
    return render_template('noticiasapp.html', noticias=noticias)

@app.route('/insnot', methods=['GET', 'POST'])
def agregar_noticia():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        img = request.form['img']
        fecha = request.form['fecha']

        cursor  = db.cursor()
        cursor.execute("INSERT INTO noticias (titulo, descripcion, img, fecha) VALUES (%s, %s, %s, %s)",
                       (titulo, descripcion, img, fecha))
        db.commit()
        

        return redirect(url_for('noticias'))
    return render_template('insnot.html')



if __name__ == '__main__':
    app.run(debug=True)
