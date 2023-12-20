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


def create_booking(conn, item):
    """
    Create a new item in the inventory table.
    :param conn: Connection object
    :param item: Tuple containing item details (name, quantity, price)
    """
    # Example: Adding a booking with two different items
    #booking_id = generate_new_booking_id()  # Implement this function
    booking_items = [
    {"item_id": 1, "quantity": 2},
    {"item_id": 3, "quantity": 1}
    ]
    '''
    for item in booking_items:
        cursor.execute(
            "INSERT INTO bookings (booking_id, item_id, quantity_booked, from_date, to_date) VALUES (?, ?, ?, ?, ?)",
            ("1234", item['item_id'], item['quantity'], '2023-12-18', '2023-12-19')
        )      
    '''

    sql = '''INSERT INTO bookings(booking_id, item_id, quantity_booked, from_date, to_date)
             VALUES (?, ?, ?, ?, ?)
             '''
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql, item)
        conn.commit()
        return cursor.lastrowid
    except Error as e:
        print(e)
    

def select_all_bookings(conn):
    """
    Query all rows in the bookings table.
    :param conn: Connection object
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM bookings")
        rows = cursor.fetchall()
        return rows
    except Error as e:
        print(e)

def print_all_bookings(conn):
    """
    Print all items in the bookings.
    :param conn: Connection object
    """
    try:
        items = select_all_bookings(conn)
        for item in items:
            print(f"booking entry id: {item[0]}, booking: {item[1]}, item id: {item[2]}, quantity booked: {item[3]}, from date: {item[4]}, to date: {item[5]}")
    except Error as e:
        print(e)
