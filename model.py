"""Models and database functions for ghost_bike_project."""
from flask_sqlalchemy import SQLAlchemy

from collections import defaultdict

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

#My database is called ghostbikes

db = SQLAlchemy()


##############################################################################
# Model definitions


class Location(db.Model):
    """ghost bike location model"""

    __tablename__ = "gb_map_locations"

    marker_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    gb_lat = db.Column(db.String(20), nullable=True)
    gb_long = db.Column(db.String(20), nullable=True)
    gb_id = db.Column(db.Integer, db.ForeignKey('ghostbikes.ghostbike_id'))
    #ghostbike_id is the foreign key from the ghostbikes and ghostbike_photos tables

    def __repr__(self):
        """provide helpful representation when printed."""
        return f"<Location gb_id{self.gb_id} gb_lat={self.gb_lat} gb_long={self.gb_long}>"



class Ghostbike(db.Model):
    """ghostbike instance model"""

    __tablename__ = "ghostbikes"

    ghostbike_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    accident_date = db.Column(db.Integer, nullable=True)
    cyclist_name = db.Column(db.String(50), nullable=True)
    in_memoriam = db.Column(db.String(1000), nullable=True)
    is_verified = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """provide helpful ghostbike representation when printed"""

        return f"<Ghostbike ghostbike_id={self.ghostbike_id} cyclist_name={self.cyclist} is_verified={self.is_verified}>"


class Photo(db.Model):
    """ghostbike photos model"""

    __tablename__ = "ghostbike_photos"

    photo_id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    submitted_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    ghostbike_id = db.Column(db.Integer, db.ForeignKey('ghostbikes.ghostbike_id'))
    # *Looks like I prooobably don't need this** submission_id = db.Column(db.Integer, autoincrement=True, nullable=False)
    # reminder DATE - format YYYY-MM-DD
    submission_date = db.Column(db.String(100))
    user_date = db.Column(db.String(20))
    photo_blob = db.Column(db.String(20))
    #Again, not sure about doing something with datetime here
    photo_lat = db.Column(db.String(20))
    photo_long = db.Column(db.String(20))
    #Also not sure how to describe an address


    def __repr__(self):
        """provide helpful ghostbike photo representation when printed"""

        return f"<Photo photo_id={self.photo_id} ghostbike_id={self.ghostbike_id} submitted_by={self.submitted_by}>"



class User(db.Model):
    """ghostbike user model"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(30))
    #I don't want this displayed in the table I guess, maybe there's a way to hide it
    is_discoverable = db.Column(db.Integer)
    #maybe it's easier to make a boolean value an integer?

    def __repr__(self):
        """provide helpful user/username representation when printed"""

        return f"<User username={self.username} user_id={self.user_id}>"















##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ghostbikes'
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