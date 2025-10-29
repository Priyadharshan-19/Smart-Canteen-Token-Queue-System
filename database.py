# database.py
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

# Initialize SQLAlchemy
db = SQLAlchemy()

# Base project directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)

# Shared absolute database path
DB_PATH = os.path.join(INSTANCE_DIR, "smartcanteen.db")

def init_menu_db():
    """Initializes menu table and adds default items if empty."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Create menu table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    ''')

    # Insert default items if empty
    c.execute("SELECT COUNT(*) FROM menu")
    count = c.fetchone()[0]

    if count == 0:
        menu_items = [
            ("Veg Meal", 50),
            ("Chicken Meal", 90),
            ("Sandwich", 40),
            ("Juice", 25),
            ("Fried Rice", 60),
            ("Parotta with Kurma", 70),
            ("Noodles", 55),
            ("Chapathi with Gravy", 50),
            ("Coffee", 20),
        ]
        c.executemany("INSERT INTO menu (item_name, price) VALUES (?, ?)", menu_items)
        conn.commit()
        print("✅ Database created and sample menu items added!")
    else:
        print("ℹ️ Menu table already populated.")

    conn.close()
