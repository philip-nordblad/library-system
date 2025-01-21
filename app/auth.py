import functools

from flask import (Blueprint, flash, g, redirect, render_template,request,session,url_for)

from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager

from flask_wtf import FlaskForm
from .models import User
from .forms import RegistrationForm, LoginForm
from flask_login import login_required, login_user




bp = Blueprint('auth',__name__,url_prefix='/auth')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@bp.route('/register', methods=['GET','POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        print("Form Data",request.form)


        username = form.username.data
        password = form.password.data
        role = form.role.data
        

        error = None


        if User.query.filter_by(username=username).first() is not None:
            error = f'User {username} is already registered'

        if error is None:
            new_user = User(username=username,password=generate_password_hash(password,method="pbkdf2:sha256"), role=role)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods = ["GET","POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        print("Data Form: ", request.form)

        username = form.username.data
        password = form.password.data
        error = None

        user = User.query.filter_by(username=username).first()
        print(f"Hashed password from DB: {user.password}")
        print(f"Password input: {password}")
        if user is None:
            error = "Incorrect Username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            login_user(user)
            return redirect(url_for('index'))


        flash(error)
    
    return render_template('auth/login.html',form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    redirect(url_for('login'))



            

