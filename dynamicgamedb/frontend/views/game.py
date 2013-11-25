from dynamicgamedb.frontend import frontend, dgdb
from flask import request, jsonify, redirect, url_for, render_template
from dynamicgamedb.frontend.api_com import DynamicGameDB, Game, Platform
import sys, traceback

@frontend.route('/games', methods=['GET', 'POST'])
def games():
    print "games"
    games = dgdb.games()
    print "games return"
          # should be changed to what the search query was for
    if request.method == 'POST':
        search=request.form['search_field']
        return render_template("games.html", games=games, search=search)
    else: 
    # games_list = []
    # for game in games:
    #     games_list = games_list + " - %d %s %s %s" % (game.id, game.title, game.platform, game.developer)
        search = "GET"
        return render_template("games.html", games=games, search=search)
    

    #return render_template("games.html", games=games)

@frontend.route('/game/<int:id>', methods=['GET'])
def game(id):
    game = dgdb.game(id)
    games = dgdb.games()
    #game_str = "%d %s %s %s" % (game.id, game.title, game.platform, game.developer)
    return render_template("game.html", game=game, games=games)

@frontend.route('/game/add', methods=['GET','POST'])
def add_game():
    platforms = dgdb.platforms()
    if request.method == 'POST':
        game = dgdb.add_game(title=request.form['title'], platform_id=request.form['platform']) 
        try:
            return redirect(url_for('frontend.edit_game', id=game.id))
        except:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
    else:
        #TODO: form page for Adding games
        return render_template('add_game.html', platforms=platforms)


@frontend.route('/game/<int:id>/edit', methods=['GET','POST'])
def edit_game(id):
    game = dgdb.game(id)
    print "edit game"
    if request.method == 'POST':
        game = dgdb.edit_game(id, title=request.form['title'])
        return redirect(url_for('frontend.game', id=game.id))
    else:
        try:
            return render_template('edit_game.html',game=game)
        except:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
        
    
    #TODO: extended form page for editing games and givinhg additional data
    

@frontend.route('/game/<int:id>/connection', methods=['POST'])
def connect_game():
    print "Connecting Games :D"
    #TODO: connection mechanics
    return "connect game"