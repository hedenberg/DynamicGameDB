
from dynamicgamedb.frontend import frontend, dgdb
from flask import Flask,request, jsonify, redirect, url_for, render_template,g, session, flash, current_app
from dynamicgamedb.frontend.api_com import DynamicGameDB, Game
#import dynamicgamedb 
import sys, traceback, os


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
        print "token: ", token
    print "redirect to /"
    return redirect("/")

