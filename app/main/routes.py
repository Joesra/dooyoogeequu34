from flask import render_template, redirect, request, flash
from app.main import bp
from app.settings import DATABASE
import mysql.connector
from app.contact_model import ContactAanvraag #maakt connectie met contact_model.py, daar gebeurt alle magie

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

@bp.route("/nieuws")        
def nieuws():
    return render_template("nieuws.html")

@bp.route("/")
def home():
    return render_template("index.html")


@bp.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        aanvraag = ContactAanvraag(
            naam=request.form["naam"],
            email=request.form["email"],
            onderwerp=request.form["onderwerp"],
            bericht=request.form["bericht"]
        )
        aanvraag.opslaan()  #slaat de aanvraag op in de database

        flash(
            "Bedankt voor je vraag, we zullen het zo spoedig beantwoorden!",
            "success"
        ) #support_aanvraag.html

        return redirect("/contact")  #stuurt gebruiker terug naar contactpagina

    return render_template("support_aanvraag.html")

@bp.route("/admin/contact")
def admin_contact():
    #haalt alle open contactaanvragen op
    aanvragen = ContactAanvraag.get_open_vragen()
    return render_template("dev.html", aanvragen=aanvragen)

@bp.route("/admin")
def home():
    return render_template("admin.html")

@bp.route("/admin/contact/<int:id>")
def contact_detail(id):
    aanvraag = ContactAanvraag.get_by_id(id)
    return render_template("contact_beantwoorden.html", aanvraag=aanvraag)

@bp.route("/contact/beantwoord/<int:id>", methods=["POST"])
def beantwoord_contact(id):
    antwoord = request.form["antwoord"]

    #slaat het antwoord op bij de juiste aanvraag
    ContactAanvraag.beantwoord(id, antwoord)

    #redirect naar admin overzicht (PRG pattern)
    return redirect("/admin/contact")

@bp.route("/services")
def services():
    return render_template("services.html")

 #test        
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

@bp.route("/design1/<int:article_id>")
def design1(article_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT id, title, likes FROM newsarticle WHERE id = %s", (article_id,))
    newsarticle = cursor.fetchone()

    cursor.close()
    conn.close()

    if newsarticle is None:
        return "Artikel niet gevonden", 404

    return render_template("design1.html", newsarticle=newsarticle)

@bp.route("/incidenten")
def incidenten():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            i.incidents_id,
            i.incident_subject,
            i.incident_category,
            i.incident_message,
            i.incident_date,
            i.incident_priority,
            c.firstname,
            c.lastname
        FROM incidents i
        JOIN customer c ON i.Customer_customer_id = c.customer_id
        ORDER BY i.incident_date DESC
    """
    cursor.execute(query)
    incidenten = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("incidenten.html", incidenten=incidenten)

@bp.route("/nieuwe_incident")
def nieuwe_incident():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM incident_categories"
    
    return render_template("nieuwe_incident.html")

