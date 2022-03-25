from user_app import application
from user_app.models import magazine
from flask import render_template, redirect, request, session

@application.route("/new")
def new_magazine():
    return render_template("new_magazine.html")

@application.route("/magazines/create", methods=["POST"])
def create_magazine():
    if magazine.Magazine.validate_new(request.form):
        magazine.Magazine.create({"user_id": session["id"], "name": request.form["name"], "description": request.form["description"]})
        return redirect("/dashboard")
    return redirect("/new")

@application.route("/magazines/delete/<int:id>")
def delete_magazine(id):
    magazine.Magazine.delete(id)
    return redirect("/users/account")

@application.route("/show/<int:id>")
def show_magazine(id):
    info = magazine.Magazine.get_by_id(id)
    print(info)
    return render_template("show_magazine.html", info=info)