from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import get_db_connection
from utils.helpers import login_required

bp = Blueprint('cursos_controller', __name__)

@bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    cursos = conn.execute('SELECT * FROM cursos').fetchall()
    conn.close()
    return render_template('cursos/list.html', cursos=cursos)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        horas = request.form['horas']

        conn = get_db_connection()
        conn.execute('INSERT INTO cursos (descripcion, horas) VALUES (?, ?)',
                    (descripcion, horas))
        conn.commit()
        conn.close()

        flash('Curso agregado correctamente.')
        return redirect(url_for('cursos_controller.index'))

    return render_template('cursos/add.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    conn = get_db_connection()
    curso = conn.execute('SELECT * FROM cursos WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        horas = request.form['horas']

        conn.execute('UPDATE cursos SET descripcion = ?, horas = ? WHERE id = ?',
                    (descripcion, horas, id))
        conn.commit()
        conn.close()

        flash('Curso actualizado correctamente.')
        return redirect(url_for('cursos_controller.index'))

    conn.close()
    return render_template('cursos/edit.html', curso=curso)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM cursos WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    flash('Curso eliminado correctamente.')
    return redirect(url_for('cursos_controller.index'))