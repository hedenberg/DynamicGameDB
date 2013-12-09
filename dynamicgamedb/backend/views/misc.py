# -*- coding: utf-8 -*-
from dynamicgamedb.backend import backend, oid
from dynamicgamedb.backend.model import Game, Platform, User, Relation, Client
from dynamicgamedb.backend.database import db_session

from flask import Response, request, jsonify, redirect, url_for, session, g
import dateutil.parser


@backend.route("/init/")
def init_server():
    # -- Clients --
    c1 = Client(1337, "you no take candle")
    db_session.add(c1)

    #**********platforms************
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
    #**********games************
    game1 = Game("Battlefield 3",p1)
    game1.developer = "DICE"
    game1.info = "Battlefield 3 is a First-Person Shooter (FPS) that is designed to attack your senses, delivering a visceral combat experience like no other FPS before it. Sequel to 2005's Battlefield 2, Battlefield 3 utilizes the updated Frostbite 2 game engine, which allows for advanced destruction, sound, and graphics as well as a focus on dense in-game urban settings."
    game1.picture = "http://upload.wikimedia.org/wikipedia/en/6/69/Battlefield_3_Game_Cover.jpg"
    game1.publisher = "EA"
    game1.release_date =  dateutil.parser.parse("2011-10-25")
    game1.relations = 3
    game1.edited_by = "dynamic@game.db"
    db_session.add(game1)

    game2 = Game("ARMA 3",p1)
    game2.developer = "Bohemia Interactive"
    game2.info = "After years of intense warfare against Eastern armies, Europe has become the last stand for the battered NATO forces. On the verge of being driven into the sea, NATO command embarks upon a most desperate measure. In the hope of seizing what seems to be a well-guarded military secret, Operation Magnitude is launched. A small group of Special Forces and Researchers are sent to a Mediterranean island deep behind enemy lines."
    game2.picture = "http://www.blogcdn.com/www.joystiq.com/media/2013/03/arma-3-cover.jpg"
    game2.publisher = "Bohemia Interactive"
    game2.release_date =  dateutil.parser.parse("2013-09-12")
    game2.relations = 2
    game2.edited_by = "dynamic@game.db"
    db_session.add(game2)

    game3 = Game("Grand Theft Auto: Vice City",p1)
    game3.developer = "Rockstar North"
    game3.info = "SOMETEXT"
    game3.picture = "http://upload.wikimedia.org/wikipedia/en/c/ce/Vice-city-cover.jpg"
    game3.publisher = "Rockstar"
    game3.release_date =  dateutil.parser.parse("2002-10-27")
    game3.relations = 2
    game3.edited_by = "dynamic@game.db"
    db_session.add(game3)

    game4 = Game("Battlefield 4",p1)
    game4.developer = "DICE"
    game4.info = "Battlefield 4 is the genre-defining action blockbuster made from moments that blur the line between game and glory. Fueled by the next-generation power and fidelity of Frostbite 3, Battlefield 4 provides a visceral, dramatic experience unlike any other."
    game4.picture = "http://upload.wikimedia.org/wikipedia/en/e/ed/Battlefield_4.jpg"
    game4.publisher = "EA"
    game4.release_date =  dateutil.parser.parse("2013-10-29")
    game4.relations = 2
    game4.edited_by = "dynamic@game.db"
    db_session.add(game4)

    game5 = Game("Minecraft",p1)
    game5.developer = "Mojang"
    game5.info = "Minecraft is a sandbox indie game originally created by Swedish programmer Markus \"Notch\" Persson and later developed and published by Mojang. It was publicly released for the PC on May 17, 2009, as a developmental alpha version and, after gradual updates, was published as a full release version on November 18, 2011."
    game5.picture = "http://pcgamerparadise.com/images/Minecraft_cover.jpg"
    game5.publisher = "Mojang"
    game5.release_date =  dateutil.parser.parse("2009-05-17")
    game5.relations = 2
    game5.edited_by = "dynamic@game.db"
    db_session.add(game5)

    game6 = Game("Terraria",p1)
    game6.developer = "Re-Logic"
    game6.info = "Terraria is an open-ended sandbox 2D game with gameplay revolved around exploration, building, and action. The game has a 2D sprite tile-based graphical style reminiscent of the 16-bit sprites found on the SNES. The game is noted for its classic exploration-adventure style of play, similar to titles such as Metroid and Minecraft."
    game6.picture = "http://www.pageofreviews.com/wp-content/uploads/terraria1.png"
    game6.publisher = "Re-Logic"
    game6.release_date =  dateutil.parser.parse("2011-05-16")
    game6.relations = 1
    game6.edited_by = "dynamic@game.db"
    db_session.add(game6)

    game7 = Game("Ace of Spades",p1)
    game7.developer = "Jagex Game Studio"
    game7.info = "Ace of Spades is a sandbox building and FPS game, originally developed by Ben Aksoy for the PC and released in 2011 as a beta version. In late 2012, RuneScape developer, Jagex took over development of the game, making it payware on Steam and updating its gameplay."
    game7.picture = "http://media.ign.com/games/image/object/106/106949/Ace-Of-Spades_PCDL.jpg"
    game7.publisher = "Jagex Game Studio"
    game7.release_date =  dateutil.parser.parse("2012-12-12")
    game7.relations = 2
    game7.edited_by = "dynamic@game.db"
    db_session.add(game7)

    game8 = Game("Fallout 2",p1)
    game8.developer = ""
    game8.info = ""
    game8.picture = "http://pics.mobygames.com/images/covers/large/1124464345-00.jpg"
    game8.publisher = ""
    game8.release_date =  dateutil.parser.parse("2013-12-29")
    game8.edited_by = "dynamic@game.db"
    db_session.add(game8)

    game9 = Game("Dishonored",p1)
    game9.developer = "Arkane Studios"
    game9.info = ""
    game9.picture = "http://i.imgur.com/CMiXt.jpg"
    game9.publisher = "Bethesda Softworks"
    game9.release_date =  dateutil.parser.parse("2012-10-09")
    game9.relations = 1
    game9.edited_by = "dynamic@game.db"
    db_session.add(game9)

    game10 = Game("Saints Row IV",p1)
    game10.developer = "Volition Inc"
    game10.info = ""
    game10.picture = "http://fronttowardsgamer.com/wp-content/uploads/2013/05/srivbox.jpg"
    game10.publisher = "Deep Silver"
    game10.release_date =  dateutil.parser.parse("2013-08-20")
    game10.relations = 1
    game10.edited_by = "dynamic@game.db"
    db_session.add(game10)

    game11 = Game("Prototype 2",p1)
    game11.developer = "Radical Entertainment"
    game11.info = "SOMETEXT"
    game11.picture = "http://www.yellmagazine.com/wp-content/uploads/2012/05/prototype-2-cover.jpg"
    game11.publisher = "Activision"
    game11.release_date =  dateutil.parser.parse("2012-04-24")
    game11.relations = 2
    game11.edited_by = "dynamic@game.db"
    db_session.add(game11)


    #***********relation*********************
    rel = Relation(game1, game2)    #BF3 -> ARMA 3
    db_session.add(rel)
    rel = Relation(game1, game4)    #BF3 -> BF4
    db_session.add(rel)
    rel = Relation(game2, game4)    #BF4 -> ARMA 3
    db_session.add(rel)
    rel = Relation(game1, game7)    #BF3 -> Ace of spades
    db_session.add(rel)
    rel = Relation(game5, game7)    #Minecraft -> Ace of spades
    db_session.add(rel)
    rel = Relation(game5, game6)    #Minecraft -> Terraria
    db_session.add(rel)
    rel = Relation(game3, game11)    #GTA:Vice city -> prototype 2
    db_session.add(rel)
    rel = Relation(game3, game10)    #GTA:Vice city -> Saints row
    db_session.add(rel)
    rel = Relation(game11, game9)    #prototype 2 -> Dishonored
    db_session.add(rel)

    db_session.commit()
    return redirect(url_for('backend.games'))
