from flask import session, request
from .. import db


def get_league_id_by_name():
    league_label = request.form['label']
    return db.get_db().execute(
        'SELECT l.id FROM league l WHERE label = ?', (league_label,)
    ).fetchone()


def get_all_leagues():
    leagues = db.get_db().execute(
        'SELECT l.id,l.label FROM league l'
    )
    return leagues.fetchall()


def get_league_name_by_id(id):
    league_name = db.get_db().execute(
        'SELECT label FROM league  WHERE id = ?', (id,)
    )
    return league_name.fetchone()


def set_new_league(label, type, start_date, end_date):
    db.get_db().execute(
        'INSERT INTO league (label, type, start_date, end_date) VALUES (?, ?, ?, ?)',
        (label, type, start_date, end_date)
    )

    db.get_db().commit()


def get_league_ranking(league_id):
    return db.get_db().execute(
        'select p.name, pl.elo from player_league pl '
        'inner join player p on pl.player_id = p.id '
        'where pl.league_id = ? '
        'order by pl.elo desc', (league_id)
    ).fetchall()
