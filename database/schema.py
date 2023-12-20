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

def create_bookings_table(conn):
    """Create the bookings table in the SQLite database."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_entry_id INTEGER PRIMARY KEY,
                booking_id INTEGER,
                item_id INTEGER,
                quantity_booked INTEGER NOT NULL,
                from_date DATE NOT NULL,
                to_date DATE NOT NULL,
                FOREIGN KEY (item_id) REFERENCES inventory (item_id)
            );
        """)
        conn.commit()
    except Error as e:
        print(e)
