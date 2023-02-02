from flask import Flask, render_template, request, send_file, jsonify, url_for, redirect, flash, session
from psycopg2 import connect, extras
import os
from cryptography.fernet import Fernet
from wtforms import StringField, PasswordField, SubmitField
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_sqlalchemy import SQLAlchemy

import hashlib


app = Flask(__name__)
key = Fernet.generate_key()
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] =  'MOAA'

host = 'localhost'
port = 5432
dbname = 'MOOA'
user = 'postgres'
password = 'Campos0430'

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# class User(dbname.Model, UserMixin):
#     id = dbname.Column(dbname.Integer, primary_key=True)
#     username = dbname.Column(dbname.String(20), nullable=False, unique=True)
#     password = dbname.Column(dbname.String(80), nullable=False)

def get_connection():
    conn = connect(host=host, port=port, dbname=dbname,
                        user=user, password=password)
    return conn


@app.route('/')
def index():
    # return "<h1>Hola mundo</h1>"

    return render_template("index.html")

# Productos

@app.route('/hombre')
def hombre():
    return render_template("hombre.html")


@app.route('/mujer')
def mujer():
    return render_template("mujer.html")


@app.route('/niño')
def niño():
    return render_template("kid.html")
# Fin de Productos
#Carrito

@app.route('/carrito')
def carrito():
    return render_template("carrito.html")


@app.route('/servicios')
def servicios():
    return render_template('servicio.html')


@app.route('/conocenos')
def conocenos():
    return render_template('conocenos.html')


@app.route('/lcatalogo')
def lcatalogo():

    return render_template('lcatalogo.html')


@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')


@app.route('/register')
def register():

    return render_template('register.html')

#Crud Comentario

@app.get('/api/comment')
def get_comment():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM comment')
    users = cur.fetchall()

    cur.close()
    conn.close()
    return jsonify(users)


@app.post('/api/comment')
def create_comment():
    new_comment = request.get_json()
    username = new_comment['username']
    email = new_comment['email']
    pregunta = new_comment['pregunta']

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('INSERT INTO comment (username, email, pregunta) VALUES (%s, %s, %s) RETURNING *',
                (username, email, pregunta))
    new_created_comment = cur.fetchone()
    print(new_created_comment)
    conn.commit()

    cur.close()
    conn.close()

    return jsonify(new_created_comment)


@app.delete('/api/comment/<id>')
def delete_comentarios(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("DELETE FROM comment WHERE id = %s RETURNING *", (id,))
    user = cur.fetchone()

    conn.commit()

    conn.close()
    cur.close()

    if user is None:
        return jsonify({'message': 'User Not Found'}, 404)

    return jsonify(user)


@app.put('/api/comment/<id>')
def update_comment(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    new_comment = request.get_json()
    username = new_comment['username']
    email = new_comment['email']
    pregunta = new_comment['pregunta']

    cur.execute(
        'UPDATE comment SET username = %s, email = %s, pregunta = %s WHERE id = %s RETURNING *', (username, email, pregunta, id))
    update_comment = cur.fetchone()
    
    conn.commit()
    
    conn.close()
    cur.close()
    
    if update_comment is None:
        return jsonify({'message': 'User Not Found'}, 404)

    return jsonify(update_comment)


@app.get('/api/comment/<id>')
def get_comments(id):

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute('SELECT * FROM comment WHERE id = %s', (id,))
    user = cur.fetchone()

    if user is None:
        return jsonify({'message': 'User Not Found'}), 404

    print(user)

    return jsonify(user)

@app.get('/comentarios')
def comentarios():
    return render_template('comentarios.html')

# fin crud commentarios


# @app.route('/login/', methods=['GET', 'POST'])
# def login():
#     return render_template('login.html')

@app.route('/contactanos')
def contactanos():
    return render_template('contactanos.html')


@app.route('/dashboard')
def dashboard():
    # Verificación de variable de sesión
    if 'id' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html')


@app.get('/api/users')
def get_users():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    cur.close()
    return jsonify(users)


@app.post('/api/users')
def create_users():
    new_user = request.get_json()
    username = new_user['username']
    lastname = new_user['lastname']
    datebirth = new_user['datebirth']
    phone = new_user['phone']
    addres = new_user['addres']
    email = new_user['email']
    #password = Fernet(key).encrypt(bytes(new_user['password'], 'utf-8'))
    password_hash = hashlib.md5(new_user['password'].encode())
    password=password_hash.hexdigest()
    

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('INSERT INTO users (username, lastname, datebirth, phone, addres, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *',
                (username, lastname, datebirth, phone, addres, email, password))

    new_created_user = cur.fetchone()
    print(new_created_user)
    conn.commit()
    cur.close()
    conn.close()

    return jsonify(new_created_user)


@app.delete('/api/users/<id>')
def delete_users(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute(' DELETE FROM users WHERE id = %s RETURNING *', (id))
    user = cur.fetchone()
    conn.commit()
    conn.close()
    cur.close()

    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user)


@app.put('/api/users/<id>')
def update_users(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = new_user['password']

    cur.execute(' UPDATE users SET  username = %s, email = %s, password = %s WHERE id = %s RETURNING *',
                (username, email, password, id))
    update_user = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()
    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(update_user)


@app.get('/api/users/<id>')
def get_user(id):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM users WHERE id = %s', (id,))
    user = cur.fetchone()

    if user is None:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user)


class LoginForm(FlaskForm):
    username = StringField(validators=[
            InputRequired(), Length(min=4, max=222)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
            InputRequired(), Length(min=8, max=222)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    form = LoginForm()
    if form.validate_on_submit():
        cur.execute('SELECT * FROM users WHERE username = %s', (form.username.data,))
        user = cur.fetchone()
        print(user)
        if user:
            for_password_hash = hashlib.md5(form.password.data.encode())
            print(for_password_hash.hexdigest())
            print(user['password'])
            if user['password'] == for_password_hash.hexdigest():
                # Guardamos el id del usuario en session
                session['id']= user['id']
                # En el logout se debería eliminar la variable de sesión session.pop('username', None)
                
                password_hash = hashlib.md5(form.password.data.encode())
                
                # print(f"variable de sesión almacenada {session['id']}, password hashed {password_hash.hexdigest()}")
                return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

if __name__ == '__main__':

    app.run(debug=True, port=5000)
