from flask import Blueprint, render_template
import requests

cj_bp = Blueprint("cj", __name__)

CJ_ACCESS_TOKEN = "YOUR_CJ_TOKEN"

@cj_bp.route("/cj_products")
def cj_products():

    url = "https://developers.cjdropshipping.com/api2.0/v1/product/list"

    headers = {
        "CJ-Access-Token": CJ_ACCESS_TOKEN
    }

    params = {
        "pageNum": 1,
        "pageSize": 20
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        data = response.json()

        products = data.get("data", {}).get("list", [])

        return render_template("cj_products.html", products=products)

    except requests.exceptions.HTTPError as e:
        return f"CJ API request failed: {e}"

    except Exception as e:
        return f"Error: {e}"
