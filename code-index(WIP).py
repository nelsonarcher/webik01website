@app.route("/index")
@login_required
def index():

    photo_locations = db.execute("SELECT * FROM photos WHERE photo_id IN (SELECT photo_id FROM photo ORDER BY RANDOM() LIMIT x);")
    locations = []
    for photo_location in photo_locations:
        locations.append(photo_location["photo_location"])

    captions = db.execute("SELECT caption FROM photos WHERE user_id=:user_id", user_id=session["user_id"])
    photo_captions = []
    for caption in captions:
        photo_captions.append(caption["caption"])

    return render_template("index.html", photo_locations=locations, caption=photo_captions)

SELECT * FROM table ORDER BY RANDOM() LIMIT 1;