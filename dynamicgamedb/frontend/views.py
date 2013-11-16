# -*- coding: utf-8 -*-
from dynamicgamedb.frontend import frontend
from flask import request, jsonify, redirect, url_for

@frontend.route('/games', methods=['GET'])
def home():
    return "Many games.. beautiful html and much css."

@frontend.route('/docs/api', methods=['GET'])
def api_doc():
    return "Much api info"