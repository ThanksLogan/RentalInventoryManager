import sys
import os

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

from database.connection import create_connection
from database.schema import create_bookings_table

def initialize_db():
    # Define your database path
    database_path = "path_to_your_database.db"

    # Create a database connection
    conn = create_connection(database_path)

    # Create the inventory table
    if conn is not None:
        create_bookings_table(conn)
        print("Bookings table created successfully.")
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

if __name__ == "__main__":
    initialize_db()
