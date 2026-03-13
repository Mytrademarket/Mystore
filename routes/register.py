from flask import Blueprint, render_template, request, redirect, session, flash

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if not name or not email or not password:
            return "All fields required"

        hashed_password = generate_password_hash(password)

        try:
            conn.execute("""
                INSERT INTO customers (name, email, password)
                VALUES (?, ?, ?)
            """, (name, email, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Email already registered"

        return redirect("/login")

    return render_template("register.html")