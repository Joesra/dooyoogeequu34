from flask import render_template, redirect, request, flash
from app.main import bp
from app.contact_model import ContactAanvraag #maakt connectie met contact_model.py, daar gebeurt alle magie
from flask import url_for
from app.database import get_db_connection
import re
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from app.supabase.client import get_files


@bp.route("/")
def index():
    if "user_id" not in session:
        return redirect("/login")

    bestanden = get_files()

    bestanden = [
        b for b in bestanden if b["datum"] is not None
    ]

    #sorteer nieuwste eerst
    bestanden = sorted(
        bestanden,
        key=lambda b: b["datum"],
        reverse=True
    )

    recente_bestanden = bestanden[:5]

    return render_template(
        "base.html",
        recente_bestanden=recente_bestanden
    )

@bp.route("/info")
def informatie():
    return render_template("info.html")

@bp.route("/nieuws")        
def nieuws():
    return render_template("nieuws.html")

# @bp.route("/")
# def home():
#     return render_template("index.html")


@bp.route("/contact", methods=["GET", "POST"])
def contact():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        aanvraag = ContactAanvraag(
            naam=request.form["naam"],
            email=request.form["email"],
            onderwerp=request.form["onderwerp"],
            bericht=request.form["bericht"],
            user_id=session["user_id"]
        )
        aanvraag.opslaan() #slaat de aanvraag op in de database

        flash(
            "Bedankt voor je vraag, we zullen het zo spoedig beantwoorden!",
            "success"
        )
        return redirect("/mijn-tickets") #stuurt gebruiker terug naar contactpagina

    return render_template("support_aanvraag.html")

@bp.route("/admin/contact")
def admin_contact():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM contact_aanvragen ORDER BY id DESC"
    )
    aanvragen = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("dev.html", aanvragen=aanvragen)

@bp.route("/admin/contact/<int:id>", methods=["GET", "POST"])
def admin_contact_detail(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        antwoord = request.form["antwoord"]
        status = request.form["status"]

        cursor.execute(
            """
            UPDATE contact_aanvragen
            SET antwoord = %s, status = %s
            WHERE id = %s
            """,
            (antwoord, status, id)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return redirect("/admin/contact")

    cursor.execute(
        "SELECT * FROM contact_aanvragen WHERE id = %s",
        (id,)
    )
    aanvraag = cursor.fetchone()

    cursor.close()
    conn.close()

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


def is_overheid_email(email):
    return email.lower().endswith("@amsterdam.nl") #checkt of email eindigt met @amsterdam

def is_sterk_wachtwoord(wachtwoord):
    if len(wachtwoord) < 8: #wachtwoord lengte langer dan 8
        return False
        #re voor regex
    if not re.search(r"[A-Z]", wachtwoord): #moet een hoofdletter bevatten
        return False

    if not re.search(r"[0-9]", wachtwoord): #moet een cijfer van 1-9 bevatten
        return False

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", wachtwoord): #moet een teken bevatten
        return False

    return True

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
        wachtwoord_confirm = request.form["wachtwoord_confirm"]

        if not is_overheid_email(email):
            return render_template(
                "registreer.html",
                error="Alleen e-mailadressen met @amsterdam.nl zijn toegestaan."
            )

        if wachtwoord != wachtwoord_confirm:
            return render_template(
                "registreer.html",
                error="Wachtwoorden komen niet overeen."
            )

        if not is_sterk_wachtwoord(wachtwoord):
            return render_template(
                "registreer.html",
                error=(
                    "Wachtwoord moet minimaal 8 tekens bevatten, "
                    "1 hoofdletter, 1 cijfer en 1 speciaal teken."
                )
            )

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id FROM users WHERE gebruikersnaam = %s", #checkt of gebruikresnaam al bestaat 
            (gebruikersnaam,)
        )
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return render_template(
                "registreer.html",
                error="Gebruikersnaam bestaat al."
            )

        hashed_password = generate_password_hash(wachtwoord)

        cursor.execute( #slaat gebruiker op in de db
            """
            INSERT INTO users
            (voornaam, achternaam, email, telefoonnummer, gebruikersnaam, wachtwoord)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (voornaam, achternaam, email, telefoonnummer, gebruikersnaam, hashed_password)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect("/login")

    return render_template("registreer.html")

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        gebruikersnaam = request.form["gebruikersnaam"]
        wachtwoord = request.form["wachtwoord"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, wachtwoord FROM users WHERE gebruikersnaam = %s",
            (gebruikersnaam,)
        )
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        if row and check_password_hash(row[1], wachtwoord):
            session["user_id"] = row[0]
            session["gebruikersnaam"] = gebruikersnaam
            return redirect(url_for("main.index"))

        return render_template("login.html", error="Onjuiste gebruikersnaam of wachtwoord.")

    return render_template("login.html")

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

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

@bp.route("/mijn-tickets")
def mijn_tickets():
    if "user_id" not in session:
        return redirect("/login")

    tickets = ContactAanvraag.get_by_user(session["user_id"])
    return render_template("mijn_tickets.html", tickets=tickets)
