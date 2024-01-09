from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """ Root route"""
    return render_template('index.html')
@app.route('/league')
def league():
    """ league page route"""
    return render_template('league.html')
@app.route('/login')
def login():
    """ league page route"""
    return render_template('login.html')
@app.route('/logout')
def logout():
    """ league page route"""
    return render_template('logout.html')
@app.route('/signup')
def signup():
    """ league page route"""
    return render_template('signup.html')