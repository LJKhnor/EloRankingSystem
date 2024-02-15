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
