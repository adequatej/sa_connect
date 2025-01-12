from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_session import Session
import identity.web  

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager() 
login.login_view = 'user.login'  
app_session = Session()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER
    app.template_folder = config_class.TEMPLATE_FOLDER_APPLICATION

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    Session(app)
    
    # Azure auth
    auth = identity.web.Auth(
        session=Session,
        authority=app.config["AUTHORITY"],
        client_id=app.config["CLIENT_ID"],
        client_credential=app.config["CLIENT_SECRET"],
    )

    from app.application import application_blueprint as application
    application.template_folder = Config.TEMPLATE_FOLDER_APPLICATION
    app.register_blueprint(application)

    from app.course import course_blueprint as course
    course.template_folder = Config.TEMPLATE_FOLDER_COURSE
    app.register_blueprint(course)

    from app.user import user_blueprint as user
    user.template_folder = Config.TEMPLATE_FOLDER_USER
    app.register_blueprint(user)

    from app.errors import error_blueprint as errors
    errors.template_folder = Config.TEMPLATE_FOLDER_ERRORS
    app.register_blueprint(errors)


    return app