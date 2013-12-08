# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend
from dynamicgamedb.backend.model import Game, Platform, Relation
from dynamicgamedb.backend.database import db_session
from flask import request, jsonify, redirect, url_for
import dateutil.parser
import datetime
from sqlalchemy import desc

@backend.route('/api/games', methods=['POST', 'GET'])
def games():
    print "api games"
    if request.method == 'POST':
        search_term = str(request.form['search_term'])
        print "search_term_backend",search_term
        #games = Game.query.filter(Game.title.like(search_term)).all()
        games = (Game.query.filter(Game.title.contains(search_term)).all())
        #Game.query.filter(Game.title.like(title)).all()
        return jsonify({"games":[{"game_id":game.g_id,
                                  "game_title":game.title,
                                  "platform":game.platform.name,
                                  "platform_id":game.platform.p_id,
                                  "info":game.info,
                                  "picture":game.picture,
                                  "release_date":game.release_date.strftime("%Y-%m-%d"),
                                  "developer":game.developer,
                                  "publisher":game.publisher,
                                  "relations":game.relations} for game in games]})
    else:
        #relations = db_session.query(Relation).order_by(Relation.count)
        games = db_session.query(Game).order_by(Game.relations.desc())
        games = games[:9]
        return jsonify({"games":[{"game_id":game.g_id,
                                  "game_title":game.title,
                                  "platform":game.platform.name,
                                  "platform_id":game.platform.p_id,
                                  "info":game.info,
                                  "picture":game.picture,
                                  "release_date":game.release_date.strftime("%Y-%m-%d"),
                                  "developer":game.developer,
                                  "publisher":game.publisher,
                                  "relations":game.relations} for game in games]})        

@backend.route('/api/game/add', methods=['POST'])
@backend.user_required
def add_game():
    title = request.form['title']
    platform_id = str(request.form['platform_id'])
    games = Game.query.filter(Game.title.like(title)).all()
    exists = False
    for game in games:
        if game.title == title and str(game.platform_id) == platform_id:
            exists = True
    if not exists:
        platform = db_session.query(Platform).get(request.form['platform_id'])
        if platform == None:
            print "Platform doesn't exist"
            return jsonify({"error":"Platform doesn't exist"})
        game = Game(request.form['title'], platform)
        db_session.add(game)
        db_session.commit()
    else:
        print "Already existed"
        game = games[0]
    return jsonify({"game_id":game.g_id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "platform_id":game.platform.p_id,
                    "info":game.info,
                    "picture":game.picture,
                    "release_date":game.release_date.strftime("%Y-%m-%d"),
                    "developer":game.developer,
                    "publisher":game.publisher,
                    "relations":game.relations})

@backend.route('/api/game/<int:id>', methods=['GET'])
def game(id):
    game = db_session.query(Game).get(id)
    return jsonify({"game_id":game.g_id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "platform_id":game.platform.p_id,
                    "info":game.info,
                    "picture":game.picture,
                    "release_date":game.release_date.strftime("%Y-%m-%d"),
                    "developer":game.developer,
                    "publisher":game.publisher,
                    "relations":game.relations})

@backend.route('/api/game/<int:id>/edit', methods=['POST'])
def edit_game(id):
    game = db_session.query(Game).get(id)
    game.title = request.form['title']
    platform = db_session.query(Platform).get(request.form['platform_id'])
    game.platform = platform
    game.platform_id = platform.p_id
    game.picture = request.form['picture']
    game.info = request.form['info']
    game.release_date = dateutil.parser.parse(request.form['release_date'])
    game.developer = request.form['developer']
    game.publisher = request.form['publisher']
    db_session.commit()
    return jsonify({"game_id":game.g_id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "platform_id":game.platform.p_id,
                    "info":game.info,
                    "picture":game.picture,
                    "release_date":game.release_date.strftime("%Y-%m-%d"),
                    "developer":game.developer,
                    "publisher":game.publisher,
                    "relations":game.relations})
@backend.route('/api/game/<int:id>/relation', methods=['GET', 'POST'])
def game_relations(id):
    if request.method == 'GET':
        # All relations including this game
        relations = Relation.query.filter((Relation.game1_id==id)|(Relation.game2_id==id)).all()
        rs = [(r.game1_id, r.count) if not r.game1_id == id else (r.game2_id, r.count) for r in relations]
        # All games with either part of the relation except this game
        #games = db_session.query(Game).filter((Game.g_id!=id)&(Game.g_id.in_(map(lambda r:r.game1_id, relations))|Game.g_id.in_(map(lambda r:r.game2_id, relations))))
        games = db_session.query(Game).filter(Game.g_id.in_(map(lambda (r, c):r, rs)))
        rgs = zip((map(lambda (r,c):c, rs)),games)
        rgs = sorted(rgs,key=lambda rg: rg[0], reverse=True)
        return jsonify({"relatedgames":[{"game_id":game.g_id,
                            "game_title":game.title,
                            "platform":game.platform.name,
                            "platform_id":game.platform.p_id,
                            "info":game.info,
                            "picture":game.picture,
                            "release_date":game.release_date.strftime("%Y-%m-%d"),
                            "developer":game.developer,
                            "publisher":game.publisher,
                            "relations":game.relations,
                            "relation_count":c} for (c,game) in rgs]})
    else:
        if id == request.form['g_id']:
            return jsonify({"error":"Can not relate to self"})
        g1id = id if id < request.form['g_id'] else request.form['g_id']
        g2id = request.form['g_id'] if id < request.form['g_id'] else id
        g1 = db_session.query(Game).get(g1id)
        g2 = db_session.query(Game).get(g2id)
        if g1 == None:
            if g1id == id:
                return jsonify({"error":"Source id doesn't exist"})
            else:
                return jsonify({"error":"Target id doesn't exist"})
        if g2 == None:
            if g2id == id:
                return jsonify({"error":"Source id doesn't exist"})
            else:
                return jsonify({"error":"Target id doesn't exist"})
        #Target-game from users point of view
        game = db_session.query(Game).get(request.form['g_id'])
        #Always least id first
        relation = db_session.query(Relation).get((g1.g_id,g2.g_id))
        if relation == None:
            print "Relation was None"
            relation = Relation(g1,g2)
            db_session.add(relation)
        else:
            relation.count = relation.count + 1
        g1.relations = g1.relations + 1
        g2.relations = g2.relations + 1
        try:
            db_session.commit()
        except Exception, e:
            return "Failed"
        return jsonify({"game_id":game.g_id,
                        "game_title":game.title,
                        "platform":game.platform.name,
                        "platform_id":game.platform.p_id,
                        "info":game.info,
                        "picture":game.picture,
                        "release_date":game.release_date.strftime("%Y-%m-%d"),
                        "developer":game.developer,
                        "publisher":game.publisher,
                        "relations":game.relations,
                        "relation_count":relation.count})

@backend.route('/api/game/<int:source_id>/relation/<int:target_id>', methods=['GET'])
def game_relation(source_id, target_id):
    if source_id == target_id:
        return jsonify({"error":"Can not relate to self"})
    g1id = source_id if source_id < target_id else target_id
    g2id = target_id if source_id < target_id else source_id
    g1 = db_session.query(Game).get(g1id)
    g2 = db_session.query(Game).get(g2id)
    if g1 == None:
        if g1id == source_id:
            return jsonify({"error":"Source id doesn't exist"})
        else:
            return jsonify({"error":"Target id doesn't exist"})
    if g2 == None:
        if g2id == source_id:
            return jsonify({"error":"Source id doesn't exist"})
        else:
            return jsonify({"error":"Target id doesn't exist"})
    #Target-game from users point of view
    game = db_session.query(Game).get(target_id)
    relation = db_session.query(Relation).get((g1.g_id,g2.g_id))
    if relation == None:
        return jsonify({"game_id":game.g_id,
                        "game_title":game.title,
                        "platform":game.platform.name,
                        "platform_id":game.platform.p_id,
                        "info":game.info,
                        "picture":game.picture,
                        "release_date":game.release_date.strftime("%Y-%m-%d"),
                        "developer":game.developer,
                        "publisher":game.publisher,
                        "relations":game.relations,
                        "relation_count":0})
    return jsonify({"game_id":game.g_id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "platform_id":game.platform.p_id,
                    "info":game.info,
                    "picture":game.picture,
                    "release_date":game.release_date.strftime("%Y-%m-%d"),
                    "developer":game.developer,
                    "publisher":game.publisher,
                    "relations":game.relations,
                    "relation_count":relation.count})