from flask import Blueprint, redirect
import requests
from models.database import get_db

eprolo_bp = Blueprint("eprolo", __name__)

EPROLO_API_KEY = "A2AE353C17A944439339E04FB3859EF7"

@eprolo_bp.route("/import_eprolo_products")
def import_eprolo_products():

    url = "https://api.eprolo.com/products"

    headers = {
        "Authorization": EPROLO_API_KEY
    }

    try:

        response = requests.get(url, headers=headers)
        data = response.json()

        products = data.get("products", [])

        conn = get_db()

        for p in products:

            name = p.get("title")
            price = p.get("price", 0)
            image = p.get("image")

            conn.execute(
                "INSERT INTO products (name,price,image) VALUES (?,?,?)",
                (name, price, image)
            )

        conn.commit()

        return redirect("/products")

    except Exception as e:

        return f"EPROLO import error: {e}"