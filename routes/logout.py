from flask import Blueprint, render_template, request, redirect, session, flash

logout_bp = Blueprint("logout", __name__)

@logout_bp.route("/logout")
def logout():
    session.pop("customer_id", None)
    session.pop("customer_name", None)
    return redirect("/")