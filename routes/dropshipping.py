from flask import Blueprint, render_template, redirect
import requests
from models.database import get_db
from services.pricing import calculate_price

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
    
    price = calculate_price(product["price"])
    conn.execute("""
INSERT INTO products
(name, price, description, stock, image)
VALUES (?,?,?,?,?)
""",(
    product["title"],
    price,
    product["description"],
    100,
    product["thumbnail"]
))

@dropshipping_bp.route("/sync_supplier_stock")
def sync_supplier_stock():

    conn = get_db()

    products = conn.execute(
        "SELECT * FROM products WHERE supplier IS NOT NULL"
    ).fetchall()

    for p in products:

        supplier_id = p["supplier_id"]

        response = requests.get(
            f"https://dummyjson.com/products/{supplier_id}"
        )

        data = response.json()

        stock = data.get("stock", 0)

        conn.execute(
            "UPDATE products SET stock=? WHERE id=?",
            (stock, p["id"])
        )

    conn.commit()

    return "Stock Updated Successfully"

    conn.commit()

    return redirect("/products")