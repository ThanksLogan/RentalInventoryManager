import sqlite3
from datetime import datetime, timedelta


def delete_booking_rows(db_file, condition):
    """
    Delete rows from the bookings table based on a condition.

    :param db_file: Path to the SQLite database file
    :param condition: SQL condition for the rows to delete (e.g., "booking_id = 123")
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # SQL query to delete rows
        sql = f"DELETE FROM bookings WHERE {condition}"

        # Execute the query
        cursor.execute(sql)

        # Commit the changes
        conn.commit()

        print(f"Rows deleted: {cursor.rowcount}")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        if conn:
            # Close the database connection
            conn.close()

# Example usage
db_path = "path_to_your_database.db"
date = datetime(2023, 11, 1)
# Loop through November and December (61 days total)
for _ in range(61):
    #formatted_date = date.strftime('%Y-%m-%d')
    delete_booking_rows(db_path, formatted_date)
    date += timedelta(days=1)  # Increment the day by 1