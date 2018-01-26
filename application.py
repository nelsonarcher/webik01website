from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *
from PIL import Image
# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")

@app.route("/")
@login_required
def index():

    return render_template("apology.html")

@app.route("/explore")
@login_required
def explore():

    return render_template("explore.html")

@app.route("/profile")
@login_required
def profile():

    username = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
    photo = db.execute("SELECT photo_id FROM photos WHERE id=:id", id=session["user_id"])
    page = []
    for x in range(len(photo)):
        page.append(photo)

    return render_template("profile.html", username=username, page=page)


@app.route('/post', methods=['GET', 'POST'])
def post():

    if request.method == "POST":

        if not request.form.get("file"):
           return render_template("apology.html")

        save_image = img.save(request.form.get("file"), "/webik01website/upload-images", "JPEG")

        new_post = db.execute("INSERT INTO photos (photo_location, photo_id, id) VALUES (:photo_location, :photo_id, id)", photo_location=save_image, photo_id=session["photo_id"], id=session["user_id"])
        if not new_post:
            return render_template("apology.html")

        rows = db.execute("SELECT * FROM photos WHERE photo_location = :photo_location", photo_location=save_image)
        session["photo_id"] = rows[0]["photo_id"]

        return redirect(url_for("index"))

    return render_template('post.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html")

        # ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return render_template("apology.html")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html")
        # ensure password was submitted
        if not request.form.get("password"):
            return render_template("apology.html")
        #ensure again password submitted
        if not request.form.get("password_again"):
            return render_template("apology.html")
        # make sure passwords match
        if request.form.get("password") and not request.form.get("password_again"):
            return render_template("apology.html")

        # encrypt password
        store_password = pwd_context.encrypt(request.form.get("password"))

        # make sure username is unique
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=store_password)
        if not result:
            return render_template("apology.html")

        # store id
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        return redirect(url_for("index"))

    else:
        return render_template("register.html")