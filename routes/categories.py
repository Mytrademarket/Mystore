from flask import Blueprint, render_template, request, redirect
from models.database import get_db
from services.helpers import admin_required

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/add_category", methods=["GET","POST"])
@admin_required
def add_category():

    conn = get_db()

    if request.method == "POST":

        name = request.form["name"]

        conn.execute(
            "INSERT INTO categories (name) VALUES (?)",
            (name,)
        )

        conn.commit()

    categories = conn.execute(
        "SELECT * FROM categories"
    ).fetchall()

    return render_template(
        "add_category.html",
        categories=categories
    )