from dateutil.parser import isoparse

from flask import abort, redirect, render_template, request, url_for

from app.events import bp, create_event, get_event, get_events, update_event
from flask import render_template, request, redirect, session, jsonify, current_app
from app.settings import DATABASE
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

def get_db_connection():
    """Connectie maken met mysql database"""
    return mysql.connector.connect(
        host=DATABASE["HOST"],
        user=DATABASE["USER"],
        password=DATABASE["PASSWORD"],
        database=DATABASE["NAME"],
        port=DATABASE["PORT"]
    )

@bp.route("/")
def index():
    """returns the events index page"""
    events = get_events()
    return render_template("events/index.html", events=events)

@bp.route("/nieuws")
def nieuws():
    return render_template("nieuws.html")

@bp.route("/categorie_design")
def categorie_design():
    return render_template("categorie_design.html")

@bp.route("/artikel_privacy1")
def artikel_privacy1():
    return render_template("artikel_privacy1.html")

@bp.route("/design1/<int:article_id>")
def design1 (article_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT newsarticle_id, title, likes FROM newsarticle WHERE newsarticle_id = %s", (article_id,))
    newsarticle = cursor.fetchone()   

    cursor.close()
    conn.close()

    if newsarticle is None:
        return "Artikel niet gevonden", 404
    
    liked_list = session.get("liked_articles", [])
    is_liked = article_id in liked_list


    return render_template("design1.html", newsarticle=newsarticle, is_liked=is_liked,)
        

@bp.route("/design1/<int:article_id>/like", methods=["POST"])
def toggle_like(article_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) 
    try:
        #gelikte artikelen worden in liked_set opgeslagen
        liked_set = set(session.get("liked_articles", []))

        # if statement voor als de gebruiker al een artikel heeft geliked
        if article_id in liked_set:
            cursor.execute("UPDATE newsarticle SET likes = GREATEST(likes - 1, 0) WHERE newsarticle_id = %s",(article_id,))
            liked_set.discard(article_id)
            liked = False
        else:
            # else stament voor als iemand nog niet heeft geliked
            cursor.execute("UPDATE newsarticle SET likes = likes + 1 WHERE newsarticle_id = %s",(article_id,))
            liked_set.add(article_id)
            liked = True

        conn.commit()

        # likes worden opgehaald van een specifiek rij met row
        cursor.execute("SELECT likes FROM newsarticle WHERE newsarticle_id = %s",(article_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Artikel niet gevonden"}), 404
        
        #de variable new_likes verandert alle likes in een int en ophaalt informatie op met row
        new_likes = int(row.get("likes"))

        #liked_articles worden verandert in een list 
        session["liked_articles"] = list(liked_set)

        return jsonify({"likes": new_likes, "liked": liked})

    except Exception:
        current_app.logger.exception("Fout bij toggle_like")
        conn.rollback()
        return jsonify({"error": "Serverfout"}), 500
    finally:
        cursor.close()
      
@bp.route("/artikel_systeem1")
def artikel_systeem1():
    return render_template("artikel_systeem1.html")

@bp.route("/artikel_categorie_design1")  
def artikel_categorie_design1():
    return render_template("artikel_categorie_design1.html")

@bp.route("/artikel_categorie_design2")  
def artikel_categorie_design2():
    return render_template("artikel_categorie_design2.html")

@bp.route("/artikel_categorie_design3")  
def artikel_categorie_design3():
    return render_template("artikel_categorie_design3.html")

@bp.route("/view/<int:event_id>")
def view(event_id):
    event = get_event(event_id) or abort(404)
    event["eventDate"] = isoparse(event["eventDate"])
    return render_template("events/view.html", event=event)

@bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":

        description = request.form["description"]
        date = request.form["date"]
        event_id = create_event(description, date)

        if not event_id:
            return render_template("events/create.html", error="Event kon niet worden aangemaakt, zorg dat de datum in de toekomst ligt.")
        return redirect(url_for("events.view", event_id=event_id))

    return render_template("events/create.html")


@bp.route("/edit/<int:event_id>", methods=["GET", "POST"])
def edit(event_id):
    if request.method == "POST":

        description = request.form["description"]
        date = request.form["date"]
        update_event(event_id, description, date)

        return redirect(url_for("events.view", event_id=event_id))

    event = get_event(event_id) or abort(404)
    event["eventDate"] = isoparse(event["eventDate"])
    return render_template("events/edit.html", event=event)
