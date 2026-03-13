from flask import Blueprint, render_template, request, redirect, session, flash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Example login logic (replace with your DB check)
        if email == "test@test.com" and password == "1234":
            session["customer_id"] = 1
            session["customer_name"] = "Customer"
            return redirect("/")

        flash("Invalid login details")

    return render_template("login.html")