'''
SQLAlchemy ORM models
'''
from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class User(DB.Model):  # user Table
    """ Property Owners/Managers corresponding to Listings"""
    id = DB.Column(DB.Integer, primary_key=True)  # id column
    name = DB.Column(DB.String, nullable=False)  # name column

    def __repr__(self):
        return f'<User: {self.name}:{self.id}>'


class Listing(DB.Model):  # listing Table
    """Listings corresponding to Users"""
    id = DB.Column(DB.Integer, primary_key=True)  # id column
    name = DB.Column(DB.String, nullable=False)
    property_type = DB.Column(DB.String, nullable=False)
    room_type = DB.Column(DB.String, nullable=False)
    minimum_nights = DB.Column(DB.Integer, nullable=False)
    availability_365 = DB.Column(DB.Integer, nullable=False)
    city = DB.Column(DB.String, nullable=False)
    neighborhood = DB.Column(DB.String, nullable=False)
    price = DB.Column(DB.Integer, nullable=False)
    user_id = DB.Column(DB.BigInteger,
                        DB.ForeignKey("user.id"),
                        nullable=False)  # user_id column (corresponding user)
    # creates user link between listings
    user = DB.relationship("User",
                           backref=DB.backref("listings",
                                              lazy=True))

    def __repr__(self):
        return f'<Listing: {self.name}:{self.property_type}:'\
            f'{self.room_type}:{self.minimum_nights}:'\
            f'{self.city}:{self.neighborhood}:'\
            f'{self.availability_365}:{self.user.name}>'


def init_db(app):
    '''
    Initialize SQLAlchemy database.
    '''
    with app.app_context():
        try:
            # Attempt to access the user table from the database
            print(User.query.first())
        except Exception as no_such_table_exception:
            # The table does not exist yet
            # We catch the generalized Exception because the
            # specific exception would vary based on the
            # underlying database e.g. for sqlite it is
            # sqlite3.OperationalError
            print(no_such_table_exception)
            print('Creating DB tables')
            # Create the user and listing tables
            DB.create_all()
