# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend
from dynamicgamedb.backend.model import Game, Platform, Relation
from dynamicgamedb.backend.database import db_session
from flask import request, jsonify, redirect, url_for


@backend.route('/api/relations/', methods=['GET'])
def relations():
    relations = db_session.query(Relation).order_by(Relation.game1_id)
    return jsonify({"relations":[{"g1_id":relation.game1_id,
                                  "g2_id":relation.game2_id,
                                  "count":relation.count} for relation in relations]})

@backend.route('/api/relation/<int:id>/', methods=['GET'])
def relation(id):
    relations = Relation.query.filter((Relation.game1_id==id)|(Relation.game2_id==id)).all()
    return jsonify({"relations":[{"g1_id":relation.game1_id,
                                  "g2_id":relation.game2_id,
                                  "count":relation.count} for relation in relations]})

@backend.route('/api/relation/add/', methods=['POST'])
def add_relation():
    in1 = request.form['g1_id']
    in2 = request.form['g2_id']
    if in1 == in2:
        return jsonify({"error":"Can not relate to self"})
    g1id = in1 if in1 < in2 else in2
    g2id = in2 if in1 < in2 else in1
    g1 = db_session.query(Game).get(g1id)
    g2 = db_session.query(Game).get(g2id)
    if g1 == None:
        return jsonify({"error":"Source id doesn't exist"})
    if g2 == None:
        return jsonify({"error":"Target id doesn't exist"})
    #Always least id first
    relation = db_session.query(Relation).get((g1.g_id,g2.g_id))
    if relation == None:
        print "Relation was None"
        relation = Relation(g1,g2)
        db_session.add(relation)
    else:
        relation.count = relation.count + 1
    try:
        db_session.commit()
    except Exception, e:
        return "Failed"
    return jsonify({"g1_id":relation.game1_id,
                    "g2_id":relation.game2_id,
                    "count":relation.count})
