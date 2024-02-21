from flask import session, request
from .. import db


def get_all_players():
    return db.get_db().execute(
        'select * from player'
    ).fetchall()


def get_player_by_id(id):
    return db.get_db().execute(
        'select * from player where id = ?', (id,)
    ).fetchone()


# find in player_league table
def get_elo_by_ids(player_id, league_id):
    return db.get_db().execute(
        'select * from player_league where player_id = ? and league_id = ?', (player_id,league_id)
    ).fetchone()

def save_players_elo(player_id, player_elo, league_id):
    db.get_db().execute(
        'insert or replace into player_league(player_id, elo, league_id) values (?,?,?)',
        (player_id, player_elo, league_id)
    )
    db.get_db().commit()