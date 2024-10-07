import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_file_upload import FileUpload
from flask_login import LoginManager
from config import Config
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate(render_as_batch=True)
file_upload = FileUpload()
login = LoginManager()


def create_app(config_class=Config):
    
    app = Flask(__name__, static_folder="static")
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    file_upload.init_app(app, db)
    login.init_app(app)

    CORS(app, resources={r'/*': {'origins': '*'}})

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app