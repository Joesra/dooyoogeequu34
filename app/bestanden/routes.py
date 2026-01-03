from flask import render_template, request, redirect, flash
from app.bestanden import bp
from app.supabase.client import upload_file, get_files

@bp.route("/bestanden", methods=["GET", "POST"])
def upload_bestand():
    if request.method == "POST":
        file = request.files.get("bestand")

        if not file or file.filename == "":
            flash("Geen bestand geselecteerd", "error")
            return redirect("/bestanden")

        upload_file(file)
        flash("Bestand succesvol geüpload!", "success")
        return redirect("/bestanden")  #PRG 

    #GET: bestanden ophalen
    bestanden = get_files()
    return render_template("bestanden.html", bestanden=bestanden)