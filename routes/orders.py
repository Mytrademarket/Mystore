from flask import Blueprint, render_template, redirect
from models.database import get_db
from services.helpers import admin_required, get_order_items

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders")
@admin_required
def view_orders():

    conn = get_db()

    orders = conn.execute(
        "SELECT * FROM orders"
    ).fetchall()

    return render_template(
        "orders.html",
        orders=orders,
        get_order_items=get_order_items
    )


@orders_bp.route("/order_status/<int:id>/<status>")
@admin_required
def order_status(id, status):

    conn = get_db()

    conn.execute(
        "UPDATE orders SET status=? WHERE id=?",
        (status,id)
    )

    conn.commit()

    return redirect("/orders")

# ✅ DELETE ORDER
@orders_bp.route("/delete_order/<int:id>")
@admin_required
def delete_order(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM orders WHERE id=?",
        (id,)
    )

    conn.execute(
        "DELETE FROM order_items WHERE order_id=?",
        (id,)
    )

    conn.commit()

    return redirect("/orders")

@orders_bp.route("/invoice/<int:id>")
@admin_required
def invoice(id):

    conn = get_db()

    order = conn.execute(
        "SELECT * FROM orders WHERE id=?",
        (id,)
    ).fetchone()

    items = conn.execute(
        "SELECT * FROM order_items WHERE order_id=?",
        (id,)
    ).fetchall()

    return render_template(
        "invoice.html",
        order=order,
        items=items
    )