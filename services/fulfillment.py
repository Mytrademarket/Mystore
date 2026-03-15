import requests

def send_order_to_supplier(product):

    payload = {

        "product_id": product["supplier_id"],
        "quantity": 1,
        "address": "customer shipping address"

    }

    requests.post(
        "https://supplier-api.com/order",
        json=payload
    )