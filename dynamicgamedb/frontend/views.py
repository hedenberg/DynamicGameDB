# -*- coding: utf-8 -*-
from dynamicgamedb.frontend import frontend
from flask import request, jsonify, redirect, url_for, render_template

@frontend.route('/games', methods=['GET'])
def home():
    return "Many games.. beautiful html and much css."

@frontend.route('/docs/api', methods=['GET'])
def api_doc():
    try:
        return render_template('api_doc.html')  
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
    



#************************ AWESOME ERROR FINDER ************************************
    # try:
    #     return render_template('create_game.html',friends_list=friends_list,game_type=game_type)
    # except:
    #     print "Exception in user code:"
    #     print '-'*60
    #     traceback.print_exc(file=sys.stdout)
    #     print '-'*60