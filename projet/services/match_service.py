from flask import session, request
from .. import db

def save_new_match():
    db.get_db().execute(
        'INSERT INTO league (label, type, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)',
        (league, player_1, player_2, deck_player_1, deck_player_2, winner)
    )