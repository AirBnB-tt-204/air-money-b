import os
from flask import Flask
from dotenv import load_dotenv

from .models import DB, init_db
from .routes import airbnb_routes

load_dotenv()

DB_FILEPATH = os.path.join(os.path.dirname(__file__), 'db.sqlite3')

DB_URI = f'sqlite:////{DB_FILEPATH}' # using absolute filepath 

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
