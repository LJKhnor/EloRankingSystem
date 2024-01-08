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