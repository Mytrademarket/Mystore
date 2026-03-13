import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# -----------------------------
# Create categories table
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
)
""")

# -----------------------------
# Add category_id column to products if not exists
# -----------------------------
try:
    cursor.execute("ALTER TABLE products ADD COLUMN category_id INTEGER")
except sqlite3.OperationalError:
    pass  # column already exists

# -----------------------------
# Add stock column to products if not exists
# -----------------------------
try:
    cursor.execute("ALTER TABLE products ADD COLUMN stock INTEGER DEFAULT 0")
except sqlite3.OperationalError:
    pass  # column already exists

cursor.execute(
    "INSERT OR IGNORE INTO site_settings (key,value) VALUES (?,?)",
    ("homepage_content","")
)

# -----------------------------
# Create site_settings table for logo
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS site_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT
)
""")

# Insert default logo if not exists
cursor.execute("INSERT OR IGNORE INTO site_settings (key, value) VALUES (?, ?)", 
               ("logo", "default_logo.png"))

# -----------------------------
# Create orders table
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    address TEXT NOT NULL,
    total REAL NOT NULL,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# -----------------------------
# Create order_items table
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY(order_id) REFERENCES orders(id)
)
""")

# -----------------------------
# Add quantity column if missing (for old database)
# -----------------------------
try:
    cursor.execute("ALTER TABLE order_items ADD COLUMN quantity INTEGER DEFAULT 1")
except sqlite3.OperationalError:
    pass

# -----------------------------
# Create customers table
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# -----------------------------
# Add customer_id to orders
# -----------------------------
try:
    cursor.execute("ALTER TABLE orders ADD COLUMN customer_id INTEGER")
except sqlite3.OperationalError:
    pass

# -----------------------------
# Insert footer & social settings
# -----------------------------

settings = [
    ("facebook",""),
    ("instagram",""),
    ("twitter",""),
    ("tiktok",""),
    ("youtube",""),
    ("footer_about",""),
    ("footer_contact_phone",""),
    ("footer_contact_email",""),
    ("footer_address",""),
    ("privacy_policy_page","/privacy-policy"),
    ("terms_page","/terms"),
    ("refund_page","/refund-policy"),
    ("shipping_page","/shipping-policy"),
    ("contact_page","/contact"),
    ("faq_page","/faq"),
    ("popup_enabled","0"),
    ("popup_title",""),
    ("popup_text",""),
    ("popup_button_text",""),
    ("popup_button_link",""),
('store_name','My Online Store'),
('store_email',''),
('store_phone',''),
('store_address',''),
('favicon',''),
('whatsapp',''),
('google_analytics','')
]

for key,value in settings:
    cursor.execute(
        "INSERT OR IGNORE INTO site_settings (key,value) VALUES (?,?)",
        (key,value)
    )

# -----------------------------
# Pages table (CMS pages)
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    slug TEXT UNIQUE,
    title TEXT,
    content TEXT
)
""")

# Default pages
pages = [
    ("privacy-policy", "Privacy Policy"),
    ("terms", "Terms & Conditions"),
    ("refund-policy", "Refund Policy"),
    ("shipping-policy", "Shipping Policy"),
    ("contact", "Contact"),
    ("faq", "FAQ")
]

for slug,title in pages:
    cursor.execute(
        "INSERT OR IGNORE INTO pages (slug,title,content) VALUES (?,?,?)",
        (slug,title,"Edit this page from admin dashboard")
    )



conn.commit()
conn.close()

print("Database updated successfully!")