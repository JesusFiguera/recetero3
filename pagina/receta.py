import functools
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)

from werkzeug.security import check_password_hash, generate_password_hash

from pagina.auth import login_required
from pagina.db import get_db

bp = Blueprint('receta',__name__,)

@bp.route('/')
def inicio():
    db,c = get_db()
    c.execute(
        'select r.ingredientes from receta r'
    )
    ingredientes = c.fetchall()
    rows = 0
    rows_list = []
    linea = 0
    for i in range(len(ingredientes)):
        for j in ingredientes[i]['ingredientes']:
            if j == '\n':
                rows+=1
        rows_list.append(rows)
        rows = 0
            
    c.execute(
        'select * from receta'
    )
    receta = c.fetchall()
    size = len(receta)
    return render_template('inicio.html',receta=receta,rows=rows_list,size=size)

@bp.route('/create',methods=['POST','GET'])
@login_required
def create():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        ingredientes = request.form['ingredientes']
        preparacion = request.form['preparacion']
        categoria = request.form['categoria']
        url = request.form['url']
        db ,c = get_db()
        c.execute(
            'insert into receta (titulo,descripcion,ingredientes,preparacion,categoria,url) values (%s,%s,%s,%s,%s,%s)',
            (titulo,descripcion,ingredientes,preparacion,categoria,url)
        )
        db.commit()
        return redirect(url_for('receta.index_adm'))
    return render_template('recetas/create.html')


@bp.route('/index')
@login_required
def index():
    db,c = get_db()
    c.execute(
        'select r.ingredientes from receta r'
    )
    ingredientes = c.fetchall()
    rows = 0
    rows_list = []
    linea = 0
    for i in range(len(ingredientes)):
        for j in ingredientes[i]['ingredientes']:
            if j == '\n':
                rows+=1
        rows_list.append(rows)
        rows = 0
    c.execute(
        'select * from receta'
    )
    receta = c.fetchall()
    size = len(receta)
    return render_template('recetas/index.html',receta=receta,rows=rows_list,size=size)


@bp.route('/index_adm')
@login_required
def index_adm():
    db,c = get_db()
    c.execute(
        'select r.ingredientes from receta r'
    )
    ingredientes = c.fetchall()
    rows = 0
    rows_list = []
    linea = 0
    for i in range(len(ingredientes)):
        for j in ingredientes[i]['ingredientes']:
            linea+=1
            if j == '\n':
                rows+=1
            if linea >= 30:
                rows+=1
                linea = 0
        rows_list.append(rows)
        rows = 0
    c.execute(
        'select * from receta'
    )
    receta = c.fetchall()
    size = len(receta)
    return render_template('recetas/index_adm.html',receta=receta,rows=rows_list,size=size)

@bp.route('/recipe')
def recipe():
    db,c = get_db()
    c.execute(
        'select * from receta'
    )
    receta = c.fetchall()
    return render_template('recetas/recipe.html',receta=receta)


@bp.route('/recipe_adm')
@login_required
def recipe_adm():
    db,c = get_db()
    c.execute(
        'select * from receta'
    )
    receta = c.fetchall()
    return render_template('recetas/recipe_adm.html',receta=receta)


@bp.route('/recipe_user')
@login_required
def recipe_user():
    db,c = get_db()
    c.execute(
        'select * from receta'
    )
    receta = c.fetchall()
    return render_template('recetas/recipe_user.html',receta=receta)

def get_recipe(id):
    db, c= get_db()
    c.execute(
        'select * from receta where id = %s',(id,)
    )
    receta = c.fetchone()

    if receta is None:
        abort(404, "El todo de id {0} no existe".format(id))
    return receta
@bp.route('/<int:id>/mostrar')
def mostrar(id):
    receta = get_recipe(id)
    rows = 0
    for i in receta['ingredientes']:
        if i == '\n':
            rows+=1
    return render_template('recetas/mostrar.html',receta=receta,rows=rows)

@bp.route('/<int:id>/mostrar_adm')
@login_required
def mostrar_adm(id):
    receta = get_recipe(id)
    rows = 0
    for i in receta['ingredientes']:
        if i == '\n':
            rows+=1
    return render_template('recetas/mostrar_adm.html',receta=receta,rows=rows)



@bp.route('/<int:id>/mostrar_user')
@login_required
def mostrar_user(id):
    receta = get_recipe(id)
    rows = 0
    for i in receta['ingredientes']:
        if i == '\n':
            rows+=1
    return render_template('recetas/mostrar_user.html',receta=receta,rows=rows)


@bp.route('/categorias')
def categorias():
    db,c = get_db()
    c.execute(
        'select * from receta'
    )
    receta = c.fetchall()
    return render_template('recetas/categorias.html',receta=receta)

@bp.route('/<categoria>/mostrar_categoria')
def mostrar_categoria(categoria):
    db,c = get_db()
    c.execute(
        'select r.ingredientes from receta r where categoria = %s',(categoria,)
    )
    ingredientes = c.fetchall()
    rows = 0
    rows_list = []
    linea = 0
    for i in range(len(ingredientes)):
        for j in ingredientes[i]['ingredientes']:
            if j == '\n':
                rows+=1
        rows_list.append(rows)
        rows = 0
    c.execute(
        'select * from receta where categoria = %s',(categoria,)
    )
    receta = c.fetchall()
    size = len(receta)
    return render_template('recetas/mostrar_categoria.html',receta=receta,rows=rows_list,size=size)


@bp.route('/categorias_adm')
@login_required
def categorias_adm():
    return render_template('recetas/categorias_adm.html')


@bp.route('/<categoria>/mostrar_categoria_adm')
@login_required
def mostrar_categoria_adm(categoria):
    db,c = get_db()
    c.execute(
        'select r.ingredientes from receta r where categoria = %s',(categoria,)
    )
    ingredientes = c.fetchall()
    rows = 0
    rows_list = []
    linea = 0
    for i in range(len(ingredientes)):
        for j in ingredientes[i]['ingredientes']:
            if j == '\n':
                rows+=1
        rows_list.append(rows)
        rows = 0
    c.execute(
        'select * from receta where categoria = %s',(categoria,)
    )
    receta = c.fetchall()
    size = len(receta)
    return render_template('recetas/mostrar_categoria_adm.html',receta=receta,rows=rows_list,size=size)



@bp.route('/categorias_user')
@login_required
def categorias_user():
    return render_template('recetas/categorias_user.html')

@bp.route('/<categoria>/mostrar_categoria_user')
@login_required
def mostrar_categoria_user(categoria):
    db,c = get_db()
    c.execute(
        'select r.ingredientes from receta r where categoria = %s',(categoria,)
    )
    ingredientes = c.fetchall()
    rows = 0
    rows_list = []
    linea = 0
    for i in range(len(ingredientes)):
        for j in ingredientes[i]['ingredientes']:
            if j == '\n':
                rows+=1
        rows_list.append(rows)
        rows = 0
    c.execute(
        'select * from receta where categoria = %s',(categoria,)
    )
    receta = c.fetchall()
    size = len(receta)
    return render_template('recetas/mostrar_categoria_user.html',receta=receta,rows=rows_list,size=size)
