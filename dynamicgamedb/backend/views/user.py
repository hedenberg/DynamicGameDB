# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend, oid
from dynamicgamedb.backend.model import Game, Platform, User, Relation, Client
from dynamicgamedb.backend.database import db_session

from flask import Response, request, jsonify, redirect, url_for, session, g
import dateutil.parser

#FRONTEND_URL = 'http://localhost:8000'
FRONTEND_URL = 'http://dynamicgamedb.herokuapp.com'

@backend.route('/api/logout/')
def logout():
    session.pop('openid', None)
    #flash(u'You were signed out')
    return redirect(oid.get_next_url())

@backend.route('/api/login/')
@oid.loginhandler
def api_login():
    if not "openid" in session:
        print "no openid in session redirecting to google"
        return oid.try_login( 'https://www.google.com/accounts/o8/id', ask_for=['email'])
    else:
        print "openid in session: ", session['openid']
        user = db_session.query(User).filter_by(openid=session['openid']).first()
        if user is None:
            return backend.get_error_response(
                message="No user with that openid exists.",
                status_code=404)
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

@backend.route('/api/token/', methods=['GET','POST'])
@backend.client_required
def api_token():
    print "api token"
    ott = request.form.get('one_time_token', None)
    #ott = request.args.get("one_time_token", None)
    if not ott:
        print "/api/token/ there was no one time token"
        return backend.get_error_response(
            message="No OneTimeToken was provided.",
            status_code=404)
    # Get one time token from database 
    # check if it existed as described in database
    user = db_session.query(User).filter_by(one_time_token=ott).first()
    if user is None:
        print "Invalid one time token"
        return backend.get_error_response(
            message="The one time token was invalid, try logging in again.",
            status_code=404)
    user.generate_new_token()
    db_session.commit()
    return user.token

@backend.route('/api/user/', methods=['GET','POST'])
def user():
    print "backend user"
    #token = request.args.get("user_token", None)
    token = request.form.get('token', None)
    if not token:
        print "no token"
        return backend.get_error_response(
            message="No token was provided.",
            status_code=404)
    
    #Get openid from token
    print "token: ", token
    user = db_session.query(User).filter(User.token.like(token)).first()
    if user is None:
        return backend.get_error_response(
            message="Token was invalid.",
            status_code=404)
    print "json user email: ", user.email
    return jsonify({"user_email":user.email})