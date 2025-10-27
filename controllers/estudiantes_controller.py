from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import get_db_connection
from utils.helpers import login_required

bp = Blueprint('estudiantes_controller', __name__)

@bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    estudiantes = conn.execute('SELECT * FROM estudiantes').fetchall()
    conn.close()
    return render_template('estudiantes/list.html', estudiantes=estudiantes)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']

        conn = get_db_connection()
        conn.execute('INSERT INTO estudiantes (nombre, apellidos, fecha_nacimiento) VALUES (?, ?, ?)',
                    (nombre, apellidos, fecha_nacimiento))
        conn.commit()
        conn.close()

        flash('Estudiante agregado correctamente.')
        return redirect(url_for('estudiantes_controller.index'))

    return render_template('estudiantes/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    conn = get_db_connection()
    estudiante = conn.execute('SELECT * FROM estudiantes WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        fecha_nacimiento = request.form['fecha_nacimiento']

        conn.execute('UPDATE estudiantes SET nombre = ?, apellidos = ?, fecha_nacimiento = ? WHERE id = ?',
                    (nombre, apellidos, fecha_nacimiento, id))
        conn.commit()
        conn.close()

        flash('Estudiante actualizado correctamente.')
        return redirect(url_for('estudiantes_controller.index'))

    conn.close()
    return render_template('estudiantes/edit.html', estudiante=estudiante)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM estudiantes WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('Estudiante eliminado correctamente.')
    return redirect(url_for('estudiantes_controller.index'))