from flask import session, request
from .. import db

def get_all_decks():
    decks = db.get_db().execute(
        'SELECT * FROM deck '
    )
    return decks.fetchall()

def get_deck_by_id(id):
    return db.get_db().execute(
        'select * from deck where id = ?', (id,)
    ).fetchone()