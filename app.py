from flask import Flask
from models.database import close_db

from routes.admin import admin_bp
from routes.dashboard import dashboard_bp
from routes.products import products_bp
from routes.orders import orders_bp
from routes.cart import cart_bp
from routes.categories import categories_bp
from routes.settings import settings_bp
from routes.payments import payments_bp
from routes.products import products_bp
from routes.pages import pages_bp
from routes.auth import auth_bp
from routes.register import register_bp
from routes.logout import logout_bp
from routes.my_orders import my_orders_bp
from routes.paypal_payment import paypal_bp
from routes.cj import cj_bp
from routes.eprolo import eprolo_bp
from routes.dropshipping import dropshipping_bp


app = Flask(__name__)
app.secret_key = "supersecretkey"

#load settings globally preprocessor
from models.database import get_db

@app.context_processor
def inject_settings():
    conn = get_db()
    settings = conn.execute(
        "SELECT * FROM settings WHERE id=1"
    ).fetchone()

    return dict(settings=settings)



app.register_blueprint(admin_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(categories_bp)
app.register_blueprint(settings_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(pages_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(register_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(my_orders_bp)
app.register_blueprint(paypal_bp)
app.register_blueprint(cj_bp)
app.register_blueprint(eprolo_bp)
app.register_blueprint(dropshipping_bp)


app.teardown_appcontext(close_db)


if __name__ == "__main__":
    app.run(debug=True)