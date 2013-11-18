from dynamicgamedb.frontend import frontend, dgdb
from flask import request, jsonify, redirect, url_for, render_template
from dynamicgamedb.frontend.api_com import DynamicGameDB, Game

@frontend.route('/games', methods=['GET'])
def games():
    games = dgdb.games()
	# games_list = []
	# for game in games:
	#     games_list = games_list + " - %d %s %s %s" % (game.id, game.title, game.platform, game.developer)
    return render_template("games.html", games=games)

@frontend.route('/game/<int:id>', methods=['GET'])
def game(id):
    game = dgdb.game(id)
    #game_str = "%d %s %s %s" % (game.id, game.title, game.platform, game.developer)
    return render_template("game.html", game=game)

@frontend.route('/game/add', methods=['POST'])
def add_game():
	print "add game"
	#TODO: form page for Adding games


@frontend.route('/game/<int:id>/edit', methods=['POST'])
def edit_game():
	print "edit game"
	#TODO: extended form page for editing games and givinhg additional data


@frontend.route('/game/<int:id>/connection', methods=['POST'])
def connect_game():
	print "Connecting Games :D"
	#TODO: connection mechanics