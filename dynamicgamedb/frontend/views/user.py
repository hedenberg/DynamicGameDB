from dynamicgamedb.frontend import frontend, dgdb
from flask import request, jsonify, redirect, url_for, render_template,g, session,flash
from dynamicgamedb.frontend.api_com import DynamicGameDB, Game
from flask.ext.openid import OpenID

oid = OpenID(frontend, 'sqlite:///dynamicgame.db')       
# oid = OpenID(frontend, 'postgres://jmcqxvdgcsvsyl:BlvratbaAe05GQYS6HQIjX_ZIX@ec2-184-73-254-144.compute-1.amazonaws.com:5432/d10k9sruavbqno')

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
    if request.method == 'POST':
        openid = request.form.get('openid')
        if openid:
            return oid.try_login(openid, ask_for=['email','fullname','nickname'])
    return render_template('index.html', next=oid.get_next_url(), error=oid.fetch_error())

@oid.after_login
def create_or_login(resp):
    session['openid'] = resp.identity_url
    user = User.query.filter_by(openid=resp.identity_url).first()
    if user is not None:
        flash(u'Successfully signed in')
        g.user = user
        return redirect(oid.get_next_url())
    return redirect(url_for('create_profile', next=oid.get_next_url(), name=resp.fullname or resp.nickname, email=resp.email))

@app.route('/create-profile', methods=['GET', 'POST'])
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


@app.route('/logout')
def logout():
    session.pop('openid', None)
    flash(u'You were signed out')
    return redirect(oid.get_next_url())