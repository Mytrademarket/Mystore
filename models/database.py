import sqlite3
from flask import g

DATABASE = "database.db"


# ----------------------------------
# Get database connection
# ----------------------------------
def get_db():

    if "db" not in g:

        g.db = sqlite3.connect(DATABASE)

        g.db.row_factory = sqlite3.Row

    return g.db


# ----------------------------------
# Close database connection
# ----------------------------------
def close_db(e=None):

    db = g.pop("db", None)

    if db is not None:

        db.close()


# ----------------------------------
# Initialize database tables
# ----------------------------------
def init_db():

    conn = sqlite3.connect(DATABASE)

    conn.executescript("""

    CREATE TABLE IF NOT EXISTS product_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        image TEXT,
        FOREIGN KEY(product_id) REFERENCES products(id)
    );

    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        name TEXT,
        comment TEXT,
        rating INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    """)

    conn.commit()

    conn.close()