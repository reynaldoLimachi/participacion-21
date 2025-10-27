from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import get_db_connection
from utils.helpers import login_required

bp = Blueprint('inscripcion_controller', __name__)

@bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    inscripciones = conn.execute('''
        SELECT i.id, i.fecha, e.nombre, e.apellidos, c.descripcion
        FROM inscripcion i
        JOIN estudiantes e ON i.estudiante_id = e.id
        JOIN cursos c ON i.curso_id = c.id
    ''').fetchall()
    conn.close()
    return render_template('inscripcion/list.html', inscripciones=inscripciones)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    conn = get_db_connection()
    estudiantes = conn.execute('SELECT * FROM estudiantes').fetchall()
    cursos = conn.execute('SELECT * FROM cursos').fetchall()

    if request.method == 'POST':
        fecha = request.form['fecha']
        estudiante_id = request.form['estudiante_id']
        curso_id = request.form['curso_id']

        conn.execute('INSERT INTO inscripcion (fecha, estudiante_id, curso_id) VALUES (?, ?, ?)',
                    (fecha, estudiante_id, curso_id))
        conn.commit()
        conn.close()

        flash('Inscripción agregada correctamente.')
        return redirect(url_for('inscripcion_controller.index'))

    conn.close()
    return render_template('inscripcion/add.html', estudiantes=estudiantes, cursos=cursos)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    conn = get_db_connection()
    inscripcion = conn.execute('SELECT * FROM inscripcion WHERE id = ?', (id,)).fetchone()
    if not inscripcion:
        conn.close()
        flash('Inscripción no encontrada.')
        return redirect(url_for('inscripcion_controller.index'))

    estudiantes = conn.execute('SELECT * FROM estudiantes').fetchall()
    cursos = conn.execute('SELECT * FROM cursos').fetchall()

    if request.method == 'POST':
        fecha = request.form['fecha']
        estudiante_id = request.form['estudiante_id']
        curso_id = request.form['curso_id']

        conn.execute('''
            UPDATE inscripcion
            SET fecha = ?, estudiante_id = ?, curso_id = ?
            WHERE id = ?
        ''', (fecha, estudiante_id, curso_id, id))
        conn.commit()
        conn.close()

        flash('Inscripción actualizada correctamente.')
        return redirect(url_for('inscripcion_controller.index'))

    conn.close()
    return render_template(
        'inscripcion/edit.html',
        inscripcion=inscripcion,
        estudiantes=estudiantes,
        cursos=cursos
    )

@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM inscripcion WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Inscripción eliminada correctamente.')
    return redirect(url_for('inscripcion_controller.index'))