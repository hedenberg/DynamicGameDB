# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend
from dynamicgamedb.backend.model import Game, Platform, Relation, UniqueRelation
from dynamicgamedb.backend.database import db_session
from flask import request, jsonify, redirect, url_for, g, make_response, send_file
import dateutil.parser
import datetime
import sys
import mimetypes
from sqlalchemy import desc

#BACKEND_URL = 'http://localhost:8000/api'
BACKEND_URL = 'http://dynamicgamedb.herokuapp.com/api'

@backend.route('/api/games/', methods=['POST', 'GET'])
def games():
    print "api games"
    if request.method == 'POST':
        search_term = str(request.form['search_term'])
        print "search_term_backend",search_term
        try:
            games = (Game.query.filter(Game.title.contains(search_term)).all())
        except Exception, e:
            return backend.get_error_response(
                    message="Invalid search parameter.",
                    status_code=400)
        try:
            games2 = (Game.query.filter(Game.title.contains(search_term.title())).all())
        except Exception, e:
            return backend.get_error_response(
                    message="Invalid search parameter.",
                    status_code=400)
        for game in games2:
            exists = False
            for ga in games:
                if ga.g_id == game.g_id:
                    exists = True
            if not exists:
                games = games + [game]
        games = games[:11]
        print "games: ----- "
        for game in games:
            print "game :", game.title
        return jsonify({"games":[{"game_id":game.g_id,
                                  "game_title":game.title,
                                  "platform":game.platform.name,
                                  "platform_id":game.platform.p_id,
                                  "info":game.info,
                                  "picture":game.picture,
                                  "release_date":game.release_date.strftime("%Y-%m-%d"),
                                  "developer":game.developer,
                                  "publisher":game.publisher,
                                  "edited_by":game.edited_by,
                                  "relations":game.relations} for game in games]})
    else:
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
                                  "edited_by":game.edited_by,
                                  "relations":game.relations} for game in games]})        

@backend.route('/api/game/add/', methods=['POST'])
@backend.user_required
def add_game():
    title = request.form['title']
    platform_id = str(request.form['platform_id'])
    games = Game.query.filter(Game.title.like(title)).all()
    exists = False
    for game in games:
        print "games like ", title, game.title
        if game.title == title and str(game.platform_id) == platform_id:
            exists = True
    if exists:
        return backend.get_error_response(
                message="A game with that title and platform already exists.",
                status_code=400)
    platform = db_session.query(Platform).get(request.form['platform_id'])
    if platform == None:
        print "Platform doesn't exist"
        return backend.get_error_response(
            message="Platform ID invalid.",
            status_code=401)
    game = Game(request.form['title'], platform)
    game.edited_by = g.backend_user.email
    db_session.add(game)
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
                    "edited_by":game.edited_by,
                    "relations":game.relations})

@backend.route('/api/game/<int:id>/', methods=['GET'])
def game(id):
    game = db_session.query(Game).get(id)
    if not game:
        return backend.get_error_response(
            message="Game ID invalid.",
            status_code=400)
    return jsonify({"game_id":game.g_id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "platform_id":game.platform.p_id,
                    "info":game.info,
                    "picture":game.picture,
                    "release_date":game.release_date.strftime("%Y-%m-%d"),
                    "developer":game.developer,
                    "publisher":game.publisher,
                    "edited_by":game.edited_by,
                    "relations":game.relations})

@backend.route('/api/game/<int:id>/edit/', methods=['POST'])
@backend.user_required
def edit_game(id):
    game = db_session.query(Game).get(id)
    game.title = request.form['title']
    platform = db_session.query(Platform).get(request.form['platform_id'])
    if not platform:
        return backend.get_error_response(
            message="Platform ID invalid.",
            status_code=400)
    game.platform = platform
    game.platform_id = platform.p_id
    games = Game.query.filter(Game.title.like(game.title)).all()
    exists = False
    for ga in games:
        print "game platform:", game.platform_id, " ", game.g_id
        print "ga platform:", ga.platform_id, " ", game.g_id
        if ga.g_id != game.g_id and game.title == ga.title and str(game.platform_id) == str(ga.platform_id):
            exists = True
    if exists:
        return backend.get_error_response(
                message="A game with that title and platform already exists.",
                status_code=400)
    game.info = request.form['info']
    game.release_date = dateutil.parser.parse(request.form['release_date'])
    game.developer = request.form['developer']
    game.publisher = request.form['publisher']
    game.edited_by = g.backend_user.email
    try:
        db_session.commit()
    except Exception, e:
        return backend.get_error_response(
            message="Info text too long.",
            status_code=400)
    return jsonify({"game_id":game.g_id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "platform_id":game.platform.p_id,
                    "info":game.info,
                    "picture":game.picture,
                    "release_date":game.release_date.strftime("%Y-%m-%d"),
                    "developer":game.developer,
                    "publisher":game.publisher,
                    "edited_by":game.edited_by,
                    "relations":game.relations})

@backend.route('/api/game/<int:id>/edit_image/', methods=['POST'])
@backend.user_required
def edit_image(id):
    print "Edit image backend"
    image = request.files['image']
    #fn = secure_filename(f.filename)
    #f_size = sys.getsizeof(f) 
    # Makea da fix @ adding to database lol.

    game = db_session.query(Game).get(id)
    game.image = image.read()
    game.image_name = image.filename
    game.image_size = sys.getsizeof(image)
    game.picture = BACKEND_URL+'/game/'+str(id)+'/image/'
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
                    "edited_by":game.edited_by,
                    "relations":game.relations})

@backend.route('/api/game/<int:id>/image/', methods=['GET'])
def game_image(id):
    game = db_session.query(Game).get(id)
    response = make_response()
    response.headers['Pragma'] = 'public'
    response.headers['Content-Type'] = mimetypes.guess_type(game.image_name)[0]
    response.headers['Content-Transfer-Encoding'] = 'binary'
    response.headers['Content-Disposition'] = 'filename=%s' % game.image_name
    response.headers['Content-Length'] = game.image_size
    response.data = game.image
    return response

@backend.route('/api/game/<int:id>/relation/', methods=['GET'])
def game_relations(id):
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
                        "edited_by":game.edited_by,
                        "relations":game.relations,
                        "relation_count":c} for (c,game) in rgs]})

@backend.route('/api/game/<int:id>/relation/', methods=['POST'])
@backend.user_required
def add_game_relations(id):
    if id == request.form['g_id']:
        return jsonify({"error":"Can not relate to self"})
    g1id = id if id < int(request.form['g_id']) else request.form['g_id']
    print "low id: ", g1id
    g2id = request.form['g_id'] if id < int(request.form['g_id']) else id
    print "high id: ", g2id
    g1 = db_session.query(Game).get(g1id)
    g2 = db_session.query(Game).get(g2id)
    if g1 == None:
        if g1id == id:
            return backend.get_error_response(
                message="Source id doesn't exist",
                status_code=404)
        else:
            return backend.get_error_response(
                message="Target id doesn't exist",
                status_code=404)
    if g2 == None:
        if g2id == id:
            return backend.get_error_response(
                message="Source id doesn't exist",
                status_code=404)
        else:
            return backend.get_error_response(
                message="Target id doesn't exist",
                status_code=404)

    uniqueRelation = db_session.query(UniqueRelation).get((g.backend_user.openid, g1.g_id, g2.g_id))
    print "unik relation", uniqueRelation

    if uniqueRelation != None:
        print "Not unique relation"
        return backend.get_error_response(message="You have already done this relation earlier", status_code=404)
    else:
        #Target-game from users point of view
        game = db_session.query(Game).get(request.form['g_id'])
        #Always least id first
        relation = db_session.query(Relation).get((g1.g_id,g2.g_id))
        if relation == None:
            print "Relation was None"
            relation = Relation(g1,g2)
            db_session.add(relation)
            uniqueRelation = UniqueRelation(g.backend_user.openid, g1.g_id, g2.g_id)
            db_session.add(uniqueRelation)
        else:
            print "Relation already existed"
            relation.count = relation.count + 1
            uniqueRelation =UniqueRelation(g.backend_user.openid, relation.game1_id, relation.game2_id)
            db_session.add(uniqueRelation)
        print "relation: ", relation
        print "relations: ", relation.count
        g1.relations = g1.relations + 1
        g2.relations = g2.relations + 1
    try:
        db_session.commit()
    except Exception, e:
        return backend.get_error_response(
                message="Commit has failed.",
                status_code=404)
    return jsonify({"game_id":game.g_id,
                    "game_title":game.title,
                    "platform":game.platform.name,
                    "platform_id":game.platform.p_id,
                    "info":game.info,
                    "picture":game.picture,
                    "release_date":game.release_date.strftime("%Y-%m-%d"),
                    "developer":game.developer,
                    "publisher":game.publisher,
                    "edited_by":game.edited_by,
                    "relations":game.relations,
                    "relation_count":relation.count})

@backend.route('/api/game/<int:source_id>/relation/<int:target_id>/', methods=['GET'])
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
                        "edited_by":game.edited_by,
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
                    "edited_by":game.edited_by,
                    "relations":game.relations,
                    "relation_count":relation.count})