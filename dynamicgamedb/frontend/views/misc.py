 #!/usr/bin/python
# -- coding: utf-8 --

from dynamicgamedb.frontend import frontend, dgdb
import sys, traceback
from flask import request, jsonify, redirect, url_for, render_template, send_from_directory, session



@frontend.route('/')
def index():
    print "games"
    games = dgdb.get_games()
    #search = "GET"
    return render_template("games.html", games=games, search="GET")


@frontend.route('/about')
def about():
    return render_template('about.html')

@frontend.route('/contact')
def contact():  
    return render_template('contact.html')
