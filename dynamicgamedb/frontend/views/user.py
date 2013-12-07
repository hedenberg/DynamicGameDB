
from dynamicgamedb.frontend import frontend, dgdb
from flask import Flask,request, jsonify, redirect, url_for, render_template,g, session, flash, current_app
from dynamicgamedb.frontend.api_com import DynamicGameDB, Game
#import dynamicgamedb 
import sys, traceback, os



#from dynamicgamedb import oid
from flask.ext.openid import OpenID


oid = OpenID( '../openid')
def create_app():
    ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../static')
    app = Flask(__name__, static_folder=ASSETS_DIR)
    oid.init_app(app)
    return app


@frontend.before_request
def lookup_current_user():
    g.user = None
    if 'openid' in session:
        g.user = User.query.filter_by(openid=openid).first() #openid???




@frontend.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None:
        return redirect(oid.get_next_url())
    else:
        return oid.try_login( 'https://www.google.com/accounts/o8/id', ask_for=['email'])
    

@oid.after_login
def create_or_login(resp):
    print "create or login"
    session['openid'] = resp.identity_url
    user = User.query.filter_by(openid=resp.identity_url).first()
    if user is not None:
        flash(u'Successfully signed in')
        g.user = user
        return redirect(oid.get_next_url())
    return redirect(url_for('create_profile', next=oid.get_next_url(), email=resp.email))



@frontend.route('/create-profile', methods=['GET', 'POST'])
def create_profile():
    if g.user is not None or 'openid' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        if not name:
            flash(u'Error: you have to provide a name')
        elif '@' not in email:
            flash(u'Error: you have to enter a valid email address')
        else:
            flash(u'Profile successfully created')
            db_session.add(User(name, email, session['openid']))
            db_session.commit()
            return redirect(oid.get_next_url())
    return render_template('create_profile.html', next_url=oid.get_next_url())


@frontend.route('/logout')
def logout():
    session.pop('openid', None)
    flash(u'You were signed out')
    return redirect(oid.get_next_url())