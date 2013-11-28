from dynamicgamedb.frontend import frontend, dgdb
from flask import request, jsonify, redirect, url_for, render_template
from dynamicgamedb.frontend.api_com import DynamicGameDB, Game, Platform
import sys, traceback
from datetime import datetime

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

@frontend.route('/game/<int:id>/', methods=['GET'])
def game(id):
    game = dgdb.game(id)
    print "platform_id: ", game.platform_id
    #game_str = "%d %s %s %s" % (game.id, game.title, game.platform, game.developer)
    #return render_template("game.html", game=game, games=games)
    try:
        games = dgdb.games()
        return render_template("game.html", game=game, games=games)
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

@frontend.route('/game/add', methods=['GET','POST'])
def add_game():
    platforms = dgdb.platforms()
    if request.method == 'POST':
        game = dgdb.add_game(title=request.form['title'],
                             platform_id=request.form['platform']) 
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
    platforms = dgdb.platforms()
    print "edit game"
    if request.method == 'POST':
        print "edit game POST"
        date = request.form['release_date']
        print "Date: ",date
        desc = request.form['description']
        print "Desc: ", desc
        #edit_game(self, id, title, platform_id, info, release_date, developer)
        game = dgdb.edit_game(id, 
                              title=request.form['title'],
                              platform_id=request.form['platform'],
                              info=request.form['description'],
                              release_date=request.form['release_date'],
                              developer=request.form['developer'],
                              publisher=request.form['publisher'])
        print "after backend call"
        return redirect(url_for('frontend.game', id=game.id))
    else:
        try:
            date = datetime.utcnow()
            print date
            return render_template('edit_game.html',game=game, platforms=platforms)
        except:
            print "Exception in user code:"
            print '-'*60
            traceback.print_exc(file=sys.stdout)
            print '-'*60
        
    
    #TODO: extended form page for editing games and givinhg additional data
    

@frontend.route('/game/<int:id>/relate', methods=['POST','GET'])
def search_relate_game(id):
    print "Connecting Games :D"
    if request.method == 'POST':
        print "POST"
        rel_search = request.form['relate_search_field']
        print rel_search
        game = dgdb.game(id)
        games = dgdb.games()
        return render_template('relate_game.html',games=games, game=game)
    else:

        #TODO: connection mechanics
        return "relate game"

@frontend.route('/game/<int:id>/relate/<int:relate_id>', methods=['POST','GET'])
def make_relation(id,relate_id):
    print "make relation", id , relate_id
    return redirect(url_for('frontend.game', id=id ))