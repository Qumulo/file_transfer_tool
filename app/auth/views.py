import errno
import os
from flask import current_app, render_template, redirect, request, url_for, flash, session
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from .forms import LoginForm, RegistrationForm

def create_starting_folder():
    # If the current user has a specified starting folder, tack that on to the path
    starting_folder = session.get("starting_folder")
    save_folder = current_app.config['UPLOADS_FOLDER'] + "/" + starting_folder + "/"

    if not os.path.exists(save_folder):
       try:
           os.makedirs(save_folder)
       except OSError as exc:
           if exc.errno == errno.EEXIST and os.path.isdir(save_folder):
               pass
           else:
               raise

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(None):
            login_user(user, form.remember_me.data)

            if user.starting_folder is not None:
                session["starting_folder"] = user.starting_folder
                # ensure the user's starting_folder exists
                create_starting_folder()

            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()

    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        starting_folder = request.args.get('starting_folder')
        user = User(email=form.email.data, username=form.email.data, starting_folder=starting_folder)
        db.session.add(user)
        flash('You can now login.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)
