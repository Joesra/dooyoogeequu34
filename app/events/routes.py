from dateutil.parser import isoparse
from flask import abort, redirect, render_template, request, url_for
from app.events import bp, create_event, get_event, get_events, update_event
from flask import render_template, request, redirect, session, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint
from app.database import get_db_connection


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

@bp.route("/design1")
def design1():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM newsarticle")
        articles = cursor.fetchall()

        comments_per_article = {}
        for article in articles:
            article_id = article["newsarticle_id"]
            comments_per_article[article_id] = comments_article(conn, article_id)

        cursor.close()
        conn.close()

        return render_template(
            "design1.html", articles=articles, comments_per_article=comments_per_article
        )
    except Exception as e:
        # Log the exception and render the page with a helpful error message
        current_app.logger.exception("Fout bij ophalen van artikelen uit de database")
        # No fallback articles: show empty lists so we keep behavior deterministic
        return render_template("design1.html", articles=[], comments_per_article={}, db_error=True)


def comments_article(conn, article_id):
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT author, content FROM comments WHERE newsarticle_id = %s",
        (article_id,)
    )

    comments = cursor.fetchall()
    cursor.close()

    return comments

@bp.route("/design1/<int:article_id>/comment", methods=["POST"])
def add_comment(article_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        author = request.form["author"]
        content = request.form["content"]

        cursor.execute(
            """
            INSERT INTO comments (newsarticle_id, author, content)
            VALUES (%s, %s, %s)
            """,
            (article_id, author, content)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("events.design1"))
    except Exception:
        current_app.logger.exception("Fout bij toevoegen van comment")
        # Redirect back to the article list with an error flag
        return redirect(url_for("events.design1") + "?error=comment")
    

@bp.route("/design1/<int:article_id>/like", methods=["POST"])
def toggle_like(article_id):
    try:
        conn = get_db_connection()
    except Exception:
        current_app.logger.exception("Fout bij verbinden met database voor likes")
        return jsonify({"error": "Database niet bereikbaar"}), 500

    service = LikeService(conn)

    try:
        result = service.toggle_like(article_id, session)
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except Exception:
        current_app.logger.exception("Fout bij toggle_like")
        return jsonify({"error": "Serverfout"}), 500

    finally:
        conn.close()

class LikeService:
    def __init__(self, conn):
        self.conn = conn

    def toggle_like(self, article_id, session):
        liked_set = set(session.get("liked_articles", []))
        cursor = self.conn.cursor(dictionary=True)
        try:
            if article_id in liked_set:
                cursor.execute('UPDATE newsarticle SET likes = GREATEST(likes - 1, 0) WHERE newsarticle_id = %s', (article_id,))
                liked_set.remove(article_id)
                liked = False
            else:
                cursor.execute('UPDATE newsarticle SET likes = likes + 1 WHERE newsarticle_id = %s', (article_id,))
                liked_set.add(article_id)
                liked = True
            self.conn.commit()
            cursor.execute('SELECT likes FROM newsarticle WHERE newsarticle_id = %s', (article_id,))
            row = cursor.fetchone()
            if row is None:
                raise ValueError('artikel niet gevonden')
            session["liked_articles"] = list(liked_set)
            return {
                'liked': liked,
                'likes': row['likes']
            }
        except Exception as e:
            self.conn.rollback()
            raise e
        
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

