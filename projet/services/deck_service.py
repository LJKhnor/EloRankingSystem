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

def save_deck_elo(deck_id, league_id, elo):
    db.get_db().execute(
        'insert or replace into deck_league (deck_id, league_id, elo) VALUES (?, ?, ?)',
        (deck_id, league_id, elo)
    )
    db.get_db().commit()
    
def get_elo_by_ids(deck_id, league_id):
    return db.get_db().execute(
        'select * from deck_league where deck_id = ? and league_id = ?', (deck_id, league_id)
    ).fetchone()

def get_deck_ranking(league_id):
    return db.get_db().execute(
        'select dl.deck_id, d.name, dl.elo from deck_league dl inner join deck d on d.id = dl.deck_id where league_id = ? order by dl.elo desc', (league_id)
    ).fetchall()