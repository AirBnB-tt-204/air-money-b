import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import psycopg2

from .models import DB, init_db
from .routes import airbnb_routes

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, 
                              password=DB_PASSWORD, host=DB_HOST)


def create_app():
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
