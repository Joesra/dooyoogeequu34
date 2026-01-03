from flask import (
    render_template,
    request,
    redirect,
    url_for,
    abort,
    jsonify,
    session,
    current_app,
)
from dateutil.parser import isoparse

from app.events import bp
from app.db import execute_query
from app.events import create_event, get_event, get_events, update_event


# ------------------------
# PAGINA'S
# ------------------------

@bp.route("/")
def index():
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

@bp.route("/artikel_systeem1")
def artikel_systeem1():
    return render_template("artikel_systeem1.html")


# ------------------------
# NIEUWS / COMMENTS
# ------------------------

@bp.route("/design1")
def design1():
    articles = execute_query("SELECT * FROM newsarticle")

    comments_per_article = {}
    for article in articles:
        article_id = article["newsarticle_id"]
        comments_per_article[article_id] = execute_query(
            "SELECT author, content FROM comments WHERE newsarticle_id = %s",
            (article_id,)
        )

    return render_template(
        "design1.html",
        articles=articles,
        comments_per_article=comments_per_article,
    )


@bp.route("/design1/<int:article_id>/comment", methods=["POST"])
def add_comment(article_id):
    execute_query(
        """
        INSERT INTO comments (newsarticle_id, author, content)
        VALUES (%s, %s, %s)
        """,
        (
            article_id,
            request.form["author"],
            request.form["content"],
        ),
    )

    return redirect(url_for("events.design1"))


# ------------------------
# LIKES
# ------------------------

@bp.route("/design1/<int:article_id>/like", methods=["POST"])
def toggle_like(article_id):
    liked_set = set(session.get("liked_articles", []))

    if article_id in liked_set:
        execute_query(
            """
            UPDATE newsarticle
            SET likes = GREATEST(likes - 1, 0)
            WHERE newsarticle_id = %s
            """,
            (article_id,),
        )
        liked_set.remove(article_id)
        liked = False
    else:
        execute_query(
            """
            UPDATE newsarticle
            SET likes = likes + 1
            WHERE newsarticle_id = %s
            """,
            (article_id,),
        )
        liked_set.add(article_id)
        liked = True

    row = execute_query(
        "SELECT likes FROM newsarticle WHERE newsarticle_id = %s",
        (article_id,),
    )

    if not row:
        return jsonify({"error": "Artikel niet gevonden"}), 404

    session["liked_articles"] = list(liked_set)

    return jsonify(
        {
            "liked": liked,
            "likes": row[0]["likes"],
        }
    )


# ------------------------
# EVENTS (BESTAAND)
# ------------------------

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
            return render_template(
                "events/create.html",
                error="Event kon niet worden aangemaakt, zorg dat de datum in de toekomst ligt.",
            )

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
