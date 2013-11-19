# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend
from dynamicgamedb.backend.model import Game, Platform
from dynamicgamedb.backend.database import db_session
from flask import request, jsonify, redirect, url_for



@backend.route('/initp', methods=['GET'])
def initp():
    p1 = Platform("PC")
    db_session.add(p1)
    p2 = Platform("Xbox 360")
    db_session.add(p2)
    p3 = Platform("PlayStation 3")
    db_session.add(p3)
    p4 = Platform("PlayStation 4")
    db_session.add(p4)
    p5 = Platform("Xbox One")
    db_session.add(p5)
    p6 = Platform("Nintendo Entertainment System")
    db_session.add(p6)
    db_session.commit()
    return redirect(url_for('backend.platforms'))

@backend.route('/initg', methods=['GET'])
def initg():
    #platform = db_session.query(Platform).get(1)
    #game1 = Game("Kattspelet",platform)
    #game2 = Game("Hundspelet",platform)
    #game3 = Game("Battlefield 3",platform)
    #game4 = Game("Ett spel om fiskar",platform)
    #nintendo = db_session.query(Platform).get(6)
    #print nintendo.name
    #game5 = Game("Tetris",nintendo)
    #game6 = Game("Ett irriterande långt spelnamn kanske", nintendo) #Fungerar ej Yay! För långt eller pga åäö?
    #game7 = Game("Ölspelet", nintendo)
    #db_session.add(game1)
    #db_session.add(game2)
    #db_session.add(game3)
    #db_session.add(game4)
    #db_session.add(game5)
    #db_session.add(game6)
    #db_session.add(game7)
    #db_session.commit()
    return redirect(url_for('backend.games'))
