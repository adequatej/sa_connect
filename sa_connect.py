from config import Config

from app import create_app, db
from app.user.user_models import User, Student, Faculty
from app.course.course_models import Course
from app.static import form_options
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

# Azure stuff
import identity.web
from flask_session import Session
from werkzeug.middleware.proxy_fix import ProxyFix

app = create_app(Config)
app.jinja_env.globals.update(Auth=identity.web.Auth)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
Session(app)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'db': db, 'User': User, 'Student': Student, 'Faculty': Faculty}

def add_courses(*args, **kwargs):
    query = sqla.select(Course)
    if db.session.scalars(query).first() is None:
        for c in form_options.courses:
            db.session.add(Course(major = c['major'], coursenum = c['coursenum']))
        db.session.commit()

@app.before_request
def init_db(*args, **kwargs):
    if app._got_first_request:
        db.create_all()
    add_courses()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
