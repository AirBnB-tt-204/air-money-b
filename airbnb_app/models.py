from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):  # User Table
    """Twitter Users corresponding to Tweets"""
    id = DB.Column(DB.BigInteger, primary_key=True)  # id column
    name = DB.Column(DB.String, nullable=False)  # name column
    
    def __repr__(self):
        return f'<User: {self.name}:{self.id}>'


class Listing(DB.Model):
    """Listings corresponding to Users"""
    id = DB.Column(DB.BigInteger, primary_key=True)  # id column
    name = DB.Column(DB.String, nullable=False)
    property_type = DB.Column(DB.String, nullable=False)
    room_type =  DB.Column(DB.String, nullable=False)
    min_nights = DB.Column(DB.Integer, nullable=False)
    location = DB.Column(DB.String, nullable=False)
    price = DB.Column(DB.Float, nullable=False)
    user_id = DB.Column(DB.BigInteger, 
                        DB.ForeignKey("user.id"), 
                        nullable=False)  # user_id column (corresponding user)
    user = DB.relationship("User",
                           backref=DB.backref("listings", lazy=True))  # creates user link between listings

    def __repr__(self):
        return f'<Listing: {self.name}:{self.property_type}:{self.room_type}:{self.min_nights}:{self.location}:{self.user.name}>'


def init_db(app):
    with app.app_context():
        try:
            print(User.query.all())
        except Exception as e:
            print(e)
            print('Creating DB tables')
            DB.create_all()
        