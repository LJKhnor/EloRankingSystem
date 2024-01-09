<!-- TOC -->
# Table of content
* [EloRankingSystem](#elorankingsystem)
  * [What is the Elo Rating System?](#what-is-the-elo-rating-system)
  * [Calculations](#calculations)
* [Project configuration and how to run](#project-configuration-and-how-to-run)
  * [Setup dev environment](#setup-dev-environment-)
    * [.venv](#venv)
    * [Install dependencies](#install-dependencies)
  * [Install Flask](#install-flask-)
<!-- TOC -->

# EloRankingSystem
A python application for the Elo Rating. It provide a backend system to manage ELO league, and will provide a web application to allow user to create and manage their ELO league.

This code originally come from https://github.com/HankSheehan/EloPy
Originally create as a librairy, it contain only one simply file.
So to integrate this code directly in a application, the development 
will be integrate around.

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
Run `pip install -r requirements.txt`

Your application will start when you run your run.py file 

you are now in your dev environment

## Install Flask 
(https://flask.palletsprojects.com/en/3.0.x/installation/)

`pip install Flask`
