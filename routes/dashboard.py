from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import check_password_hash
from models.database import get_db
from services.helpers import admin_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route('/dashboard')
@admin_required
def dashboard():
    conn = get_db()
    total_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    completed_orders = conn.execute("SELECT COUNT(*) FROM orders WHERE status='Completed'").fetchone()[0]
    total_revenue = conn.execute("SELECT SUM(total) FROM orders WHERE status='Completed'").fetchone()[0] or 0
    revenue_data = conn.execute("SELECT id, total FROM orders WHERE status='Completed'").fetchall()
    labels = [f"Order {row['id']}" for row in revenue_data]
    values = [row['total'] for row in revenue_data]
    return render_template("dashboard.html", total_orders=total_orders, completed_orders=completed_orders,
                           total_revenue=total_revenue, labels=labels, values=values)

# -----------------------------
# Orders management
# -----------------------------
def get_order_items(order_id):
    conn = get_db()
    return conn.execute("SELECT * FROM order_items WHERE order_id=?", (order_id,)).fetchall()