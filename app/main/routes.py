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

@bp.route("/")
def home():
    return render_template("index.html")

@bp.route("/contact", methods=["GET", "POST"])
def contact():
    # Haalt data op van de form in support_aanvraag.html
    if request.method == "POST":
        naam = request.form["naam"]
        email = request.form["email"]
        onderwerp = request.form["onderwerp"]
        bericht = request.form["bericht"]

        conn = get_db_connection() #verbinding maken met de database
        cursor = conn.cursor() 

        #query om de aanvraag op te slaan
        query = """
            INSERT INTO contact_aanvragen (naam, email, onderwerp, bericht)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (naam, email, onderwerp, bericht))
        conn.commit() #slaat de ingevulde variable op in de database
        cursor.close() 
        conn.close() #sluit de verbinding met de database af

        return redirect("/contact")  #blijft op dezelfde pagina voor nu, later naar iets van bedankt voor de aanvraag

    return render_template("support_aanvraag.html")

@bp.route("/services")
def services():
    return render_template("services.html")

 #test        