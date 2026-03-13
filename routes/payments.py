from flask import Blueprint, session, redirect, url_for, request, flash
import requests
import uuid
import sqlite3

payments_bp = Blueprint("payments", __name__)

# Pesapal credentials
PESAPAL_CONSUMER_KEY = "od9WE172p0ag8yTqdeO5/2+UnjHWclas"
PESAPAL_CONSUMER_SECRET = "/5UGWJPjPGFtZVL56qJx4NUIbsc="

# Sandbox (testing)
PESAPAL_BASE_URL = "https://pay.pesapal.com/v3/api"

# Your IPN ID from Pesapal dashboard
PESAPAL_IPN_ID = "https://susuman.pythonanywhere.com/payment_callback"


# -----------------------------
# Database connection
# -----------------------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# Save order
# -----------------------------
def save_order(cart, customer_info, total):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO orders (customer_name, phone, address, total, status)
        VALUES (?,?,?,?,?)
    """, (
        customer_info["name"],
        customer_info["phone"],
        customer_info["address"],
        total,
        "Pending"
    ))

    order_id = cursor.lastrowid

    for item in cart.values():
        cursor.execute("""
            INSERT INTO order_items (order_id, product_name, price, quantity)
            VALUES (?,?,?,?)
        """, (
            order_id,
            item["name"],
            item["price"],
            item["quantity"]
        ))

    conn.commit()
    conn.close()

    return order_id


# -----------------------------
# Get Pesapal token
# -----------------------------
def get_token():
    url = f"{PESAPAL_BASE_URL}/Auth/RequestToken"

    payload = {
        "consumer_key": PESAPAL_CONSUMER_KEY,
        "consumer_secret": PESAPAL_CONSUMER_SECRET
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Pesapal token error:", response.text)
        return None

    return response.json().get("token")


# -----------------------------
# Pay with Pesapal
# -----------------------------
@payments_bp.route("/pesapal_pay", methods=["POST"])
def pesapal_pay():

    cart = session.get("cart", {})

    if not cart:
        flash("Cart is empty")
        return redirect(url_for("cart.checkout"))

    total = sum(item["price"] * item["quantity"] for item in cart.values())

    customer_info = {
        "name": request.form.get("name"),
        "phone": request.form.get("phone"),
        "address": request.form.get("address")
    }

    # Save order
    order_id = save_order(cart, customer_info, total)

    token = get_token()

    if not token:
        flash("Could not get Pesapal token")
        return redirect(url_for("cart.checkout"))

    merchant_ref = str(order_id)

    payload = {
        "id": merchant_ref,
        "currency": "ZMW",
        "amount": total,
        "description": f"Order #{order_id}",
        "callback_url": url_for("payments.payment_callback", _external=True),
        "notification_id": PESAPAL_IPN_ID,
        "billing_address": {
            "email_address": request.form.get("email"),
            "phone_number": customer_info["phone"],
            "country_code": "ZM",
            "first_name": customer_info["name"].split()[0],
            "last_name": customer_info["name"].split()[-1]
        }
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{PESAPAL_BASE_URL}/Transactions/SubmitOrderRequest",
        json=payload,
        headers=headers
    )

    print("Pesapal response:", response.text)

    if response.status_code != 200:
        flash("Error initiating payment")
        return redirect(url_for("cart.checkout"))

    data = response.json()

    payment_url = data.get("redirect_url")

    if not payment_url:
        flash("Payment link not received")
        return redirect(url_for("cart.checkout"))

    return redirect(payment_url)


# -----------------------------
# Payment callback
# -----------------------------
@payments_bp.route("/payment_callback")
def payment_callback():

    order_tracking_id = request.args.get("OrderTrackingId")
    merchant_ref = request.args.get("OrderMerchantReference")

    token = get_token()

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{PESAPAL_BASE_URL}/Transactions/GetTransactionStatus?orderTrackingId={order_tracking_id}",
        headers=headers
    )

    data = response.json()

    status = data.get("payment_status_description")

    conn = get_db()
    cursor = conn.cursor()

    if status == "Completed":

        cursor.execute("""
            UPDATE orders
            SET status = ?
            WHERE id = ?
        """, ("Completed", merchant_ref))

        conn.commit()

    conn.close()

    return "Payment processed successfully"