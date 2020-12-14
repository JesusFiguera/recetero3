import functools
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)

from werkzeug.security import check_password_hash, generate_password_hash

from pagina.db import get_db

bp = Blueprint('auth',__name__,url_prefix='/auth')

@bp.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        sexo = request  .form['sexo']
        db, c = get_db()
        error = None
        c.execute(
            'select * from user where username = %s',(username,)
        )
        if not username:
            error = 'Username requerido'
        if not password:
            error = 'Password es requerido'
        elif c.fetchone() is not None:
            error = 'El usuario ya se encuentra registrado'

        if error is None:
            c.execute(
                'insert into user (username,password,nombre,apellido,correo,permisos,sexo) values (%s,%s,%s,%s,%s,%s,%s)',
                (username,generate_password_hash(password),nombre,apellido,email,0,sexo)
            )
            db.commit()
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@bp.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db,c = get_db()
        error = None
        c.execute(
            'select * from user where username = %s',(username,)
        )
        user = c.fetchone()
        if user is None:
            error = 'El usuario no existe'
        elif not check_password_hash(user['password'],password):
            error = 'El usuario no existe'
        if error is  None and user['permisos'] == 1:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('receta.index_adm'))
        if error is None and user['permisos'] == 0:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('receta.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))



@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'select * from user where id = %s', (user_id,)
        )
        g.user = c.fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view