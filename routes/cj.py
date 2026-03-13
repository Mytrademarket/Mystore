from flask import Blueprint, render_template, redirect, url_for, flash
import requests
from models.database import get_db
import os

cj_bp = Blueprint("cj", __name__)

# Securely get CJ access token from environment variables
CJ_ACCESS_TOKEN = os.environ.get("CJ_ACCESS_TOKEN")
if not CJ_ACCESS_TOKEN:
    raise ValueError(
        "CJ Access Token is missing! Set it as an environment variable on Render."
    )

# CJ API base URL
CJ_API_URL = "https://developers.cjdropshipping.com/api2.0/v1/product/list"


@cj_bp.route("/cj_products")
def cj_products():
    """Fetch CJ products and render them"""
    headers = {"CJ-Access-Token": CJ_ACCESS_TOKEN}
    params = {"pageNum": 1, "pageSize": 20}

    try:
        response = requests.get(CJ_API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        # Handle request errors
        print(f"CJ API request failed: {e}")
        return "Failed to fetch CJ products. Please try again later.", 500

    products = data.get("data", {}).get("list", [])
    return render_template("cj_products.html", products=products)


@cj_bp.route("/import_cj/<product_id>")
def import_cj(product_id):
    """Import a single CJ product into local store"""
    url = f"https://developers.cjdropshipping.com/api2.0/v1/product/query?pid={product_id}"
    headers = {"CJ-Access-Token": CJ_ACCESS_TOKEN}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"CJ API request failed: {e}")
        return "Failed to fetch CJ product. Please try again later.", 500

    product = data.get("data")
    if not product:
        return "Product not found", 404

    conn = get_db()
    try:
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
                999,
            ),
        )
        conn.commit()
    except Exception as e:
        print(f"Database insert failed: {e}")
        return "Failed to import product into store.", 500

    flash(f"Product '{product['productName']}' imported successfully!", "success")
    return redirect(url_for("products.products"))
