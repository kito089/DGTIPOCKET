from flask import Flask, render_template
import sqlite3



# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Definir una ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sesion')
def sesion():
    return render_template('inicioS.html')

@app.route('/registro')
def registro():
    return render_template('Registro.html')


if __name__ == '__main__':
    app.run(debug=True)
