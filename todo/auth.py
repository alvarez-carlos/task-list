import functools
from flask import (
           Blueprint,
           flash, 
           g,
           render_template,
           request, 
           url_for,
           session,
           redirect
        )

from  werkzeug.security import check_password_hash, generate_password_hash

from todo.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

#register route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      db, c = get_db()
      error = None
      c.execute(
              'select id from user where username = %s', (username,)
              )
      if not username:
          error = 'Username is required'
      if not password:
          error = 'Password is required'
      elif c.fetchone() is not None:
          error = 'The user {} alreay exists'.format(username)
      if error is None:
          c.execute(
                  'insert into user (username, password) values (%s, %s)',
                  (username, generate_password_hash(password))
                  )
          db.commit()
          return redirect(url_for('auth.login'))
      flash(error)
    return render_template('auth/register.html') 


#login route
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
                'select * from user where username = %s', (username,)
                )
        user = c.fetchone()

        if user is None:
            error = 'User and/or Password Incorrect'
        elif not check_password_hash(user['password'], password):
            error = 'User and/or Password Incorrect'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
                'select * from user where id=%s', (user_id,)
                )
        g.user = c.fetchone()
        

#Protegiendo nuestras rutas
#utilizamos una funcion la cual es una funcion que recibe como argumento la misma funcion que nosotros estamos decorando
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for(auth.login))
        return view(**kwargs)
    return wrapped_view

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
    

       




