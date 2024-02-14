from flask import session, request
from .. import db

def save_new_match(league_id, date, player_1_id, player_2_id, deck_player_1_id, deck_player_2_id, winner_id):
    db.get_db().execute(
        'insert into player_deck_league (player_1_id, player_2_id, deck_1_id, deck_2_id, league_id, date, winner_player_id) '
        'values (?, ?, ?, ?, ?, ?, ?)',
        (player_1_id, player_2_id, deck_player_1_id, deck_player_2_id, league_id, date, winner_id)
    )
    db.get_db().commit()

def get_last_five_matches():
    c = db.get_db().cursor()
    return c.execute(
        'SELECT * FROM player_deck_league p LIMIT 5'
    ).fetchall()
