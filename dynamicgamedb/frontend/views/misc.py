 #!/usr/bin/python
# -- coding: utf-8 --

from dynamicgamedb.frontend import frontend, dgdb
import sys, traceback
from flask import request, jsonify, redirect, url_for, render_template, send_from_directory, session

#@frontend.route('/dynamicgamedb/frontend/static/<path:filename>')
#def send_foo(filename):
    #print "filename", filename
#    return send_from_directory('frontend/static', filename)


@frontend.route('/login/')
def new_login():
    return redirect(dgdb.api_login_url())

@frontend.route('/auth/')
def auth_onetime():
    print "frontend auth"
    if request.args.get("one_time_token"):
        print "One time token: ", request.args.get("one_time_token")
        token = dgdb.auth_token(request.args.get("one_time_token"))
        session["user_token"] = token
    print "redirect to /"
    return redirect("/")


@frontend.route('/')
def index():
    print "games"
    games = dgdb.get_games()
    #search = "GET"
    return render_template("games.html", games=games, search="GET")
"""
def index():
    print "INDEX"
    try:
        return render_template('index.html')
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
    """

    
    

@frontend.route('/about')
def about():
    return render_template('about.html')

@frontend.route('/contact')
def contact():  
    return render_template('contact.html')



        # try:
        #     return render_template('index.html')
        # except:
        #     print "Exception in user code:"
        #     print '-'*60
        #     traceback.print_exc(file=sys.stdout)
        #     print '-'*60