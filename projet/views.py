from flask import Flask, render_template, request, session, flash, redirect, url_for
from . import auth, business
from .auth import login_required
from .db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

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


# Auth route
@bp_auth.route('/login', methods=('GET', 'POST'))
def login():
    """ login page route"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

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
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                'INSERT INTO user (username, email, password) VALUES (?, ?, ?)',
                (username, email, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error, category='message')

    return render_template('auth/signup.html')