from dynamicgamedb.frontend import frontend
from flask import request, jsonify, redirect, url_for, render_template

@frontend.route('/dynamicgamedb/frontend/static/css/<path:filename>')
def send_foo(filename):
     return send_from_directory('dynamicgamedb/frontend/static/css', filename)




@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/about')
def about():
    return render_template('about.html')

@frontend.route('/contact')
def contact():  
    return render_template('contact.html')