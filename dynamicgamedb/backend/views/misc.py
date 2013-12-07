# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend, oid
from dynamicgamedb.backend.model import Game, Platform, User
from dynamicgamedb.backend.database import db_session
from flask import Response, request, jsonify, redirect, url_for, session

FRONTEND_URL = 'http://localhost:8000'

@backend.route('/api/logout/')
def logout():
    session.pop('openid', None)
    #flash(u'You were signed out')
    return redirect(oid.get_next_url())

@backend.route('/api/login/')
@oid.loginhandler
def api_login():
    client_id = request.args.get("client_id", None)
    print "clientid: ", client_id
    if not client_id:
        """
        response = Response(    ## This should totaly be defined as a helper function somewhere...
            json.dumps({"error": { 
                "type": "DGDBApiException", 
                "message": "Why did you forget client_id!?" 
            }}),
            mimetype="application/json",
            status=400 # Bad request, bad!
        )
        return response
        """
        print "Something went wrong but I'll allow it for now"
        ##return "This is wrong"
    session['client_id'] = client_id
    ## Get client from some magical database of accepted clients
    # client = magic
    # if client:
    if not "openid" in session:
        print "not openid"
        # Redirect to google 
        # But for now redirect to a fake endpoint
        print "redirect to google"
        return oid.try_login( 'https://www.google.com/accounts/o8/id', ask_for=['email'])
    else:
        print "openid in session: ", session['openid']
        # Already logged in but didn't know it so we provide a new code for them
        # to generate a new token.
        # Store one time token in database
        # Redirect to frontend with a code so that frontend can request a new token
        return redirect(FRONTEND_URL+'/auth/?one_time_token=1337')

@oid.after_login
def create_or_login(resp):
    print "create or login"
    session['openid'] = resp.identity_url
    user = db_session.query(User).filter_by(openid=resp.identity_url).first()
    if user is not None:
        #flash(u'Successfully signed in')
        print "user found - openid: ", session['openid']
        g.user = user
        return redirect(FRONTEND_URL+'/auth/?one_time_token=1337')
    print "no user - openid: ", session['openid']
    db_session.add(User(openid=session['openid'], email=resp.email))
    db_session.commit()
    return redirect(FRONTEND_URL+'/auth/?one_time_token=1337')

@backend.route('/api/token', methods=['GET','POST'])
@backend.route('/api/token/', methods=['GET','POST'])
def api_token():
    print "api token"
    ott = request.form.get('one_time_token', None)
    #ott = request.args.get("one_time_token", None)
    if not ott:
        return "there is no one time token biatch"
    # Get one time token from database 
    # check if it existed as described in database
    token = 7331 #Generate magical token and store in database
    print "returning token 7331"
    return str(token)

@backend.route('/api/user/')
def user():
    token = request.args.get("user_token", None)
    if not token:
        return "lol failure"
    
    #Get openid from token
    user = db_session.query(User).get(token)
    return jsonify({"user_email":user.email})

@backend.route('/initp', methods=['GET'])
def initp():
    p1 = Platform("PC")
    db_session.add(p1)
    p2 = Platform("Xbox 360")
    db_session.add(p2)
    p3 = Platform("PlayStation 3")
    db_session.add(p3)
    p4 = Platform("PlayStation 4")
    db_session.add(p4)
    p5 = Platform("Xbox One")
    db_session.add(p5)
    p6 = Platform("Nintendo Entertainment System")
    db_session.add(p6)
    db_session.commit()
    return redirect(url_for('backend.platforms'))

@backend.route('/initg', methods=['GET'])
def initg():
    platform = db_session.query(Platform).get(1)
    game1 = Game("Kattspelet",platform)
    game2 = Game("Hundspelet",platform)
    game3 = Game("Battlefield 3",platform)
    game4 = Game("Ett spel om fiskar",platform)
    #nintendo = db_session.query(Platform).get(6)
    #print nintendo.name
    #game5 = Game("Tetris",nintendo)
    #game6 = Game("Ett irriterande långt spelnamn kanske", nintendo) #Fungerar ej Yay! För långt eller pga åäö?
    #game7 = Game("Ölspelet", nintendo)
    db_session.add(game1)
    db_session.add(game2)
    db_session.add(game3)
    db_session.add(game4)
    #db_session.add(game5)
    #db_session.add(game6)
    #db_session.add(game7)
    db_session.commit()
    return redirect(url_for('backend.games'))
