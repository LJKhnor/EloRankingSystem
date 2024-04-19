"""Views module"""
import logging

from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from . import auth, business
from .auth import login_required
from .elo import elo
from .services import UserService, league_service, player_service, deck_service, match_service
from .utils import utils

# import csv

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : [%(levelname)s] %(name)s %(threadName)s : %(message)s')
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)
bp_auth = auth.bp
bp_business = business.bp

LOG = app.logger

"""Home route"""


@bp_business.route('/')
@login_required
def index():
    # pylint: disable=unused-argument
    LOG.info(""" Home route""")
    if request.method == 'GET':
        matches = match_service.get_last_five_matches()
        matches_fetched = []
        for match in matches:
            league_id = match['league_id']
            league_name = league_service.get_league_name_by_id(match['league_id'])['label']
            player_1_name = player_service.get_player_by_id(match['player_1_id'])['name']
            player_2_name = player_service.get_player_by_id(match['player_2_id'])['name']
            deck_1_name = deck_service.get_deck_by_id(match['deck_1_id'])['name']
            deck_2_name = deck_service.get_deck_by_id(match['deck_2_id'])['name']
            winner_name = player_service.get_player_by_id(match['winner_player_id'])['name']
            date = match['date']
            matches_fetched.append(
                ((league_id, league_name), player_1_name, deck_1_name, player_2_name, deck_2_name, winner_name, date))

    return render_template('index.html', **locals())


"""League route"""


@bp_business.route('/league', methods=('GET', 'POST'))
@login_required
def league():
    # pylint: disable=unused-argument
    LOG.info(""" league page route""")

    leagues = league_service.get_all_leagues()

    if request.method == 'POST':
        league_id = request.form['league']
        if league_id != '':
            # infos part
            league_infos = league_service.get_league_infos(league_id)
            # ratio parts
            rankings = league_service.get_league_ranking(league_id)

            rankings_deck = deck_service.get_deck_ranking(league_id)

            players_for_league = league_service.get_players_from_league(league_id)
            rankings_html = []
            rankings_deck_html = []
            ratio_win_lose_html = []
            nb_cols = (len(players_for_league) + 1)
            nb_rows = (len(players_for_league) + 1)
            nb_matches_html = []

            for ranking in rankings:
                rankings_html.append((ranking['name'], round(ranking['elo'], 2), utils.processColor(ranking, rankings)))

            for ranking_deck in rankings_deck:
                rankings_deck_html.append((ranking_deck['name'], round(ranking_deck['elo'], 2),
                                           utils.processColor(ranking_deck, rankings_deck)))

            for player in players_for_league:
                nb_play = league_service.get_number_play(player['id'], league_id)
                nb_win = league_service.get_number_win(player['id'], league_id)
                nb_lose = nb_play[0] - nb_win[0]
                ratio_win_lose_html.append((player['name'], nb_play[0], nb_win[0], nb_lose))

            for i in enumerate(players_for_league):
                nb_matches_player = []
                for j in enumerate(players_for_league):
                    nb_matches = league_service.get_count_matches(players_for_league[i]['id'], players_for_league[j]['id'],
                                                                  league_id)
                    nb_matches_player.append(nb_matches[0])
                nb_matches_html.append(nb_matches_player)

    return render_template('league.html', **locals())


"""New match route"""


@bp_business.route('/new_match', methods=('GET', 'POST'))
def new_match():
    # pylint: disable=unused-argument
    LOG.info(""" new match route """)
    i = elo.Implementation()

    leagues = league_service.get_all_leagues()
    players = player_service.get_all_players()
    decks = deck_service.get_all_decks()

    if request.method == 'GET':
        if request.values is not None:
            pass

    if request.method == 'POST':
        error = None

        league_id = request.form['league']
        date = request.form['start_date']
        player_1_id = request.form['player_1']
        player_2_id = request.form['player_2']
        deck_player_1_id = request.form['deck_player_1']
        deck_player_2_id = request.form['deck_player_2']
        winner_id = request.form['winner']

        # gérer les erreurs
        if league_id is None:
            error = "Aucune league valide choisie"
        if player_1_id is None:
            error = "Le joueur 1 choisi n'est pas valide"
        if player_2_id is None:
            error = "Le joueur 2 choisi n'est pas valide"
        if deck_player_1_id is None:
            error = "Le deck choisi pour le joueur 1 n'est pas correct"
        if deck_player_2_id is None:
            error = "Le deck choisi pour le joueur 2 n'est pas correct"
        if winner_id is None and (winner_id is not player_1_id or winner_id is not player_2_id):
            error = "Le vainqueur choisi n'est pas correct"

        if error is None:
            add_new_match_with_elo(deck_player_1_id, deck_player_2_id, i, league_id, player_1_id, player_2_id,
                                   winner_id)

            player_service.save_players_elo(i.getPlayer(player_1_id).name, i.getPlayerRating(player_1_id), league_id)
            deck_service.save_deck_elo(i.getDeck(deck_player_1_id).name, league_id, i.getDeckRating(deck_player_1_id))
            player_service.save_players_elo(i.getPlayer(player_2_id).name, i.getPlayerRating(player_2_id), league_id)
            deck_service.save_deck_elo(i.getDeck(deck_player_2_id).name, league_id, i.getDeckRating(deck_player_2_id))

            match_service.save_new_match(league_id, date, player_1_id, player_2_id, deck_player_1_id, deck_player_2_id,
                                         winner_id)
            return redirect(url_for('index'))

        LOG.error(error)

    return render_template('new_match.html',
                           **locals())  # locals() return all the variable set in the scope of the method


"""New league route"""


@bp_business.route('/new_league', methods=('GET', 'POST'))
@login_required
def new_league():
    # pylint: disable=unused-argument
    LOG.info(""" new league route """)

    if request.method == 'POST':
        error = None
        label = request.form['label']
        type_league = request.form['type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if label is None:
            error = 'Le nom de league est requis'
        if type_league is None:
            error = 'Le type de league est requis'
        if start_date is None or end_date is None:
            error = 'Les dates sont obligatoires'
        elif league_service.get_league_id_by_name() is not None:
            error = f"League {label} is already registered."

        if error is None:
            league_service.set_new_league(label, type_league, start_date, end_date)
            return redirect(url_for('index'))

        LOG.error(error)

    return render_template('new_league.html')


"""Rejeu route"""


@bp_business.route('/rejeu', methods=('GET', 'POST'))
@login_required
def rejeu():
    # pylint: disable=unused-argument
    # Outils de rejeu pour corriger l'ajout malencontreux via l'appli qui impacterait négativement le calcul de l'elo
    LOG.info("""Outil de rejeu""")
    leagues = league_service.get_all_leagues()
    error = None
    i = elo.Implementation()

    if request.method == 'GET':
        pass

    if request.method == 'POST':
        # gérer les erreurs
        league_id = request.form['league']
        if league_id is None:
            error = "Aucune league valide choisie"
        if error is None:
            # recupérer l'ensemble des matchs de la league choisie
            matches = league_service.getAllMatchesFromOneLeague(league_id)

            # vider les elo des joueurs et de leurs decks pour la league choisie
            league_service.deleteAllEloForPlayersForOneLeague(league_id)
            league_service.deleteAllEloForDecksForOneLeague(league_id)

            # reppasser chaque match dans l implementation
            for match in matches:
                league_id = match['league_id']
                player_1_id = match['player_1_id']
                player_2_id = match['player_2_id']
                deck_player_1_id = match['deck_1_id']
                deck_player_2_id = match['deck_2_id']
                winner_id = match['winner_player_id']

                add_new_match_with_elo(deck_player_1_id, deck_player_2_id, i, league_id, player_1_id, player_2_id,
                                       winner_id)

                player_service.save_players_elo(i.getPlayer(player_1_id).name, i.getPlayerRating(player_1_id),
                                                league_id)
                deck_service.save_deck_elo(i.getDeck(deck_player_1_id).name, league_id,
                                           i.getDeckRating(deck_player_1_id))
                player_service.save_players_elo(i.getPlayer(player_2_id).name, i.getPlayerRating(player_2_id),
                                                league_id)
                deck_service.save_deck_elo(i.getDeck(deck_player_2_id).name, league_id,
                                           i.getDeckRating(deck_player_2_id))
        else:
            LOG.error(error)

        return redirect(url_for('league'))

    return render_template('rejeu.html', **locals())


"""Add new match and process the elo for players and decks"""


def add_new_match_with_elo(deck_player_1_id, deck_player_2_id, i, league_id, player_1_id, player_2_id, winner_id):
    #  rechercher l'elo des 2 joueur pour la league en cours
    elo_player_1 = player_service.get_elo_by_ids(player_1_id, league_id)
    elo_player_2 = player_service.get_elo_by_ids(player_2_id, league_id)
    elo_deck_1 = deck_service.get_elo_by_ids(deck_player_1_id, league_id)
    elo_deck_2 = deck_service.get_elo_by_ids(deck_player_2_id, league_id)
    # insérer dans Implementation les joueur, leur rating et leurs decks
    i.addPlayer(player_1_id, None if elo_player_1 is None else elo_player_1['elo'])
    i.addPlayer(player_2_id, None if elo_player_2 is None else elo_player_2['elo'])
    i.addDeck(deck_player_1_id, None if elo_deck_1 is None else elo_deck_1['elo'])
    i.addDeck(deck_player_2_id, None if elo_deck_2 is None else elo_deck_2['elo'])
    i.processEloForMatch(player_1_id, deck_player_1_id, player_2_id, deck_player_2_id, winner=winner_id)

    elo_player_1 = 0 if elo_player_1 is None else elo_player_1['elo']
    elo_player_2 = 0 if elo_player_2 is None else elo_player_2['elo']
    LOG.info(
        f" Added match for player : {player_1_id} with ({elo_player_1}) and player : {player_2_id} with ({elo_player_2}) ")

    # pour générer un graphique via matplotlib

    # pour générer un csv avec les valeurs de chaque elo pour chaque joueur
    # with open('test_data_elo.csv', 'a', newline='') as csvfile:
    #     datawriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    #     datawriter.writerow([player_1_id,elo_player_1])
    #     datawriter.writerow([player_2_id,elo_player_2])


"""Auth route"""


@bp_auth.route('/login', methods=('GET', 'POST'))
def login():
    LOG.info(""" login page route""")
    if request.method == 'POST':
        password = request.form['password']
        error = None
        user = UserService.get_user_by_email()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        LOG.error(error)

    return render_template('auth/login.html')


"""Logout route"""
@bp_auth.route('/logout')
def logout():
    LOG.info(""" logout page route""")
    session.clear()
    return redirect(url_for('index'))


"""signup route"""
@bp_auth.route('/signup', methods=('GET', 'POST'))
def signup():
    LOG.info(""" signup page route""")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif UserService.get_user_by_email() is not None:
            error = f"User {username} is already registered."

        if error is None:
            UserService.create_or_update_user(username, generate_password_hash(password), email)
            return redirect(url_for('auth.login'))

        LOG.error(error)

    return render_template('auth/signup.html')


"""Error handler method 404"""
@app.errorhandler(404)
def page_not_found(error):
    LOG.error('An exception occurred during a request.', error)
    return render_template('page_not_found.html'), 404


"""Error handler method 500"""
@app.errorhandler(500)
def server_error(error):
    LOG.error('An exception occurred during a request.', error)
    return 'Internal Server Error', 500
