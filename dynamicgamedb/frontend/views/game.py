from dynamicgamedb.frontend import frontend, dgdb
from flask import request, jsonify, redirect, url_for, render_template
from dynamicgamedb.frontend.api_com import DynamicGameDB, Game

@frontend.route('/games', methods=['GET'])
def games():
    games = dgdb.games()
    games_str = "Games:"
    for game in games:
        games_str = games_str + " - %d %s %s %s" % (game.id, game.title, game.platform, game.developer)
    return games_str

@frontend.route('/game/<int:id>', methods=['GET'])
def game(id):
    game = dgdb.game(id)
    game_str = "%d %s %s %s" % (game.id, game.title, game.platform, game.developer)
    return game_str