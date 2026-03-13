from flask import Blueprint, render_template, request, redirect
from models.database import get_db
import os
from werkzeug.utils import secure_filename

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/site_settings", methods=["GET","POST"])
def site_settings():

    conn = get_db()

    if request.method == "POST":

        store_name = request.form.get("store_name")
        store_email = request.form.get("store_email")
        store_phone = request.form.get("store_phone")
        store_address = request.form.get("store_address")

        footer_about = request.form.get("footer_about")

        facebook = request.form.get("facebook")
        instagram = request.form.get("instagram")
        twitter = request.form.get("twitter")
        youtube = request.form.get("youtube")
        tiktok = request.form.get("tiktok")

        whatsapp = request.form.get("whatsapp")
        google_analytics = request.form.get("google_analytics")

        privacy_policy_page = request.form.get("privacy_policy_page")
        terms_page = request.form.get("terms_page")
        refund_page = request.form.get("refund_page")
        shipping_page = request.form.get("shipping_page")
        contact_page = request.form.get("contact_page")
        faq_page = request.form.get("faq_page")

        logo_file = request.files.get("logo")

        logo_filename = None

        if logo_file and logo_file.filename != "":
            filename = secure_filename(logo_file.filename)
            path = os.path.join("static/uploads", filename)
            logo_file.save(path)
            logo_filename = filename

        conn.execute("""
        INSERT OR REPLACE INTO settings
        (id, store_name, store_email, store_phone, store_address,
        footer_about, facebook, instagram, twitter, youtube, tiktok,
        whatsapp, google_analytics,
        privacy_policy_page, terms_page, refund_page,
        shipping_page, contact_page, faq_page, logo)
        VALUES
        (1,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,(
            store_name, store_email, store_phone, store_address,
            footer_about, facebook, instagram, twitter, youtube, tiktok,
            whatsapp, google_analytics,
            privacy_policy_page, terms_page, refund_page,
            shipping_page, contact_page, faq_page, logo_filename
        ))

        conn.commit()

        return redirect("/site_settings")

    settings = conn.execute(
        "SELECT * FROM settings WHERE id=1"
    ).fetchone()

    return render_template("site_settings.html", **(settings or {}))