from flask import render_template, request, redirect
from app.main import bp
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

# @bp.route("/nieuws/<int:article_id>")
# def nieuws_article(article_id):
#     conn = get_db_connection()
#     try:
#         cursor = conn.cursor(dictionary=True)  # levert dicts in plaats van tuples
#         sql = "SELECT id, title, content, likes, DATE_FORMAT(publish_date, '%Y-%m-%d') AS publish_date FROM newsarticles WHERE id = %s"
#         cursor.execute(sql, (article_id,))
#         row = cursor.fetchone()
#         if row is None:
#             # 404 als artikel niet bestaat
#             abort(404)
#         # row is een dictionary, geef die door aan de template als 'newsarticle'
#         return render_template("design1.html", newsarticle=row)
#     finally:
#         cursor.close()
#         conn.close()