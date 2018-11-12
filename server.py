
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, redirect, jsonify, session, flash
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Location, Ghostbike, Photo
import base64, pdb, os

app = Flask(__name__)
app.secret_key=os.environ["app_secret_key"]
app.jinja_env.undefined = StrictUndefined

#---------------------------------------------------------------------#

@app.route('/', methods=['GET'])
def index():
    """show homepage"""

    return render_template("homepage.html")


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
            print(session)
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.user_id

            return render_template("homepage.html")

    return render_template("create_new_user_form.html")

@app.route('/upload_gb_photo', methods=['GET', 'POST'])
def upload_photo_sub():

    print("THIS IS MY FUNCTION")
    if request.method == 'POST':
        print("POSTTTTTTTTT!!!!!")
        print(request.files)
        if 'my_photo' not in request.files:
            print("no file part")
            flash('No file part')
            return redirect("/upload_gb_photo")
        file = request.files['my_photo']
        print(dir(file))
        if file.filename == '':
            print("no selected fileeeeee")
            flash('No selected file')
            return redirect("/upload_gb_photo")

        lat_data = request.form["hiddenLat"]
        long_data = request.form["hiddenLong"]
        submission_timestamp = request.form["hiddenTime"]
        user_date = request.form["gbPhotoDate"]

        if lat_data == '':
            flash("No location! Please click the map to mark photo location")
            return redirect("/upload_gb_photo")

        file.save('static/photos/' + file.filename)


        # lat_data = request.form["hiddenLat"]
        # long_data = request.form["hiddenLong"]
        # submission_timestamp = request.form["hiddenTime"]
        # user_date = request.form["gbPhotoDate"]


        gb_photo = Photo(photo_blob=file.filename, submitted_by=session['user_id'], 
            photo_lat=lat_data, photo_long=long_data, submission_date=submission_timestamp, user_date=user_date)

        print(session['user_id'])
        db.session.add(gb_photo)

        db.session.commit()
        flash('photo successfully added!')
        print(type(gb_photo.photo_blob))
        return render_template("submit_gb_form.html", photo=None)
    print(session)

    # Serve page!   
    return render_template("submit_gb_form.html", photo=None)


@app.route('/gb_locations', methods=['GET', 'POST'])
def show_markers():

    return render_template("gb_locations.html")



@app.route('/gb_photo_gallery', methods=['GET'])
def display_all_photos():
    """function to query photo table and display photos"""


    return render_template("gb_photo_gallery.html")



@app.route('/gb.json')
def gb_info():
    """json info about ghostbike photos locations"""

    ghostbikes = {
        photo.photo_id: {
            "photoId": photo.photo_id,
            "submittedBy": photo.submitted_by,
            "ghostbikeId": photo.ghostbike_id,
            "submissionDate": photo.submission_date,
            "userDate": photo.user_date,
            "photoLat": photo.photo_lat,
            "photoLong": photo.photo_long,
            "photoBlobName": photo.photo_blob
        }
        for photo in Photo.query.limit(50)}
    print("about to jsonify ghostbikes")
    return jsonify(ghostbikes)


#---------------------------------------------------------------------#

if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")