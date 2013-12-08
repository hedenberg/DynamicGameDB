# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend, oid
from dynamicgamedb.backend.model import Game, Platform, User
from dynamicgamedb.backend.database import db_session
from flask import Response, request, jsonify, redirect, url_for, session, g

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
        print "No client id provided"
    ## Get client from some magical database of accepted clients
    # client = magic
    # if client:
    session['client_id'] = client_id
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
        user = db_session.query(User).filter_by(openid=session['openid']).first()
        if user is None:
            print "openid stored but user not found, contact god and tell him this is bad."
        user.generate_new_ott()
        db_session.commit()
        return redirect(FRONTEND_URL + '/auth/?one_time_token=%s' % user.one_time_token)

@oid.after_login
def create_or_login(resp):
    print "create or login"
    session['openid'] = resp.identity_url
    user = db_session.query(User).filter_by(openid=resp.identity_url).first()
    if user is not None:
        #flash(u'Successfully signed in')
        print "user found - openid: ", session['openid']
        g.user = user
        user.generate_new_ott()
        db_session.commit()
        return redirect(FRONTEND_URL + '/auth/?one_time_token=%s' % user.one_time_token)
    print "no user - openid: ", session['openid']
    user = User(openid=session['openid'], email=resp.email)
    db_session.add(user)
    db_session.commit()
    user.generate_new_ott()
    db_session.commit()
    return redirect(FRONTEND_URL + '/auth/?one_time_token=%s' % user.one_time_token)

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
    user = db_session.query(User).filter_by(one_time_token=ott).first()
    if user is None:

        print "Invalid one time token"
        return "Invalid one time token"
    user.generate_new_token()
    db_session.commit()
    return user.token

@backend.route('/api/user', methods=['GET','POST'])
@backend.route('/api/user/', methods=['GET','POST'])
def user():
    print "backend user"
    #token = request.args.get("user_token", None)
    token = request.form.get('token', None)
    if not token:
        print "no token"
        return "lol failure"
    
    #Get openid from token
    print "token: ", token
    user = db_session.query(User).filter(User.token.like(token)).first()
    if user is None:
        users = db_session.query(User).order_by(User.token)
        for user in users:
            print "email: ", user.email
            print "user token: ", user.token
        print "what the actual fuck. "
    print "json user email: ", user.email
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
