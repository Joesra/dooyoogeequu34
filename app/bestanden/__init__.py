from flask import Blueprint

bp = Blueprint("bestanden", __name__)

from app.bestanden import routes
