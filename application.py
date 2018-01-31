from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp

from helpers import *

from flask.ext.uploads import UploadSet, configure_uploads, IMAGES

# configure application
app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/upload_images/'
configure_uploads(app, photos)

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

@app.route("/explore", methods=["GET", "POST"])
@login_required
def explore():

    photos = db.execute("SELECT * FROM photos ORDER BY RANDOM () LIMIT 99;")

    user_names = db.execute("SELECT id, username FROM users")

    userdict = {user["id"] : user["username"] for user in user_names}

    if request.method == "POST":
        if request.form.get("likeknop"):
            photo_id = request.form.get("likeknop")
            db.execute("INSERT INTO likes (photo_id, user_id) VALUES (:photo_id, :user_id)", photo_id=int(photo_id), user_id=session["user_id"])

        elif request.form.get("commentknop"):
            photo_id = request.form.get("commentknop")
            comment = request.form.get("comment")
            db.execute("INSERT INTO comments (photo_id, user_id, comment_text) VALUES (:photo_id, :user_id, :comment)", photo_id=int(photo_id), user_id=session["user_id"], comment=str(comment))

    liked_photos = db.execute("SELECT photo_id FROM likes WHERE user_id=:user_id", user_id=session["user_id"])
    photo_likes = []
    for liked_photo in liked_photos:
        photo_likes.append(liked_photo["photo_id"])

    likes_count = db.execute("SELECT photo_id FROM likes")

    like_count = {photo_id["photo_id"] : 0 for photo_id in likes_count}

    for like in likes_count:
        like_count[like["photo_id"]] += 1

    return render_template("explore.html", photos=photos, userdict=userdict, photo_likes=photo_likes, like_count=like_count)


@app.route("/profile")
@login_required
def profile():

    user_names = db.execute("SELECT username FROM users WHERE id = :id", id=session["user_id"])
    usernames = []
    for user_name in user_names:
        usernames.append(user_name["username"])

    photos = db.execute("SELECT photo_location, caption, photo_id FROM photos WHERE user_id=:id", id=session["user_id"])

    if request.method == "POST":
        photo_id = request.form.get("likeknop")
        db.execute("INSERT INTO likes (photo_id, user_id) VALUES (:photo_id, :user_id)", photo_id=int(photo_id), user_id=session["user_id"])

    liked_photos = db.execute("SELECT photo_id FROM likes WHERE user_id=:user_id", user_id=session["user_id"])
    photo_likes = []
    for liked_photo in liked_photos:
        photo_likes.append(liked_photo["photo_id"])

    likes_count = db.execute("SELECT photo_id FROM likes")

    like_count = {photo_id["photo_id"] : 0 for photo_id in likes_count}

    for like in likes_count:
        like_count[like["photo_id"]] += 1

    return render_template("profile.html", usernames=usernames, photos=photos, photo_likes=photo_likes, like_count=like_count)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():

    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])

        new_post = db.execute("INSERT INTO photos (photo_location, user_id, caption) VALUES (:photo_location, :user_id, :caption)", photo_location=filename, user_id=session["user_id"], caption=request.form.get("caption"))
        if not new_post:
            return render_template("apology.html")

        if not request.form.get("caption"):
            return render_template("apology.html")

        rows = db.execute("SELECT * FROM photos WHERE photo_location = :photo_location", photo_location=filename)
        session["photo_id"] = rows[0]["photo_id"]

        return redirect(url_for("profile"))

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
        return redirect(url_for("explore"))

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

        return redirect(url_for("explore"))

    else:
        return render_template("register.html")