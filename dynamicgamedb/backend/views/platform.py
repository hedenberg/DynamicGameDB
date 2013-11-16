# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend
from dynamicgamedb.backend.model import Game, Platform
from dynamicgamedb.backend.database import db_session
from flask import request, jsonify, redirect, url_for


@backend.route('/api/platforms', methods=['GET'])
def platforms():
    platforms = db_session.query(Platform).order_by(Platform.id)
    return jsonify({"platforms":[{"platform_id":platform.id,
                                  "platform_title":platform.name} for platform in platforms]})

@backend.route('/api/platform/<int:id>', methods=['GET'])
def platform(id):
    platform = db_session.query(Platform).get(id)
    return jsonify({"platform_id":platform.id,
                    "platform_title":platform.name})

@backend.route('/api/platform/add', methods=['POST'])
def add_platform():
    platform = Platform(request.form['name'])
    db_session.add(platform)
    try:
        db_session.commit()
    except Exception, e:
        return "Failed"
    return jsonify({"platform_id":platform.id,
                    "platform_title":platform.name})
