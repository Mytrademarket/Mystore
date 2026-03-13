from flask import Blueprint, render_template, request, redirect
from models.database import get_db

pages_bp = Blueprint("pages", __name__)

# Admin pages list
@pages_bp.route("/admin/pages")
def admin_pages():

    conn = get_db()

    pages = conn.execute(
        "SELECT * FROM pages"
    ).fetchall()

    return render_template("admin_pages.html", pages=pages)


# Edit page
@pages_bp.route("/admin/edit_page/<int:id>", methods=["GET","POST"])
def edit_page(id):

    conn = get_db()

    page = conn.execute(
        "SELECT * FROM pages WHERE id=?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        title = request.form["title"]
        content = request.form["content"]

        conn.execute(
            "UPDATE pages SET title=?, content=? WHERE id=?",
            (title,content,id)
        )

        conn.commit()

        return redirect("/admin/pages")

    return render_template("edit_page.html", page=page)


# Public page
@pages_bp.route("/page/<slug>")
def page(slug):

    conn = get_db()

    page = conn.execute(
        "SELECT * FROM pages WHERE slug=?",
        (slug,)
    ).fetchone()

    return render_template("page.html", page=page)

@pages_bp.route("/admin/page_builder")
def page_builder():
    return render_template("page_builder.html")

@pages_bp.route("/admin/save_homepage", methods=["POST"])
def save_homepage():

    content = request.form["content"]

    conn = get_db()

    conn.execute(
        "UPDATE pages SET content=? WHERE slug='home'",
        (content,)
    )

    conn.commit()

    return redirect("/")