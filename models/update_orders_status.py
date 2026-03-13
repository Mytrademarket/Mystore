import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Add status column (default 'Pending')
cursor.execute('''ALTER TABLE orders
ADD COLUMN status TEXT DEFAULT 'Pending'
''')

conn.commit()
conn.close()
print("Status column added!")