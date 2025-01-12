from flask import Blueprint

application_blueprint = Blueprint('application', __name__)

from app.application import application_routes

###