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

#opdracht 1
CREATE TABLE comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    newsarticle_id INT NOT NULL,
    author VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (newsarticle_id) REFERENCES newsarticle(newsarticle_id),
);

#opdracht 3
def comments_article(conn, article_id):
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT author, content FROM comments WHERE newsarticle_id = %s",
        (article_id,)
    )

    comments = cursor.fetchall()
    cursor.close()

    return comments

@bp.route("/design1")
def design1():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM newsarticle")
    articles = cursor.fetchall()

    # 👇 NIEUW: comments per artikel ophalen
    comments_per_article = {}
    for article in articles:
        article_id = article["newsarticle_id"]
        comments_per_article[article_id] = comments_article(conn, article_id)

    cursor.close()
    conn.close()

    return render_template(
        "design1.html", articles=articles, comments_per_article=comments_per_article
    )

bp.route("/design1/<int:article_id>/comment", methods=["post"])
def add_comment(article_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    author = request.form["author"]
    content = request.form["content"]
    cursor.execute(
        "INSERT INTO comments (newsarticle_id, author, content) VALUES (%s, %s, %s)", (article_id, author, content)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("/design1"))

      
