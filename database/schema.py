from sqlite3 import Error


def create_inventory_table(conn):
    """Create the inventory table in the SQLite database."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS furniture_items (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                quantity INTEGER,
                price REAL,
                booked INTEGER DEFAULT 0
            );
        """)
        conn.commit()
    except Error as e:
        print(e)
2