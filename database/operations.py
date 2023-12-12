from sqlite3 import Error


def create_inventory_item(conn, item):
    """
    Create a new item in the inventory table.
    :param conn: Connection object
    :param item: Tuple containing item details (name, quantity, price)
    """
    sql = '''INSERT INTO furniture_items(name, quantity, price)
             VALUES(?,?,?)'''
    try:
        cursor = conn.cursor()
        cursor.execute(sql, item)
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)

def select_all_inventory(conn):
    """
    Query all rows in the inventory table.
    :param conn: Connection object
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM furniture_items")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(e)

def print_all_inventory_items(conn):
    """
    Print all items in the inventory.
    :param conn: Connection object
    """
    try:
        items = select_all_inventory(conn)
        for item in items:
            print(f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}, Price: {item[3]}, Booked: {item[4]}")
    except Error as e:
        print(e)
