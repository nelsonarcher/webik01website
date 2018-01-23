def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")
        # ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password")
        #ensure again password submitted
        if not request.form.get("password_again"):
            return apology("must provide password again")
        # make sure passwords match
        if request.form.get("password") and not request.form.get("password_again"):
            return apology("passwords do not match")

        # encrypt password
        store_password = pwd_context.encrypt(request.form.get("password"))

        # make sure username is unique
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=store_password)
        if not result:
            return apology("Username already exists")

        # store id
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        return redirect(url_for("index"))

    else:
        return render_template("register.html")