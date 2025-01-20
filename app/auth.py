import functools

from flask import (Blueprint, flash, g, redirect, render_template,request,session,url_for)

from werkzeug.security import check_password_hash, generate_password_hash

from . import db





bp = Blueprint('auth',__name__,url_prefix='/auth')


@bp.route('/register', methods=['GET','POST'])
def register():
    
    if request.method == 'POST':


        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        

        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        
        if error is None:

            try:
                new_user = User(username=username,password=generate_password_hash(password, method="pbkdf2:sha256"),role=role)
                db.session.add(user)
                db.session.commit()

            except db.IntegrityError:
                error = f"User {user.username} is already registered."
            else:
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods = ["GET","POST"])
def login():

    if request.method = 'POST':

        username = request.form['username']
        password = request.form['password']

        error = None

        user = User.query.filter_by(username=username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password,password):
            error = "Incorrect password."

        if error is None:
            login_user(user)
            return redirect(url_for('index'))

        flash(error)
    
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
            

