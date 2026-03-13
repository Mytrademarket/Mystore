from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import check_password_hash
from models.database import get_db
from services.helpers import admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin", methods=["GET","POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        admin = conn.execute(
            "SELECT * FROM admins WHERE username=?",
            (username,)
        ).fetchone()

        if admin and check_password_hash(admin["password"], password):

            session["admin"] = True
            session["admin_username"] = username

            return redirect("/dashboard")

    return render_template("admin_login.html")


@admin_bp.route("/dashboard")
def dashboard():

    conn = get_db()

    orders = conn.execute("SELECT * FROM orders").fetchall()

    total_orders = len(orders)
    completed_orders = len([o for o in orders if o["status"] == "completed"])
    total_revenue = sum(o["total"] for o in orders)

    labels = [f"Order {o['id']}" for o in orders]
    values = [o["total"] for o in orders]

    return render_template(
        "dashboard.html",
        total_orders=total_orders,
        completed_orders=completed_orders,
        total_revenue=total_revenue,
        labels=labels,
        values=values
    )