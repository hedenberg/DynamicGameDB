from dynamicgamedb.frontend import frontend
from flask import request, jsonify, redirect, url_for, render_template, send_from_directory

@frontend.route('/docs/api', methods=['GET'])
def api_doc():
    return render_template('api_doc.html') 

@frontend.route('/docs/api_v2', methods=['GET'])
def api():
    return render_template('api.html') 