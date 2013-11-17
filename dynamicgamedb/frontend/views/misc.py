from dynamicgamedb.frontend import frontend
from flask import request, jsonify, redirect, url_for, render_template

@frontend.route('/dynamicgamedb/frontend/static/css/<path:filename>')
def send_foo(filename):
     return send_from_directory('dynamicgamedb/frontend/static/css', filename)