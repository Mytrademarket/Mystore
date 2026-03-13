from flask import Blueprint, render_template, redirect, url_for
import requests
from models.database import get_db
import os

cj_bp = Blueprint("cj", __name__)

CJ_ACCESS_TOKEN = os.environ.get("CJ5231490@api@96d336de06474ba38e2e3446db4dd836")

# CJ API base
CJ_API_URL = "https://developers.cjdropshipping.com/api2.0/v1/product/list"


@cj_bp.route("/cj_products")
def cj_products():

    headers = {
        "CJ-Access-Token": CJ_ACCESS_TOKEN
    }

    params = {
        "pageNum": 1,
        "pageSize": 20
    }

    response = requests.get(CJ_API_URL, headers=headers, params=params)

    data = response.json()

    products = data.get("data", {}).get("list", [])

    return render_template("cj_products.html", products=products)


# Import product into your store
@cj_bp.route("/import_cj/<product_id>")
def import_cj(product_id):

    url = f"https://developers.cjdropshipping.com/api2.0/v1/product/query?pid={product_id}"

    headers = {
        "CJ-Access-Token": CJ_ACCESS_TOKEN
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    product = data.get("data")

    if not product:
        return "Product not found"

    conn = get_db()

    conn.execute(
        """
        INSERT INTO products (name, price, description, image, stock)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            product["productName"],
            product["sellPrice"],
            product["description"],
            product["productImage"],
            999
        )
    )

    conn.commit()

    return redirect(url_for("products.products"))