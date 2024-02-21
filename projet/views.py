from flask import Flask, render_template, request, session, flash, redirect, url_for
from . import auth, business
from .auth import login_required
from .db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from .services import UserService, league_service, player_service, deck_service, match_service
from .elo import elo

app = Flask(__name__)
bp_auth = auth.bp
bp_business = business.bp


@bp_business.route('/')
@login_required
def index():
    """ Root route"""
    if request.method == 'GET':
        matches = match_service.get_last_five_matches()
        matches_fetched = []
        for match in matches:
            league_name = league_service.get_league_name_by_id(match['league_id'])['label']
            player_1_name = player_service.get_player_by_id(match['player_1_id'])['name']
            player_2_name = player_service.get_player_by_id(match['player_2_id'])['name']
            deck_1_name = deck_service.get_deck_by_id(match['deck_1_id'])['name']
            deck_2_name = deck_service.get_deck_by_id(match['deck_2_id'])['name']
            winner_name = player_service.get_player_by_id(match['winner_player_id'])['name']
            matches_fetched.append((league_name, player_1_name, deck_1_name, player_2_name, deck_2_name, winner_name))

    return render_template('index.html', **locals())


@bp_business.route('/league', methods=('GET', 'POST'))
@login_required
def league():
    """ league page route"""

    leagues = league_service.get_all_leagues()

    if request.method == 'POST':
        league_id = request.form['league']
        if league_id != '':
            rankings = league_service.get_league_ranking(league_id)
            ratio_win_lose = league_service.get_players_ratio(league_id)
            rankings_html = []
            ratio_win_lose_html = []
            for ranking in rankings:
                rankings_html.append((ranking['name'], round(ranking['elo'],2)))
            for ratio in ratio_win_lose:
                ratio_win_lose_html.append(((ratio['name'], ratio['win'])))
    return render_template('league.html', **locals())


@bp_business.route('/new_match', methods=('GET', 'POST'))
def new_match():
    """ new match route """
    i = elo.Implementation()

    leagues = league_service.get_all_leagues()
    players = player_service.get_all_players()
    decks = deck_service.get_all_decks()

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
        if winner_id is None and (winner_id is not player_1_id or winner is not player_2_id):
            error = "Le vainqueur choisi n'est pas correct"

        if error is None:
            #  rechercher l'elo des 2 joueur pour la league en cours
            elo_player_1 = player_service.get_elo_by_ids(player_1_id, league_id)
            elo_player_2 = player_service.get_elo_by_ids(player_2_id, league_id)
            # insérer dans Implementation les joueur, leur rating et leurs decks
            i.addPlayer(player_1_id,None if elo_player_1 is None else elo_player_1['elo'])
            i.addPlayer(player_2_id,None if elo_player_2 is None else elo_player_2['elo'])
            i.addDeck(deck_player_1_id)
            i.addDeck(deck_player_2_id)

            i.processEloForMatch(player_1_id,deck_player_1_id,player_2_id,deck_player_2_id,winner=winner_id)

            player_service.save_players_elo(i.getPlayer(player_1_id).name, i.getPlayerRating(player_1_id),league_id)
            player_service.save_players_elo(i.getPlayer(player_2_id).name, i.getPlayerRating(player_2_id),league_id)

            match_service.save_new_match(league_id, date, player_1_id, player_2_id, deck_player_1_id, deck_player_2_id, winner_id)
            return redirect(url_for('index'))

        flash(error)

    return render_template('new_match.html', **locals()) # locals() return all the variable set in the scope of the method


@bp_business.route('/new_league', methods=('GET', 'POST'))
@login_required
def new_league():
    """ new league route """

    if request.method == 'POST':
        error = None
        label = request.form['label']
        type = request.form['type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if label is None:
            error = 'Le nom de league est requis'
        if type is None:
            error = 'Le type de league est requis'
        if start_date is None or end_date is None:
            error = 'Les dates sont obligatoires'
        elif league_service.get_league_id_by_name() is not None:
            error = f"League {label} is already registered."

        if error is None:
            league_service.set_new_league(label, type, start_date, end_date)
            return redirect(url_for('index'))

        flash(error)

    return render_template('new_league.html')


# Auth route
@bp_auth.route('/login', methods=('GET', 'POST'))
def login():
    """ login page route"""
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

        flash(error)

    return render_template('auth/login.html')


@bp_auth.route('/logout')
def logout():
    """ logout page route"""
    session.clear()
    return redirect(url_for('index'))


@bp_auth.route('/signup', methods=('GET', 'POST'))
def signup():
    """ signup page route"""
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

        flash(error, category='message')

    return render_template('auth/signup.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404