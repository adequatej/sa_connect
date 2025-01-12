from flask import Blueprint

course_blueprint = Blueprint('course', __name__)

from app.course import course_routes