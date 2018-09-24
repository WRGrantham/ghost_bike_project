"""Demonstration of Google Maps."""

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, jsonify, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Location, Ghostbike, Photo
import base64

app = Flask(__name__)
app.secret_key = "yourkeynamehere"
app.jinja_env.undefined = StrictUndefined

#---------------------------------------------------------------------#

@app.route('/')
def index():
    """show homepage"""

    return render_template("homepage.html")

# @app.route('/login', methods=['GET'])
# def login_form():
#     """form for username/pw login"""
    
#     return render_template("login_form.html")

@app.route('/logout', methods=['GET'])
def logout():
    print("LOGOUT")
    print(session)

    session.clear()
    flash("You have successfully logged out")

    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login_process():
    """login process with existing credentials"""
    if request.method == 'POST':
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
        print(session)

        flash("Logged in")
        return redirect("/")
    else: 
        return render_template("login_form.html")


@app.route('/check_login', methods=['GET'])
def check_login():
    print("Hello!")
    if "user_id" in session: 
        return "True"
    else:
        return "False"

@app.route('/create_new_user', methods=['GET', 'POST'])
def create_new_user_process():
    """display create new user form"""
    if request.method == 'POST':
    #Get form variables
        username = request.form["username"]
        password = request.form["password"]

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username is already taken")
            return redirect("/create_new_user")
        else:
            user = User(username=username, password=password)
            session["user_id"] = user.user_id
            print(session)
            db.session.add(user)
            db.session.commit()

            return render_template("homepage.html")

    return render_template("create_new_user_form.html")

@app.route('/upload_gb_photo', methods=['GET', 'POST'])
def upload_photo_sub():
    """submit photo form, for upload photo"""

    print("pre_upload", request.method, session)
    print("THIS IS MY FUNCTION")
    if request.method == 'POST':
        print("POSTTTTTTTTT!!!!!")
        print(request.files)
        if 'file' not in request.files:
            print("no file part")
            flash('No file part')
            return redirect("/upload_gb_photo")
        file = request.files['file']
        print(dir(file))
        if file.filename == '':
            print("no selected fileeeeee")
            flash('No selected file')
            return redirect("/upload_gb_photo")

        # print(file.read())
        print(session)

        gb_photo = Photo(photo_blob=file.read(), submitted_by=session['user_id'])
        print(session['user_id'])
        db.session.add(gb_photo)
        db.session.commit()
        flash('photo successfully added!')
        print(type(gb_photo.photo_blob))
        return render_template("submit_gb_form.html", photo=base64.b64encode(gb_photo.photo_blob))
    # Serve page!   
    return render_template("submit_gb_form.html", photo=None)

# @app.route('/submit_gb_photo', methods=['POST'])
# def submit_photo_sub():
#     """actually submits photo and commits to db"""

#     file = request.file["file"]
#     user = User(username=username, password=password)
#     session["user_id"] = user.user_id
#     gb_photo = Photo(photo_blob="file")
#     db.session.add(gb_photo)
#     db.session.commit()

#     return render_template("submit_gb_form.html")


    







#---------------------------------------------------------------------#

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")