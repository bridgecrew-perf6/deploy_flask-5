from user_app import application
from user_app.models import user, magazine
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(application)

@application.route("/")
def index():
    if "id" in session:
        return redirect("/dashboard")
    return render_template("index.html")


@application.route("/users/create", methods=["POST"])
def create():
    if user.User.validate_new(request.form):
        if user.User.check_unique(request.form): 
            session["id"] = user.User.create({
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "email": request.form["email"],
            "password": bcrypt.generate_password_hash(request.form['password'])
        })
        return redirect("/dashboard")
    return redirect("/")

@application.route("/users/update", methods=["POST"])
def update():
    if user.User.validate_update(request.form):
        user.User.update({
            "id": session["id"],
            "first_name" : request.form["first_name"],
            "last_name" : request.form["last_name"],
            "email" : request.form["email"]
        })
        return redirect("/dashboard")
    return redirect("/users/account")

@application.route("/users/login", methods=["POST"])
def login():
    if user.User.validate_login(request.form):
        info = user.User.get_by_email(request.form)
        if not info or not bcrypt.check_password_hash(info.password, request.form["password"]):
            flash("Invalid info")
            return redirect("/")
        session["id"] = info.id
        return redirect("/dashboard")
    return redirect ("/")

@application.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@application.route("/users/account")
def account():
    if "id" in session:
        info = user.User.get_by_id(session)
        info.magazines = user.User.get_user_magazines(info.id)
        return render_template("account.html", info=info)
    return redirect("/")

@application.route("/dashboard")
def dashboard():
    if "id" in session:
        info = {
            "user": user.User.get_by_id(session),
            "magazines": magazine.Magazine.get_all()
        }
        return render_template("dashboard.html", info=info)
    return redirect("/")


