from dynamicgamedb.frontend import frontend, dgdb
from flask import request, jsonify, redirect, url_for, render_template
from dynamicgamedb.frontend.api_com import DynamicGameDB, Game

@frontend.route('/platforms', methods=['GET'])
def platforms():
    platforms=[]
    #platforms = dgdb.platforms()
    # games_list = []
    # for game in games:
    #     games_list = games_list + " - %d %s %s %s" % (game.id, game.title, game.platform, game.developer)
    return render_template("platforms.html", platforms=platforms)

@frontend.route('/platform/<int:id>', methods=['GET'])
def platform(id):
    platform =[]
    #platform = dgdb.platform(id)
    #game_str = "%d %s %s %s" % (game.id, game.title, game.platform, game.developer)
    return render_template("platform.html", platform=platform)

@frontend.route('/platform/add', methods=['GET','POST'])
def add_platform():
    print "add platform"
    #TODO: form page for platforms