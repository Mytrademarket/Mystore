from flask import Blueprint, render_template, redirect
import requests
from models.database import get_db

suppliers_bp = Blueprint("suppliers", __name__)

SUPPLIER_API = "https://dummyjson.com/products"


@suppliers_bp.route("/supplier_products")
def supplier_products():

    response = requests.get(SUPPLIER_API)
    data = response.json()

    return render_template(
        "supplier_products.html",
        products=data["products"]
    )


@suppliers_bp.route("/import_product/<int:id>")
def import_product(id):

    conn = get_db()

    response = requests.get(f"{SUPPLIER_API}/{id}")
    p = response.json()

    conn.execute("""
    INSERT INTO products
    (name, price, description, stock, image, supplier, supplier_id, supplier_price)
    VALUES (?,?,?,?,?,?,?,?)
    """,(
        p["title"],
        float(p["price"])*2,
        p["description"],
        100,
        p["thumbnail"],
        "demo_supplier",
        p["id"],
        p["price"]
    ))

    conn.commit()

    return redirect("/products")