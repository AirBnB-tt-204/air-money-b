import os
import psycopg2
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from .models import DB, init_db
from .routes import airbnb_routes

load_dotenv()

app = Flask(__name__)

'''Allows detailed error logs on Heroku'''
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

# '''Connects to Elephant Postgres database'''
# DB_URI = 'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'.format(
#     DB_NAME = os.getenv("DB_NAME"),
#     DB_HOST = os.getenv("DB_HOST"),
#     DB_USER = os.getenv("DB_USER"),
#     DB_PASSWORD = os.getenv("DB_PASSWORD")
# )

def create_app():

    app.secret_key = os.urandom(42)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)
    
    app.register_blueprint(airbnb_routes)    
    return app

APP = create_app()
init_db(APP)
        
if __name__ == "__main__":

    my_app = create_app()
    my_app.run(debug=True)
