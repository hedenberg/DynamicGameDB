# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend
from dynamicgamedb.backend.model import Game, Platform
from dynamicgamedb.backend.database import db_session
from flask import request, jsonify, redirect, url_for

@backend.teardown_app_request
def shutdown_session(exception=None):
    db_session.remove()

@backend.route('/', methods=['GET'])
def home():
    print "Katten"
    return "Hello there"

@backend.route('/initp', methods=['GET'])
def initp():
    platform = Platform("PC")
    db_session.add(platform)
    db_session.commit()
    return redirect(url_for('backend.platforms'))

@backend.route('/initg', methods=['GET'])
def initg():
    platform = db_session.query(Platform).get(1)
    game1 = Game("Kattspelet",platform)
    game2 = Game("Hundspelet",platform)
    db_session.add(game1)
    db_session.add(game2)
    db_session.commit()
    return redirect(url_for('backend.games'))

@backend.route('/api/platforms', methods=['GET'])
def platforms():
    platforms = db_session.query(Platform).order_by(Platform.id)
    return jsonify({"platforms":[{"platform_id":platform.id,
                                  "platform_title":platform.name} for platform in platforms]})

@backend.route('/api/platform/<int:id>', methods=['GET'])
def platform(id):
    platform = db_session.query(Platform).get(id)
    return jsonify({"platform_id":platform.id,
                    "platform_title":platform.name})

@backend.route('/api/platform/add', methods=['POST'])
def add_platform():
    platform = Platform(request.form['name'])
    db_session.add(platform)
    try:
        db_session.commit()
    except Exception, e:
        return "Failed"
    return jsonify({"platform_id":platform.id,
                    "platform_title":platform.name})

@backend.route('/api/games', methods=['GET'])
def games():
    games = db_session.query(Game).order_by(Game.id)
    return jsonify({"games":[{"game_id":game.id,
                              "game_title":game.title,
                              "platform":game.platform.name,
                              "developer":game.developer} for game in games]})

@backend.route('/api/game/<int:id>', methods=['GET'])
def game(id):
    game = db_session.query(Game).get(id)
    return jsonify({"game_id":game.id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "developer":game.developer})

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