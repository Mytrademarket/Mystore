from flask import session, redirect
from functools import wraps
from models.database import get_db

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin"):
            return redirect("/admin")
        return f(*args, **kwargs)
    return decorated


def customer_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("customer_id"):
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated


def get_order_items(order_id):
    conn = get_db()
    return conn.execute(
        "SELECT * FROM order_items WHERE order_id=?",
        (order_id,)
    ).fetchall()