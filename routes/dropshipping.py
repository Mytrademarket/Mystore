from flask import Blueprint, render_template, redirect
import requests
from models.database import get_db

dropshipping_bp = Blueprint("dropshipping", __name__)

# Example supplier API (can be replaced)
SUPPLIER_API = "https://dummyjson.com/products"


@dropshipping_bp.route("/supplier_products")
def supplier_products():

    response = requests.get(SUPPLIER_API)

    data = response.json()

    products = data["products"]

    return render_template(
        "supplier_products.html",
        products=products
    )


@dropshipping_bp.route("/import_supplier_product/<int:product_id>")
def import_supplier_product(product_id):

    conn = get_db()

    response = requests.get(f"{SUPPLIER_API}/{product_id}")

    product = response.json()

    conn.execute("""
        INSERT INTO products
        (name, price, description, stock, image)
        VALUES (?,?,?,?,?)
    """,(
        product["title"],
        product["price"],
        product["description"],
        100,
        product["thumbnail"]
    ))

    conn.commit()

    return redirect("/products")