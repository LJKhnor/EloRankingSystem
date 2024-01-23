from flask import session, request
from .. import db


def get_user_by_id():
    user_id = session.get('user_id')
    return db.get_db().execute(
        'SELECT * FROM user WHERE id = ?', (user_id,)
    ).fetchone()


def get_user_by_email():
    email = request.form['email']
    return db.get_db().execute(
        'SELECT * FROM user WHERE email = ?', (email,)
    ).fetchone()


def create_or_update_user(username, password, email):
    db.get_db().execute(
        'INSERT INTO user (username, email, password) VALUES (?, ?, ?)',
        (username, email, password)
    )
    db.get_db().commit()
