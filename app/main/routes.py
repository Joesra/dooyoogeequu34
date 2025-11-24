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

@bp.route("/registreer", methods=["GET", "POST"])
def registreer():
    if request.method == "POST":
        voornaam = request.form["voornaam"]
        achternaam = request.form["achternaam"]
        email = request.form["email"]
        telefoonnummer = request.form["telefoonnummer"]
        gebruikersnaam = request.form["gebruikersnaam"]
        wachtwoord = request.form["wachtwoord"]
        wachtwoord_confirm = request.form.get("wachtwoord_confirm")

        if wachtwoord_confirm is not None and wachtwoord != wachtwoord_confirm:
            return render_template("registreer.html", error="Wachtwoorden komen niet overeen.")

        conn = get_db_connection() 
        cursor = conn.cursor() 

        hashed = generate_password_hash(wachtwoord)

        query = """
            INSERT INTO user(Voornaam, achternaam, email, Telefoonnummer, gebruikersnaam, wachtwoord)
            VALUES (%s, %s, %s, %s,  %s, %s)
        """
        cursor.execute(query, (voornaam, achternaam, email, telefoonnummer, gebruikersnaam, hashed))
        conn.commit() 
        cursor.close() 
        conn.close() 

        return redirect("/login")

    return render_template("registreer.html")

@bp.route("/login", methods={ 'GET', 'POST' })
def login():
    if request.method == "POST":
        gebruikersnaam = request.form["gebruikersnaam"]
        wachtwoord = request.form["wachtwoord"]

        conn = get_db_connection() 
        cursor = conn.cursor() 

        query = """
            SELECT wachtwoord FROM user WHERE gebruikersnaam = %s
        """
        cursor.execute(query, (gebruikersnaam,))
        row = cursor.fetchone()
        user = None
        if row:
            # cursor.fetchone() geeft meestal een tuple; wachtwoord staat in eerste kolom
            stored_hash = row[0]
            if check_password_hash(stored_hash, wachtwoord):
                user = True
        cursor.close() 
        conn.close() 

        if user:
            return redirect("/home")
        else:
            # toon foutmelding zonder flash door de template opnieuw te renderen
            return render_template("login.html", error="Onjuiste gebruikersnaam of wachtwoord.")
    return render_template("login.html")