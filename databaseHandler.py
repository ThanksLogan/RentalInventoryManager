#here were going to add all of the items to sqlite inventory
import sqlite3

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn

conn = create_connection("path_to_your_database.db")


def create_table(conn, create_table_sql):
    """ Create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

# SQL statement for creating an inventory table
sql_create_inventory_table = """
CREATE TABLE IF NOT EXISTS inventory (
    id integer PRIMARY KEY,
    name text NOT NULL,
    quantity integer,
    price real,
    booked integer DEFAULT 0
);
"""

# Create inventory table
if conn is not None:
    create_table(conn, sql_create_inventory_table)
else:
    print("Error! Cannot create the database connection.")

def create_inventory_item(conn, item):
    """
    Create a new item into the inventory table
    :param conn:
    :param item:
    :return: item id
    """
    sql = ''' INSERT INTO inventory(name,quantity,price)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, item)
    conn.commit()
    return cur.lastrowid


def select_all_inventory(conn):
    """
    Query all rows in the inventory table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM inventory")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def view_all_inventory_items(db_file):
    # Create a database connection
    conn = create_connection(db_file)

    if conn:
        # Query and print all inventory items
        select_all_inventory(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")

# Call the function with your database file path
view_all_inventory_items("path_to_your_database.db")
