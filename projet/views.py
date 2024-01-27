from flask import Flask, render_template, request, session, flash, redirect, url_for
from . import auth, business
from .auth import login_required
from .db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from .services import UserService, league_service

app = Flask(__name__)
bp_auth = auth.bp
bp_business = business.bp


@bp_business.route('/')
@login_required
def index():
    """ Root route"""
    return render_template('index.html')


@bp_business.route('/league')
@login_required
def league():
    """ league page route"""
    return render_template('league.html')


@app.route('/new_match')
def new_match():
    """ new match route """
    return render_template('new_match.html')


@bp_business.route('/new_league', methods=('GET', 'POST'))
@login_required
def new_league():
    """ new league route """

    if request.method == 'POST':
        error = None
        label = request.form['label']
        type = request.form['type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if label is None:
            error = 'Le nom de league est requis'
        if type is None:
            error = 'Le type de league est requis'
        if start_date is None or end_date is None:
            error = 'Les dates sont obligatoires'
        elif league_service.get_league_id_by_name() is not None:
            error = f"League {label} is already registered."

        if error is None:
            league_service.set_new_league(label, type, start_date, end_date)
            return redirect(url_for('index'))

        flash(error)

    return render_template('new_league.html')


# Auth route
@bp_auth.route('/login', methods=('GET', 'POST'))
def login():
    """ login page route"""
    if request.method == 'POST':
        password = request.form['password']
        error = None
        user = UserService.get_user_by_email()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp_auth.route('/logout')
def logout():
    """ logout page route"""
    session.clear()
    return redirect(url_for('index'))


@bp_auth.route('/signup', methods=('GET', 'POST'))
def signup():
    """ signup page route"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif UserService.get_user_by_email() is not None:
            error = f"User {username} is already registered."

        if error is None:
            UserService.create_or_update_user(username, generate_password_hash(password), email)
            return redirect(url_for('auth.login'))

        flash(error, category='message')

    return render_template('auth/signup.html')
