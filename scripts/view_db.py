from sqlite3 import Error
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from database.connection import create_connection
from database.operations import print_all_inventory_items, print_all_bookings

def view_inventory():
    # Define your database path
    database_path = "path_to_your_database.db"

    # Create a database connection
    conn = create_connection(database_path)

    # Print all inventory items
    if conn:
        print_all_inventory_items(conn)
        print_all_bookings(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == "__main__":
    view_inventory()
