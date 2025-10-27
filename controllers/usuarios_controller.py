from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import get_db_connection
from utils.helpers import login_required
from werkzeug.security import generate_password_hash
import sqlite3

bp = Blueprint('usuarios_controller', __name__)

@bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('usuarios/list.html', usuarios=usuarios)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        usuario = request.form['usuario']
        correo = request.form['correo']
        celular = request.form['celular']
        contraseña = request.form['contraseña']
        confirmar = request.form['confirmar']

        if contraseña != confirmar:
            flash('Las contraseñas no coinciden.')
            return render_template('usuarios/add.html')

        conn = get_db_connection()
        try:
            hashed = generate_password_hash(contraseña)
            conn.execute('''
                INSERT INTO usuarios (usuario, correo, celular, contraseña)
                VALUES (?, ?, ?, ?)
            ''', (usuario, correo, celular, hashed))
            conn.commit()
            flash('Usuario agregado correctamente.')
            return redirect(url_for('usuarios_controller.index'))
        except sqlite3.IntegrityError:
            flash('Usuario o correo ya registrado.')
        finally:
            conn.close()

    return render_template('usuarios/add.html')