from flask import session, request
from .. import db

def get_all_decks():
    decks = db.get_db().execute(
        'SELECT * FROM deck '
    )
    return decks.fetchall()