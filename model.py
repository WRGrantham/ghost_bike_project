"""Models and database functions for ghost_bike_project."""
from flask_sqlalchemy import SQLAlchemy
import correlation
from collections import defaultdict

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions


class Location(db.Model):
    """ghost bike location model"""

    __tablename__ = "gb_map_locations"

    location = db.Column(db.Integer, primary_key=True)
    #this is probably wrong, I'm not sure how to present coordinates as a key
    #maybe ghostbike_id should function as the primary key, not sure
    #look up if address can be a db.value
    ghostbike_id = db.Column(db.Integer)
    #ghostbike_id is the foreign key fro the ghostbikes and ghostbike_photos tables

    def __repr__(self):
        """provide helpful representation when printed."""
        return f"<Location ghostbike_location={self.location} ghostbike_id={self.ghostbike_id}>"



class Ghostbike(db.model):
    """ghostbike instance model"""

    __tablename__ = "ghostbikes"

    ghostbike_id = db.Column(db.Integer, primary_key=True)
    accident_date = db.Column(db.Integer)
    #I need to figure out datetime for accident_date
    cyclist_name = db.Column(db.String(50))
    #maybe I can get away with two cyclist_name entries for one incident if
    #that's what happened
    in_memoriam = db.Column(db.String(1000))
    #short blurb about the cyclist, not sure if it belongs in a table because so
    #many characters
    is_verified = db.Column(db.Boolean)
    #can you make a column value a boolean?

    def __repr__(self):
        """provide helpful ghostbike representation when printed"""

        return f"<Ghostbike ghostbike_id={self.ghostbike_id} cyclist_name={self.cyclist} is_verified={self.is_verified}>"


class Photo(db.Model):
    """ghostbike photos model"""

    __tablename__ = "ghostbike_photos"

    photo_id = db.Column(db.Integer)
    submitted_by = db.Column(db.String(100))
    ghostbike_id = db.Column(db.Integer)
    submission_id = db.Column(db.Integer)
    submission_date = db.Column(db.Integer)
    #Again, not sure about doing something with datetime here
    photo_location = db.Column(db.Varchar(100))
    #Also not sure how to describe an address


    def __repr__(self):
        """provide helpful ghostbike photo representation when printed"""

        return f"<Photo photo_id={self.photo_id} ghostbike_id={self.ghostbike_id} submitted_by={self.submitted_by}>"



class User(db.Model):
    """ghostbike user model"""

    __tablename__ = "users"

    username = db.Column(db.String(50))
    password = db.Column(db.Varchar(30))
    #I don't want this displayed in the table I guess, maybe there's a way to hide it
    is_discoverable = db.Column(db.Integer)
    #maybe it's easier to make a boolean value an integer?
    user_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        """provide helpful user/username representation when printed"""

        return f"<User username={self.username} user_id={self.user_id}>"















##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print("Connected to DB.")