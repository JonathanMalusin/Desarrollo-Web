from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import os
import json
import csv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'

# Archivos para persistencia
TXT_FILE = 'datos/datos.txt'
JSON_FILE = 'datos/datos.json'
CSV_FILE = 'datos/datos.csv'

# Crear archivos si no existen
if not os.path.exists('datos'):
    os.makedirs('datos')

# Configuración de SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Definición del modelo de la base de datos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'


# Crear la base de datos si no existe
with app.app_context():
    db.create_all()


# Función para guardar datos en un archivo TXT
def guardar_en_txt(nombre):
    with open(TXT_FILE, 'a', encoding='utf-8') as f:
        f.write(f'{nombre}\n')


# Función para guardar datos en un archivo JSON
def guardar_en_json(nombre):
    data = []
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    data.append(nombre)
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Función para guardar datos en un archivo CSV
def guardar_en_csv(nombre):
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([nombre])


# Función para guardar datos en SQLite
def guardar_en_sqlite(nombre):
    nuevo_usuario = Usuario(nombre=nombre)
    db.session.add(nuevo_usuario)
    db.session.commit()


# Ruta principal
class NombreForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = NombreForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        guardar_en_txt(nombre)  # Guarda el nombre en TXT
        guardar_en_json(nombre)  # Guarda el nombre en JSON
        guardar_en_csv(nombre)  # Guarda el nombre en CSV
        guardar_en_sqlite(nombre)  # Guarda el nombre en SQLite
        return redirect(url_for('usuario', nombre=nombre))
    return render_template('index.html', form=form)


@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'


@app.route('/about')
def about():
    return render_template('about.html')


# Ruta para leer el archivo TXT
@app.route('/leer_txt')
def leer_txt():
    if not os.path.exists(TXT_FILE):
        return "No hay datos almacenados en TXT aún."

    with open(TXT_FILE, 'r', encoding='utf-8') as f:
        datos = f.readlines()

    if not datos:
        return "El archivo TXT está vacío."

    return "<br>".join([dato.strip() for dato in datos])


# Ruta para leer el archivo JSON
@app.route('/leer_json')
def leer_json():
    if not os.path.exists(JSON_FILE):
        return "No hay datos almacenados en JSON aún."

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        datos = json.load(f)

    if not datos:
        return "El archivo JSON está vacío."

    return "<br>".join(datos)


# Ruta para leer el archivo CSV
@app.route('/leer_csv')
def leer_csv():
    if not os.path.exists(CSV_FILE):
        return "No hay datos almacenados en CSV aún."

    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datos = [row[0] for row in reader]

    if not datos:
        return "El archivo CSV está vacío."

    return "<br>".join(datos)


# Ruta para leer los datos almacenados en SQLite
@app.route('/leer_sqlite')
def leer_sqlite():
    usuarios = Usuario.query.all()  # Obtener todos los usuarios de la base de datos
    if not usuarios:
        return "No hay datos almacenados en la base de datos SQLite aún."

    return "<br>".join([usuario.nombre for usuario in usuarios])


if __name__ == '__main__':
    app.run(debug=True)
