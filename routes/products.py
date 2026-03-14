from flask import Blueprint, render_template, request, redirect, jsonify, current_app
from werkzeug.utils import secure_filename
import os
from models.database import get_db
from services.helpers import admin_required

products_bp = Blueprint("products", __name__)

# Helper functions
def build_product_grid(products):
    html = ""
    for p in products:
        html += f"""
        <div class="col-md-3 mb-4">
            <div class="card h-100 shadow-sm">
                {% if "http" in p['image'] %}
<img src="{{ p['image'] }}" class="card-img-top">
{% else %}
<img src="/static/uploads/{{ p['image'] }}" class="card-img-top">
{% endif %}
                <div class="card-body">
                    <h6 class="card-title">{p['name']}</h6>
                    <p class="text-primary fw-bold">${p['price']}</p>
                    <a href="/product/{p['id']}" class="btn btn-dark btn-sm w-100">View Product</a>
                </div>
            </div>
        </div>
        """
    return html

def build_category_grid():
    conn = get_db()
    categories = conn.execute("SELECT * FROM categories").fetchall()
    html = ""
    for c in categories:
        html += f"""
        <div class="col-md-3 mb-3">
            <a href="/category/{c['id']}" class="btn btn-outline-dark w-100">{c['name']}</a>
        </div>
        """
    return html

# Homepage
@products_bp.route("/")
def home():
    conn = get_db()
    products = conn.execute("SELECT * FROM products LIMIT 12").fetchall()
    homepage = conn.execute("SELECT value FROM site_settings WHERE key='homepage_content'").fetchone()
    whatsapp = conn.execute("SELECT value FROM site_settings WHERE key='whatsapp'").fetchone()

    return render_template(
        "home.html",
        products=products,
        homepage_content=homepage["value"] if homepage else "",
        whatsapp=whatsapp["value"] if whatsapp else None
    )

# Admin products page
@products_bp.route("/products")
@admin_required
def products():
    conn = get_db()
    products = conn.execute("""
        SELECT products.*, categories.name AS category_name
        FROM products
        LEFT JOIN categories
        ON products.category_id = categories.id
    """).fetchall()
    return render_template("products.html", products=products)

# Add product
@products_bp.route("/add_product", methods=["GET", "POST"])
def add_product():
    conn = get_db()
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        stock = request.form["stock"]
        category_id = request.form["category_id"]

        image = request.files.get("image")
        filename = None
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join("static/uploads", filename))

        # Insert product
        cursor = conn.execute("""
            INSERT INTO products (name, price, description, stock, category_id, image)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, price, description, stock, category_id, filename))
        product_id = cursor.lastrowid

        # Upload gallery images
        gallery_images = request.files.getlist("images")
        for file in gallery_images:
            if file.filename != "":
                img_name = secure_filename(file.filename)
                file.save(os.path.join("static/uploads", img_name))
                conn.execute(
                    "INSERT INTO product_images (product_id,image) VALUES (?,?)",
                    (product_id, img_name)
                )

        conn.commit()
        return redirect("/products")

    categories = conn.execute("SELECT * FROM categories").fetchall()
    return render_template("add_product.html", categories=categories)

# Edit product
@products_bp.route("/edit_product/<int:product_id>", methods=["GET","POST"])
def edit_product(product_id):
    conn = get_db()
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]
        stock = request.form["stock"]
        category_id = request.form["category_id"]

        image_file = request.files.get("image")
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            upload_path = os.path.join(current_app.root_path, "static/uploads", filename)
            image_file.save(upload_path)
            conn.execute("""
                UPDATE products SET name=?, price=?, description=?, stock=?, category_id=?, image=?
                WHERE id=?
            """, (name, price, description, stock, category_id, filename, product_id))
        else:
            conn.execute("""
                UPDATE products SET name=?, price=?, description=?, stock=?, category_id=?
                WHERE id=?
            """, (name, price, description, stock, category_id, product_id))

        conn.commit()
        return redirect("/products")

    product = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    categories = conn.execute("SELECT * FROM categories").fetchall()
    images = conn.execute("SELECT * FROM product_images WHERE product_id=?", (product_id,)).fetchall()
    return render_template("edit_product.html", product=product, categories=categories, images=images)

# Search
@products_bp.route("/search")
def search():
    query = request.args.get("q")
    conn = get_db()
    products = conn.execute("SELECT * FROM products WHERE name LIKE ?", ("%"+query+"%",)).fetchall()
    return render_template("search_results.html", products=products, query=query)

# Search suggestions (AJAX)
@products_bp.route("/search_suggestions")
def search_suggestions():
    query = request.args.get("q","")
    conn = get_db()
    products = conn.execute(
        "SELECT id,name,image,price FROM products WHERE name LIKE ? LIMIT 5",
        ("%"+query+"%",)
    ).fetchall()
    results = [{"id": p["id"], "name": p["name"], "image": p["image"], "price": p["price"]} for p in products]
    return jsonify(results)

# Product page
@products_bp.route("/product/<int:product_id>")
def product_page(product_id):
    conn = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    images = conn.execute("SELECT * FROM product_images WHERE product_id=?", (product_id,)).fetchall()
    reviews = conn.execute("SELECT * FROM reviews WHERE product_id=?", (product_id,)).fetchall()
    return render_template("product.html", product=product, images=images, reviews=reviews)

# Add review
@products_bp.route("/add_review/<int:product_id>", methods=["POST"])
def add_review(product_id):
    name = request.form.get("name")
    comment = request.form.get("comment")
    rating = request.form.get("rating")
    conn = get_db()
    conn.execute("INSERT INTO reviews (product_id,name,comment,rating) VALUES (?,?,?,?)",
                 (product_id, name, comment, rating))
    conn.commit()
    return redirect(f"/product/{product_id}")

# Quick view
@products_bp.route("/product_quick/<int:product_id>")
def product_quick(product_id):
    conn = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    images = conn.execute("SELECT * FROM product_images WHERE product_id=?", (product_id,)).fetchall()
    return render_template("product_quick.html", product=product, images=images)

# Delete product image
@products_bp.route("/delete_product_image/<int:image_id>")
def delete_product_image(image_id):
    conn = get_db()
    conn.execute("DELETE FROM product_images WHERE id=?", (image_id,))
    conn.commit()
    return redirect(request.referrer)

# Upload multiple images
@products_bp.route("/upload_product_images/<int:product_id>", methods=["POST"])
def upload_product_images(product_id):
    files = request.files.getlist("images")
    conn = get_db()
    for file in files:
        if file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join("static/uploads", filename))
            conn.execute("INSERT INTO product_images (product_id,image) VALUES (?,?)", (product_id, filename))
    conn.commit()
    return redirect("/products")