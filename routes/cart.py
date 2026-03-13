from flask import Blueprint, session, render_template, redirect, jsonify, request
from models.database import get_db

cart_bp = Blueprint("cart", __name__)


# Add product to cart
@cart_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):

    conn = get_db()

    product = conn.execute(
        "SELECT * FROM products WHERE id=?",
        (product_id,)
    ).fetchone()

    if not product:
        return jsonify({"success": False})

    cart = session.get("cart", {})
    pid = str(product_id)

    if pid not in cart:
        cart[pid] = {
            "name": product["name"],
            "price": float(product["price"]),
            "image": product["image"],
            "quantity": 1
        }
    else:
        # ensure quantity exists
        cart[pid]["quantity"] = cart[pid].get("quantity", 0) + 1

    session["cart"] = cart
    session.modified = True

    return jsonify({
        "success": True,
        "cart": cart
    })


# Cart page
@cart_bp.route("/cart")
def cart():

    cart = session.get("cart", {})

    products = []
    total = 0

    for pid, item in cart.items():

        qty = item.get("quantity", 1)
        price = float(item["price"])
        subtotal = price * qty

        products.append({
            "id": pid,
            "name": item["name"],
            "price": price,
            "image": item.get("image"),
            "quantity": qty,
            "subtotal": subtotal
        })

        total += subtotal

    return render_template(
        "cart.html",
        products=products,
        total=total
    )


# Increase quantity
@cart_bp.route("/cart/increase/<product_id>", methods=["POST"])
def increase(product_id):

    cart = session.get("cart", {})

    if product_id in cart:
        cart[product_id]["quantity"] += 1

    session["cart"] = cart
    session.modified = True

    return jsonify(success=True, cart=cart)


# Decrease quantity
@cart_bp.route("/cart/decrease/<product_id>", methods=["POST"])
def decrease(product_id):

    cart = session.get("cart", {})

    if product_id in cart:

        cart[product_id]["quantity"] -= 1

        if cart[product_id]["quantity"] <= 0:
            cart.pop(product_id)

    session["cart"] = cart
    session.modified = True

    return jsonify(success=True, cart=cart)


# Remove item
@cart_bp.route("/cart/remove/<product_id>", methods=["POST"])
def remove(product_id):

    cart = session.get("cart", {})

    if product_id in cart:
        cart.pop(product_id)

    session["cart"] = cart
    session.modified = True

    return jsonify(success=True, cart=cart)


# Checkout page
@cart_bp.route("/checkout", methods=["GET","POST"])
def checkout():

    cart = session.get("cart", {})

    if not cart:
        return redirect("/cart")

    return render_template("checkout.html")
    
