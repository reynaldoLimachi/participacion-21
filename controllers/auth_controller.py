from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.database import get_db_connection
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

bp = Blueprint('auth_controller', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contraseña = request.form['contraseña']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM usuarios WHERE usuario = ?', (usuario,)).fetchone()
        conn.close()

        if user and check_password_hash(user['contraseña'], contraseña):
            session['user_id'] = user['id']
            session['usuario'] = user['usuario']
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('dashboard_controller.index'))
        else:
            flash('Credenciales incorrectas.')

    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        usuario = request.form['usuario']
        correo = request.form['correo']
        celular = request.form['celular']
        contraseña = request.form['contraseña']
        confirmar = request.form['confirmar']

        if contraseña != confirmar:
            flash('Las contraseñas no coinciden.')
            return render_template('auth/register.html')

        conn = get_db_connection()
        try:
            hashed = generate_password_hash(contraseña)
            conn.execute('''
                INSERT INTO usuarios (usuario, correo, celular, contraseña)
                VALUES (?, ?, ?, ?)
            ''', (usuario, correo, celular, hashed))
            conn.commit()
            flash('Usuario registrado correctamente.')
            return redirect(url_for('auth_controller.login'))
        except sqlite3.IntegrityError:
            flash('Usuario o correo ya registrado.')
        finally:
            conn.close()

    return render_template('auth/register.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.')
    return redirect(url_for('auth_controller.login'))