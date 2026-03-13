import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price REAL,
    description TEXT,
    image TEXT
)
''')

cursor.execute("INSERT INTO products (name, price, description, image) VALUES ('Phone', 300, 'Smartphone', 'phone.jpg')")
cursor.execute("INSERT INTO products (name, price, description, image) VALUES ('Laptop', 800, 'Gaming laptop', 'laptop.jpg')")
cursor.execute("INSERT INTO products (name, price, description, image) VALUES ('Shoes', 50, 'Running shoes', 'shoes.jpg')")

conn.commit()
conn.close()

print("Database created!")