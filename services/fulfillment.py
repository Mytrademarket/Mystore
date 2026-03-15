import requests
from models.database import get_db


def send_order_to_supplier(order_id):

    conn = get_db()

    order = conn.execute("""
    SELECT orders.*, products.supplier, products.supplier_id
    FROM orders
    JOIN products ON orders.product_id = products.id
    WHERE orders.id=?
    """,(order_id,)).fetchone()

    if not order:
        return

    supplier = order["supplier"]

    # Example supplier API
    payload = {
        "product_id": order["supplier_id"],
        "quantity": order["quantity"],
        "customer_name": order["customer_name"],
        "address": order["address"]
    }

    try:

        requests.post(
            "https://supplier-api.com/create-order",
            json=payload
        )

        conn.execute(
            "UPDATE orders SET status='sent_to_supplier' WHERE id=?",
            (order_id,)
        )

        conn.commit()

    except Exception as e:

        print("Supplier order failed:", e)