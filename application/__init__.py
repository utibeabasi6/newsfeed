from flask import Flask
from .views import views
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(views)
    return app
