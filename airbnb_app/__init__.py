'''
Create and initialize Flask app and SQLAlchemy database.
'''
import os
import psycopg2
from flask import Flask
from dotenv import load_dotenv

from .models import DB, init_db
from .routes import airbnb_routes

load_dotenv()


# DB_URI = 'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_URI = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'


def create_app():
    '''
    Create flask app.
    '''
    app = Flask(__name__)

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
