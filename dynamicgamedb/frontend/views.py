# -*- coding: utf-8 -*-
from dynamicgamedb.frontend import frontend
from flask import request, jsonify, redirect, url_for, render_template, send_from_directory

@frontend.route('/games', methods=['GET'])
def home():
    return "Many games.. beautiful html and much css."

@frontend.route('/docs/api', methods=['GET'])
def api_doc():
    return render_template('api_doc.html') 

@frontend.route('/dynamicgamedb/frontend/static/css/<path:filename>')
def send_foo(filename):
     return send_from_directory('dynamicgamedb/frontend/static/css', filename)
    



#************************ AWESOME ERROR FINDER ************************************
    # try:
    #     return render_template('create_game.html',friends_list=friends_list,game_type=game_type)
    # except:
    #     print "Exception in user code:"
    #     print '-'*60
    #     traceback.print_exc(file=sys.stdout)
    #     print '-'*60