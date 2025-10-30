from flask import render_template, request, redirect
from app.main import bp
from app.settings import DATABASE
import mysql.connector

def get_db_connection():
    """Connectie maken met mysql database"""
    return mysql.connector.connect(
        host=DATABASE["HOST"],
        user=DATABASE["USER"],
        password=DATABASE["PASSWORD"],
        database=DATABASE["NAME"],
        port=DATABASE["PORT"]
    )

@bp.route("/home")
def index():
    return render_template("base.html")

@bp.route("/info")
def informatie():
    return render_template("info.html")

@bp.route("/offerte", methods=["GET", "POST"])
def offerte():
    # Haalt data op van de form in offerte_aanvraag.html
    if request.method == "POST":
        naam = request.form["naam"]
        email = request.form["email"]
        organisatie = request.form("organisatie")
        omschrijving = request.form["omschrijving"]

        conn = get_db_connection() #verbinding maken met de database
        cursor = conn.cursor() 
        query = """
            INSERT INTO offerte_aanvragen (naam, email, organisatie, omschrijving)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (naam, email, organisatie, omschrijving))
        conn.commit() #slaat de ingevulde variable op in de database
        cursor.close() 
        conn.close() #sluit de verbinding met de database af

    return render_template("offerte_aanvraag.html")

