from dynamicgamedb.frontend import frontend, dgdb
from flask import request, jsonify, redirect, url_for, render_template, flash
from dynamicgamedb.frontend.api_com import DynamicGameDB, Game, Platform, GameRelation
from dynamicgamedb.frontend.api_com.models import DGDB_Error
import sys, traceback
from datetime import datetime

@frontend.route('/games', methods=['GET', 'POST'])
def games():
    if request.method == 'POST':
        try:
            games = dgdb.games(search_term=request.form['search_field'])
        except Exception, e:
            flash(e.message)
            return redirect(url_for('frontend.index'))
        search=request.form['search_field']
        return render_template("games.html", games=games, search=search)
    else: 
        try:
            games =  dgdb.get_games()
        except Exception, e:
            flash(e.message)
            return redirect(url_for('frontend.index'))
        games =  dgdb.get_games()
        search = "GET"
        return render_template("games.html", games=games, search=search)
    

    #return render_template("games.html", games=games)

@frontend.route('/game/<int:id>/', methods=['GET'])
def game(id):
    try:
        game = dgdb.game(id)
    except Exception, e:
        flash(e.message)
    games = dgdb.game_relations(id)
    return render_template("game.html", game=game, games=games)

@frontend.route('/game/add/', methods=['GET','POST'])
@frontend.login_required
def add_game():
    print "add game frontend"
    platforms = dgdb.platforms()
    if request.method == 'POST':
        try:
            game = dgdb.add_game(title=request.form['title'],
                                 platform_id=request.form['platform']) 
        except Exception, e:
            flash(e.message)
            return redirect(url_for('frontend.add_game'))
        return redirect(url_for('frontend.edit_game', id=game.id))
    else:
        return render_template('add_game.html', platforms=platforms)

@frontend.route('/game/<int:id>/edit/', methods=['GET','POST'])
@frontend.login_required
def edit_game(id):
    game = dgdb.game(id)
    platforms = dgdb.platforms()
    print "edit game"
    if request.method == 'POST':
        try:
            game = dgdb.edit_game(id, 
                              title=request.form['title'],
                              platform_id=request.form['platform'],
                              info=request.form['description'],
                              #picture=request.form['picture'],
                              release_date=request.form['release_date'],
                              developer=request.form['developer'],
                              publisher=request.form['publisher'])
        except Exception, e:
            flash(e.message)
            return redirect(url_for('frontend.edit_game', id=id))
        print "after backend call"
        return redirect(url_for('frontend.game', id=game.id))
    else:
        date = datetime.utcnow()
        print date
        return render_template('edit_game.html',game=game, platforms=platforms)
        
@frontend.route('/game/<int:id>/edit_picture/', methods=['POST'])
@frontend.login_required
def edit_picture(id):

    game = dgdb.game(id)
    #platforms = dgdb.platforms()
    print "edit picture ****************************************"
    if request.method == 'POST':
        print "test"
        #try:
        print "try test"
        picture = request.files['picture']
        print "test moar"
        print "THIS FILE UPLOAD", picture
            # game = dgdb.edit_game(id, 
            #                   title=request.form['title'],
            #                   platform_id=request.form['platform'],
            #                   info=request.form['description'],
            #                   #picture=request.form['picture'],
            #                   release_date=request.form['release_date'],
            #                   developer=request.form['developer'],
            #                   publisher=request.form['publisher'])
        #except Exception, e:
            #flash(e.message)
        return redirect(url_for('frontend.game', id=game.id))
    else:
        date = datetime.utcnow()
        print date
        return render_template('edit_game.html',game=game, platforms=platforms)    
    #TODO: extended form page for editing games and givinhg additional data
    

@frontend.route('/game/<int:id>/relate', methods=['POST','GET'])
@frontend.login_required
def search_relate_game(id):
    print "Connecting Games :D"
    if request.method == 'POST':
        print "POST"
        rel_search = request.form['relate_search_field']
        print rel_search
        game = dgdb.game(id)
        games = dgdb.games(search_term=rel_search)
        return render_template('relate_game.html',games=games, game=game, search=rel_search)
    else:
        game   = dgdb.game(id)
        games  = dgdb.game_relations(id)
        #TODO: connection mechanics
        return render_template('relate_game.html',games=games, game=game, search="GET")

@frontend.route('/game/<int:id>/relate/<relate_id>/', methods=['POST','GET'])
@frontend.login_required
def make_relation(id,relate_id):
    print "make relation", id , relate_id
    try:
        dgdb.add_game_relation(id,relate_id)
    except Exception, e:
        print "DBDB_ERROR"
        flash(e.message, "warning")
    print "relation made"
    return redirect(url_for('frontend.game', id=id ))