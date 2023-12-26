from sqlite3 import Error
import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from database.connection import create_connection
from database.operations import create_inventory_item
from database.operations import create_booking

def add_item():
    # Define your database path
    database_path = "path_to_your_database.db"

    # Create a database connection
    conn = create_connection(database_path)

    # Print all inventory items
    if conn:
        create_inventory_item(conn, ("test item", "1", "1"))

        conn.close()
    else:
        print("Error! Cannot insert into database.")

if __name__ == "__main__":
    add_item()