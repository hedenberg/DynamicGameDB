# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend
from dynamicgamedb.backend.model import Game, Platform
from dynamicgamedb.backend.database import db_session
from flask import request, jsonify, redirect, url_for

@backend.route('/api/games', methods=['GET'])
def games():
    print "api games"
    games = db_session.query(Game).order_by(Game.g_id)
    return jsonify({"games":[{"game_id":game.g_id,
                              "game_title":game.title,
                              "platform":game.platform.name,
                              "platform_id":game.platform.p_id,
                              "developer":game.developer} for game in games]})

@backend.route('/api/game/add', methods=['POST'])
def add_game():
    title = request.form['title']
    platform_id = str(request.form['platform_id'])
    print "add"
    games = Game.query.filter(Game.title.like(title)).all()
    print "games: ", games
    exists = False
    for game in games:
        print "game.title: ", game.title
        print "title: ", title
        print "game.pid: ", game.platform_id
        print "pid: ", platform_id
        if game.title == title and str(game.platform_id) == platform_id:
            exists = True
    if not exists:
        platform = db_session.query(Platform).get(request.form['platform_id'])
        if platform == None:
            print "Platform doesn't exist"
            return jsonify({"error":"Platform doesn't exist"})
        game = Game(request.form['title'], platform)
        db_session.add(game)
        db_session.commit()
    else:
        print "Already existed"
        game = games[0]
    return jsonify({"game_id":game.g_id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "platform_id":game.platform.p_id,
                    "developer":game.developer})

@backend.route('/api/game/<int:id>', methods=['GET'])
def game(id):
    game = db_session.query(Game).get(id)
    return jsonify({"game_id":game.g_id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "platform_id":game.platform.p_id,
                    "developer":game.developer})

@backend.route('/api/game/<int:id>/edit', methods=['POST'])
def edit_game(id):
    game = db_session.query(Game).get(id)
    print "Backend edit game title: ", request.form['title']
    game.title = request.form['title']
    #platform = db_session.query(Platform).get(request.form['platform_id'])
    #game.platform = platform
    #game.platform_id = platform_id
    #game.picture = # Must handle image
    #game.info = request.form['info']
    #game.release_date = # Must correctly handle date
    #game.developer = request.form['developer']
    #game.publisher = request.form['publisher']
    db_session.commit()
    return jsonify({"game_id":game.g_id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "developer":game.developer})