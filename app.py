from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'

class NombreForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def home():
    form = NombreForm()
    if form.validate_on_submit():
        return redirect(url_for('usuario', nombre=form.nombre.data))
    return render_template('index.html', form=form)

@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f'Bienvenido, {nombre}!'

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
