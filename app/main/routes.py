from flask import render_template

from app.main import bp


@bp.route("/home")
def index():
    return render_template("base.html")

@bp.route("/info")
def informatie():
    return render_template("info.html")

@bp.route("/offerte")
def offerte():
    return render_template("offerte_aanvraag.html")