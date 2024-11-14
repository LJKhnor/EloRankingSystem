<!-- TOC -->
# Table of content
- [Table of content](#table-of-content)
- [EloRankingSystem](#elorankingsystem)
  - [Overview](#overview)
  - [What is the Elo Rating System?](#what-is-the-elo-rating-system)
  - [Calculations](#calculations)
- [Project configuration and how to run](#project-configuration-and-how-to-run)
  - [Setup dev environment](#setup-dev-environment)
    - [.venv](#venv)
    - [Install dependencies](#install-dependencies)
  - [Application Structure](#application-structure)
  - [Install Flask](#install-flask)
  - [Install DB](#install-db)
  - [Feed DB](#feed-db)
<!-- TOC -->

# EloRankingSystem
A python application for the Elo Rating. It provide a backend system to manage ELO league, and will provide a web application to allow user to create and manage their ELO league.

This code originally come from https://github.com/HankSheehan/EloPy
Originally create as a librairy, it contain only one simply file.
So to integrate this code directly in a application, the development 
will be integrate around. Some changes had to be make to be more accurate for our needs.

## Overview
Game and league management screen
![Game and league management screen](/projet/static/logo/écran%20acceuil%20Elo%20Ranking%20System.png "Game and league management screen")

New match screen
![New match screen](/projet/static/logo/écran%20nouveaux%20match%20ERS.png "New match screen")

New league screen
![New league screen](/projet/static/logo/écran%20nouvelle%20league%20ERS.png "New league screen")

Statistics dashboard league screen
![Statistics dashboard leaguescreen](/projet/static/logo/écran%20stat%20ERS.png "Statistics dashboard league screen")

## What is the Elo Rating System?
* The Elo Rating System (Elo) is a rating system used for rating players in games. Originally developed for chess by Arpad Elo, Elo has been applied to a large array of games.
* Each player is assigned a number as a rating. The system predicts the outcome of a match between two players by using an expected score formula (i.e. a player whose rating is 100 points greater than their opponent's is expected to win 64% of the time).
* Everytime a game is played, the Elo rating of the participants change depending on the outcome and the expected outcome. The winner takes points from the loser; the amount is determined by the players' scores and ratings
* A win is counts as a score of 1, loss is a score of 0, and draw is a score of 0.5


## Calculations
If Player A has a rating of R<sub>A</sub> and Player B a rating of R<sub>B</sub>, the exact formula for Player A's score is:

![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/51346e1c65f857c0025647173ae48ddac904adcb)

And Player B's score is:

![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/4b340e7d15e61ee7d90f428dcf7f4b3c049d89ff)

Supposing Player A was expected to score E<sub>A</sub> points but actually scored S<sub>A</sub> points. The formula for updating his/her rating is:

![alt text](https://wikimedia.org/api/rest_v1/media/math/render/svg/09a11111b433582eccbb22c740486264549d1129)

Right now the K factor is found by the number of player multiplied by 42 as a constant. Working on custom K factors.


# Project configuration and how to run
## Setup dev environment 
### .venv
In dev proccess we need to use an .env environment. To do this use, in your folder project
`py -3 -m venv .venv`
To activate it, use
`.venv\Scripts\activate`
### Install dependencies
Flask is a framework that provide a lot of fonctionnalities.
In this application we use lot of basic fonctionalities, such sqlite for database management, bulma for CSS, ...
In your .venv you need to install dependencies for those fonctionalities.
Your requirements.txt is here to concentrate your dependencies.
You can install those dependencies with the next command.
Run `pip install -r requirements.txt`

Your application will start when you run your app.py file with all the configuration put in your .venv with this command
`py app.py`

you are now in your dev environment and can access to the web page here -> `localhost:5000`

## Application Structure
Flask is a framework that provide a lot of fonctionnalities.
But in a basic approach some file or package need to have their specific name unchanged. ex: static, templates, _ _ init _ _, ...

## Install Flask 
[Documentation](https://flask.palletsprojects.com/en/3.0.x/installation/)

`pip install Flask`

## Install DB
For this projet we use a simple DB infrastructure ans we need to create team in our projet
in local.
Run the init-db command in your .venv

`flask init-db`

You see the now "Initialized the database." in your console.

There will be now a flaskr.sqlite file in the instance folder of your project.
It's your local DB and you can access it with DB Browser or DBeaver.
Use .SQlite connection.

Warning !
Sqlite don't allow concurency, so if you want to execute falsk init-db, don't open a connection with DBeaver

Congratulation folks, you have a DB.

## Feed DB
In DBeaver or in other way use the script in [start_db.txt](start_db.txt) file to populate your db for the base to start with.



