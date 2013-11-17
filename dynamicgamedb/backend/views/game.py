# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend
from dynamicgamedb.backend.model import Game, Platform
from dynamicgamedb.backend.database import db_session
from flask import request, jsonify, redirect, url_for

@backend.route('/api/games', methods=['GET'])
def games():
    games = db_session.query(Game).order_by(Game.id)
    return jsonify({"games":[{"game_id":game.id,
                              "game_title":game.title,
                              "platform":game.platform.name,
                              "developer":game.developer} for game in games]})

@backend.route('/api/game/add', methods=['POST'])
def add_game():
    platform = db_session.query(Platform).get(request.form['platform_id'])
    game = Game(request.form['title'])
    db_session.add(game)
    try:
        db_session.commit()
    except Exception, e:
        return "Failed"
    return jsonify({"game_id":game.id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "developer":game.developer})

@backend.route('/api/game/<int:id>', methods=['GET'])
def game(id):
    game = db_session.query(Game).get(id)
    return jsonify({"game_id":game.id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "developer":game.developer})

@backend.route('/api/game/<int:id>/edit', methods=['POST'])
def edit_game(id):
    game = db_session.query(Game).get(id)
    #game.title = request.form['title']
    #platform = db_session.query(Platform).get(request.form['platform_id'])
    #game.platform = platform
    #game.platform_id = platform_id
    #game.picture = # Must handle image
    #game.info = request.form['info']
    #game.release_date = # Must correctly handle date
    game.developer = request.form['developer']
    #game.publisher = request.form['publisher']

    db_session.commit()

    return jsonify({"game_id":game.id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "developer":game.developer})