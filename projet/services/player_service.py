from flask import session, request
from .. import db
def get_all_players():
    return db.get_db().execute('select * from player').fetchall()