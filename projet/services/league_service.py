from flask import session, request
from .. import db


def get_league_id_by_name():
    league_label = request.form['label']
    return db.get_db().execute(
        'SELECT l.id FROM league l WHERE label = ?', (league_label,)
    ).fetchone()


def get_all_leagues():
    leagues = db.get_db().execute(
        'SELECT l.id,l.label, l.start_date FROM league l'
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


def get_players_from_league(league_id):
    return db.get_db().execute(
        'select p.id, p.name from player_deck_league pdl '
        'inner join player p on p.id = pdl.player_1_id or p.id = pdl.player_2_id '
        'where pdl.league_id = ?'
        'group by p.name '
        'order by p.id ', (league_id)
    ).fetchall()


def get_number_play(player_id, league_id):
    return db.get_db().execute(
        'select count(pdl.id) '
        'from player_deck_league pdl '
        'where (pdl.player_1_id = ? or pdl.player_2_id = ?) and pdl.league_id = ? ', (player_id, player_id, league_id)
    ).fetchone()


def get_number_win(player_id, league_id):
    return db.get_db().execute(
        'select count(pdl.id) '
        'from player_deck_league pdl '
        'where pdl.winner_player_id  = ? and pdl.league_id = ?', (player_id, league_id)
    ).fetchone()


def get_count_matches(player1_id, player2_id,league_id):
    return db.get_db().execute(
        'select count(*) '
        'from player_deck_league pdl '
        'where ((pdl.player_1_id = ? and pdl.player_2_id = ?) '
        'or (pdl.player_1_id = ? and pdl.player_2_id = ?)) and pdl.league_id= ?',
        (player1_id, player2_id, player2_id, player1_id, league_id)
    ).fetchone()


def get_league_infos(league_id):
    return db.get_db().execute(
        'select * from league where id = ?', (league_id,)
    ).fetchone()
