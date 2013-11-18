# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend
from dynamicgamedb.backend.model import Game, Platform
from dynamicgamedb.backend.database import db_session
from flask import request, jsonify, redirect, url_for



@backend.route('/initp', methods=['GET'])
def initp():
    platform = Platform("PC")
    db_session.add(platform)
    db_session.commit()
    return redirect(url_for('backend.platforms'))

@backend.route('/initg', methods=['GET'])
def initg():
    platform = db_session.query(Platform).get(1)
    game1 = Game("Kattspelet",platform)
    game2 = Game("Hundspelet",platform)
    db_session.add(game1)
    db_session.add(game2)
    db_session.commit()
    return redirect(url_for('backend.games'))
