from dynamicgamedb.frontend import frontend, dgdb
from flask import request, jsonify, redirect, url_for, render_template
from dynamicgamedb.frontend.api_com import DynamicGameDB, Game

@frontend.route('/login', methods=['GET'])
def login():
   print "login"
   #TODO: openID login stuff
   return render_template('index.html')


@frontend.route('/logout', methods=['GET'])
def logout():
   print "logout"
   #TODO: openID logout stuff
   return render_template('index.html')