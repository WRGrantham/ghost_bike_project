"""Demonstration of Google Maps."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, jsonify, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Location, Ghostbike, Photo

app = Flask(__name__)
app.secret_key = "yourkeynamehere"
app.jinja_env.undefined = StrictUndefined

#---------------------------------------------------------------------#

@app.route('/')
def index():
    """show homepage"""

    return render_template("homepage.html")

@app.route('/login', methods=['GET'])
def login_form():
    """form for username/pw login"""
    
    return render_template("login_form.html")

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    flash("You have successfully logged out")

    return redirect("/")


@app.route('/login', methods=['POST'])
def login_process():
    """login process with existing credentials"""

    #Get form variables
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/")


@app.route('/check_login', methods=['GET'])
def check_login():
    print("Hello!")
    if "user_id" in session: 
        return "True"
    else:
        return "False"









#---------------------------------------------------------------------#

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")