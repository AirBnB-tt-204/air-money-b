'''
Create and initialize Flask app and SQLAlchemy database.
'''
import os
import psycopg2
import logging
from flask import Flask
from dotenv import load_dotenv

from .models import DB, init_db
from .routes import airbnb_routes

load_dotenv()

'''Connects to Heroku PostgreSQL'''
DB_URI = os.getenv("DATABASE_URL")

def create_app():

    app = Flask(__name__)

    '''Allows detailed error logs on Heroku'''
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    app.secret_key = os.urandom(42)

    app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    app.register_blueprint(airbnb_routes)
    return app


APP = create_app()
init_db(APP)


if __name__ == "__main__":

    my_app = create_app()
    my_app.run(debug=True)
