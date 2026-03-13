from flask import Blueprint, render_template, request, redirect, session, flash

my_orders_bp = Blueprint("my_orders", __name__)

@my_orders_bp.route("/my_orders")

def my_orders():
    customer_id = session.get("customer_id")
    if not customer_id:
        return redirect("/login")  
        # extra safety

    

    try:
        # Fetch all orders for the logged-in customer
        orders = conn.execute("""
            SELECT * FROM orders
            WHERE customer_id=?
            ORDER BY id DESC
        """, (customer_id,)).fetchall()

        # For each order, fetch its items
        orders_with_items = []
        for order in orders:
            items = conn.execute("""
                SELECT * FROM order_items
                WHERE order_id=?
            """, (order["id"],)).fetchall()
            orders_with_items.append({
                "order": order,
                "items": items
            })

    except Exception as e:
        print("ERROR fetching orders:", e)
        orders_with_items = []

    return render_template("my_orders.html", orders=orders_with_items)