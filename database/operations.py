from sqlite3 import Error
import random


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


def create_booking(conn, items, from_date, to_date):
    """
    Create a new item in the booking table.
    :param conn: Connection object
    :param items: List of Tuples containing booking details [(name, quantity)]
    """
    # Now, we have to unpack the packages to get an individual item from them.
    # basically if it recognizes a package, it should push the items and their quantities to the back of the list of tuples.

    
    # for each time a create_booking is called, a unique booking number is assigned to it
    booking_id = generate_unique_8_digit_number()
    try: 
        cursor = conn.cursor()
        unpacked_items = []

        for item in items:
            print(item[0])
            match item[0]:
                case "V2_99":
                    unpacked_items.extend([(29591065, 2), (12775351, 2), (55453976, 2), (25942155, 1)])
                case "V2_100":
                    unpacked_items.extend([(29591065, 4), (12775351, 4), (55453976, 4), (25942155, 2)])
                case "V2_101":
                    unpacked_items.extend([(29591065, 8), (12775351, 8), (55453976, 8), (25942155, 4)])
                case _:
                    unpacked_items.append(item)
        print(unpacked_items)
        for unpacked_item in unpacked_items:
            #unique id for each piece within bigger booking id
            booking_entry_id = generate_unique_8_digit_number()
            cursor.execute(
                '''INSERT INTO bookings (booking_entry_id, booking_id, item_id, quantity, from_date, to_date)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (booking_entry_id, booking_id, unpacked_item[0], unpacked_item[1], from_date, to_date)
            )

        conn.commit() 
        return cursor.lastrowid
    except Error as e:
        print(e)
    print("HERE")
    

    
def generate_unique_8_digit_number():
    number = random.randint(10000000, 99999999)
    return number

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
