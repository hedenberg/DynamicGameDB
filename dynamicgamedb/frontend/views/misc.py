from dynamicgamedb.frontend import frontend
import sys, traceback
from flask import request, jsonify, redirect, url_for, render_template, send_from_directory

@frontend.route('/dynamicgamedb/frontend/static/<path:filename>')
def send_foo(filename):
    print "filename", filename
    return send_from_directory('dynamicgamedb/frontend/static', filename)




@frontend.route('/')
def index():
    try:
        return render_template('index.html')
    except:
        print "Exception in user code:"
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
    

    
    

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