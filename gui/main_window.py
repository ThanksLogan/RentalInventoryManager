from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QListWidgetItem, QListWidget, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFontDatabase
from PyQt5 import QtGui 
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer

from .fancyWindow import CustomTitleBar  # Importing CustomTitleBar

from .add_event_dialog import AddEventDialog
from business_logic import package_definitions
from database.operations import create_booking, get_available_quantity
from scripts import view_db
from database.connection import create_connection
import os
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window to frameless
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set custom window title
        self.title_bar = CustomTitleBar(self)
        self.setMenuWidget(self.title_bar) 

        ui_path = os.path.join(os.path.dirname(__file__), 'LujoIMS_UI_v1.2.ui')
        uic.loadUi(ui_path, self)

        '''Initializations'''
        # Mapping from item name to ID
        self.item_to_id = {
            "Package: V2 Lounge 99": "V2_99",
            "Package: V2 Lounge 100": "V2_100",
            "Package: V2 Lounge 101": "V2_101",
            "Package: V2 Lounge 98": "V2_98",
            "Package: Legacy Lounge 99": "L_99",
            "Package: Legacy Lounge 100": "L_100",
            "Package: Legacy Lounge 101": "L_101",
            "Package: Legacy Lounge Silver": "L_Silver",
            "Package: Legacy Lounge Bronze": "L_Bronze",
            "Package: Legacy Lounge Gold": "L_Gold",
            "Legacy Backed Ottoman": "10125473",
            "Legacy Big Ottoman": "92857097",
            "Legacy Corner Chair": "63321077",
            "Legacy Square": "90442326",
            "Legacy Armless Chair": "42212173",
            "Legacy Ottoman": "18612390",
            "Legacy Rectangle": "16177294",
            "V2 Ottoman": "12775351",
            "V2 Corner Chair": "25942155",
            "V2 Armless Chair": "29591065",
            "V2 Square": "55453976"
            # ... other mappings ...
        }
        # Create reverse mapping from ID to item name
        self.id_to_item = {v: k for k, v in self.item_to_id.items()}
        # lists of packages with items and their quantities
        # order: armless, ottoman, squares, corners, TODO: LED cubes
        self.v2_98 = [(12775351, 2), (55453976, 4)]
        self.v2_99 = [(29591065, 2), (12775351, 2), (55453976, 2), (25942155, 1)]
        self.v2_100 = [(29591065, 4), (12775351, 4), (55453976, 4), (25942155, 2)]
        self.v2_101 = [(29591065, 8), (12775351, 8), (55453976, 8), (25942155, 4)]

        self.legacy_99 = [(42212173, 2), (18612390, 2), (55453976, 2), (63321077, 1)]
        self.legacy_100 = [(42212173, 4), (18612390, 4), (55453976, 4), (63321077, 2)]
        self.legacy_101 = [(42212173, 8), (18612390, 8), (55453976, 8), (63321077, 4)]
        self.legacy_bronze = [(10125473,1), (92857097,1), (16177294,4)]
        self.legacy_silver = [(10125473,2), (92857097,2), (16177294,4)]
        self.legacy_gold = [(10125473,4), (92857097,4), (16177294,8)]

        # order: bench, serp, circle (except for ultra 98 its all round) 
        # TODO: LED cubes
        self.ultra_98 = [(92857099, 3)]
        self.ultra_99 = [(92857100, 2), (92857101, 2), (92857099, 1)]
        self.ultra_100 = [(92857100, 4), (92857101, 4), (92857099, 2)]
        self.ultra_101 = [(92857100, 8), (92857101, 8), (92857099, 4)]
        self.package_configurations = {
            "Package: V2 Lounge 98": self.v2_98,
            "Package: V2 Lounge 99": self.v2_99,
            "Package: V2 Lounge 100": self.v2_100,
            "Package: V2 Lounge 101": self.v2_101,

            "Package: Legacy Lounge 99": self.legacy_99,
            "Package: Legacy Lounge 100": self.legacy_100,
            "Package: Legacy Lounge 101": self.legacy_101,

            "Package: Legacy Bronze": self.legacy_bronze,
            "Package: Legacy Silver": self.legacy_silver,
            "Package: Legacy Gold": self.legacy_gold,

            "Package: Ultra Lounge 98": self.ultra_98,
            "Package: Ultra Lounge 99": self.ultra_99,
            "Package: Ultra Lounge 100": self.ultra_100,
            "Package: Ultra Lounge 101": self.ultra_101,   
        }
        self.package_contents = {
            "Package: V2 Lounge 98": {"V2 Ottoman": 2, "V2 Square": 4},
            "Package: V2 Lounge 99": {"V2 Armless Chair": 2, "V2 Ottoman": 2, "V2 Square": 2, "V2 Corner Chair": 1},
            "Package: V2 Lounge 100": {"V2 Armless Chair": 4, "V2 Ottoman": 4, "V2 Square": 4, "V2 Corner Chair": 2},
            "Package: V2 Lounge 101": {"V2 Armless Chair": 8, "V2 Ottoman": 8, "V2 Square": 8, "V2 Corner Chair": 4},
            "Package: Legacy Lounge 99": {"Legacy Armless Chair": 2, "Legacy Ottoman": 2, "Legacy Square": 2, "Legacy Corner Chair": 1},
            "Package: Legacy Lounge 100": {"Legacy Armless Chair": 4, "Legacy Ottoman": 4, "Legacy Square": 4, "Legacy Corner Chair": 2},
            "Package: Legacy Lounge 101": {"Legacy Armless Chair": 8, "Legacy Ottoman": 8, "Legacy Square": 8, "Legacy Corner Chair": 4},

        }

        # Connect itemClicked signal
        self.currentlySelectedListWidget.itemClicked.connect(self.on_currentlySelectedItemClicked)
        self.currentlySelectedListItem = None  # Variable to hold the currently selected item

        self.selected_item_name = None  # Initialize selected_item_name
        self.saved_items = None

        

        self.init_ui()
        #self.currently_selected_item = None  # Attribute to store the selected item

    def init_ui(self):
        self.apply_stylesheet() 
        self.label.setPixmap(QtGui.QPixmap("C:/InventoryManager/RentalInventoryManager/gui/qt images/lujoLogo.png"))
# C:\InventoryManager\RentalInventoryManager\gui
        # database connection
        self.conn = create_connection("db.db")

        # Connect the calendar widgets to update methods
        self.fromDateCalendar.selectionChanged.connect(self.update_from_date_time)
        self.toDateCalendar.selectionChanged.connect(self.update_to_date_time)

        # Assuming the object names are fromDateCalendar, toDateCalendar, and viewAvailabilityButton
        # Connect the View Availability button
        self.loginPushButton.clicked.connect(self.on_login)
        self.viewAvailabilityButton.clicked.connect(self.on_view_availability)

        # Initialize attributes for the selected dates
        self.from_date = None
        self.to_date = None
        # Connect to the signal when the current page changes
        self.stackedWidget.currentChanged.connect(self.onPageChanged)

        self.populate_list_widget()

        # Connect the itemClicked signal of each QListWidget in the tabs
        self.v2ListWidget.itemClicked.connect(self.on_item_selected)
        self.legacyListWidget.itemClicked.connect(self.on_item_selected)
        self.ultraListWidget.itemClicked.connect(self.on_item_selected)
        # Repeat for other QListWidgets in other tabs

        #Connect the Buttons
        self.backPushButton.clicked.connect(self.on_back_clicked)
        self.addPushButton.clicked.connect(self.on_add_item_clicked)
        self.removePushButton.clicked.connect(self.on_remove_item_clicked)
        self.doneButton.clicked.connect(self.on_done_clicked)
        self.confirmButton.clicked.connect(self.on_confirm_button_clicked)

    def apply_stylesheet(self):
        # Load the Inter font family
        QFontDatabase.addApplicationFont("C:/Users/forem/Downloads/static/Inter-Black.ttf")
        QFontDatabase.addApplicationFont("C:/Users/forem/Downloads/static/Inter-Bold.ttf")
        QFontDatabase.addApplicationFont("C:/Users/forem/Downloads/static/Inter-ExtraBold.ttf")
        QFontDatabase.addApplicationFont("C:/Users/forem/Downloads/static/Inter-ExtraLight.ttf")
        QFontDatabase.addApplicationFont("C:/Users/forem/Downloads/static/Inter-Light.ttf")
        QFontDatabase.addApplicationFont("C:/Users/forem/Downloads/static/Inter-Medium.ttf")
        QFontDatabase.addApplicationFont("C:/Users/forem/Downloads/static/Inter-Regular.ttf")
        QFontDatabase.addApplicationFont("C:/Users/forem/Downloads/static/Inter-SemiBold.ttf")
        QFontDatabase.addApplicationFont("C:/Users/forem/Downloads/static/Inter-Thin.ttf")
        # Define your CSS styles
        css = """
        QMainWindow {
            background-color: #333; /* Dark background color */
            border: 1px solid #444; /* Custom border color and thickness */
            border-radius: 8px; /* Rounded corners for the window */
            /* Additional styling options can be added here */
        }

        QMenuBar {
            background-color: #444; /* Dark background for menu bar */
            color: white; /* Text color for menu bar */
            /* Additional styling for menu bar */
        }

        QMenuBar::item {
            background-color: transparent; /* Transparent background for menu items */
            padding: 4px 8px; /* Padding for menu items */
        }

        QMenuBar::item:selected {
            background-color: #555; /* Background color for selected menu items */
        }

        QStatusBar {
            background-color: #444; /* Dark background for status bar */
            color: white; /* Text color for status bar */
            /* Additional styling for status bar */
        }

        /* You can add more specific styles for other widgets and controls here */

        QWidget#Form {
            background-color: #121212; /* Dark background color */
        }
        QGraphicsView#graphicsView {
           background-color: #252525; /* Slightly lighter dark background */
        }
        /* Styles for the main graphics view background */
        #graphicsView_2 {
            background-color: #121212; /* Dark grey background */
        }

        /* Styles for the main title label */
        QLabel#label_6 {
            color: white; /* White text for better contrast on dark background */
            font-family: 'Inter-Bold', sans-serif;
            font-size: 12pt; /* Adjust size as needed */
            text-align: center; /* Center the text */
            padding: 10px; /* Add some padding */
        }

        /* Styles for lines */
        Line {
            background-color: #333333; /* Dark line color */
        }

        /* Styles for buttons */
        QPushButton {
            border: 2px solid #6c6c6c;
            border-radius: 5px;
            background-color: #353535; /* Dark grey background */
            color: #DDDDDD; /* Light grey text */
            font-family: 'Inter-Bold', sans-serif;
            font-size: 10pt;
            padding: 5px;
        }
        
        QPushButton:hover {
            background-color: #434343; /* Slightly lighter grey for hover */
        }

        QPushButton:pressed {
            background-color: #5c5c5c; /* Even lighter grey for pressed */
        }

        

        /* Styles for spin boxes */
        QSpinBox {
            background-color: #454545;
            color: #DDDDDD;
            font-family: 'Inter', sans-serif;
            font-size: 10pt;
            border: 1px solid #6c6c6c;
            border-radius: 5px;
        }
        

        /* Styles for text edits */
        QTextEdit {
            background-color: #252525;
            color: #DDDDDD;
            font-family: 'Inter', sans-serif;
            font-size: 10pt;
            border: 1px solid #6c6c6c;
            border-radius: 5px;
        }

        /* Styles for table widgets */
        QTableWidget {
            background-color: #252525;
            color: #DDDDDD;
            font-family: 'Inter', sans-serif;
            font-size: 9pt;
            border: 1px solid #6c6c6c;
            border-radius: 5px;
        }

                /* Styles for DateTimeEdit Widgets */
        QDateTimeEdit {
            background-color: #454545;
            color: #DDDDDD;
            border: 1px solid #6c6c6c;
            border-radius: 5px;
            font-size: 10pt;
        }

        QTableWidget {
            background-color: #252525; /* Dark grey background */
            color: #DDDDDD; /* Light grey text for better contrast */
            font-family: 'Inter-Regular', sans-serif;
            font-size: 9pt; /* Adjust the font size as needed */
            border-radius: 5px; /* Rounded corners */
            border: 1px solid #6c6c6c; /* Border for the table */
        }

        QTableWidget QHeaderView::section {
            background-color: #353535; /* Darker grey for header */
            color: white; /* White text in header */
            padding: 5px;
            border: 1px solid #6c6c6c; /* Border for header cells */
            font-family: 'Inter-Medium', sans-serif; /* Slightly bolder font for headers */
        }

        QTableWidget::item {
            background-color: #252525; /* Dark grey background for items */
            color: #DDDDDD; /* Light grey text for items */
        }

        QTableWidget::item:selected {
            background-color: #434343; /* Slightly lighter grey for selected items */
            color: white; /* White text for selected items */
        }



        """
        self.setStyleSheet(css)

    def get_item_id(self, item_name):
        return self.item_to_id.get(item_name, 0)

    def get_item_name(self, item_id):
        return self.id_to_item.get(item_id, "Unknown")

    def onPageChanged(self, index):
        # Check if the current page is page 2
        if index == 1:
            self.existingBookingsListWidget.clear()
        if index == 2:  # Assuming page 2 is at index 1
            self.show_existing_bookings()

    def on_back_clicked(self):
        self.stackedWidget.setCurrentIndex(1)  # Assuming page 3 is at index 2

    def update_from_date_time(self):
        selected_date = self.fromDateCalendar.selectedDate()
        self.fromDateTimeEdit.setDateTime(selected_date.startOfDay())
    def update_to_date_time(self):
        selected_date = self.toDateCalendar.selectedDate()
        self.toDateTimeEdit.setDateTime(selected_date.startOfDay())

    def on_login(self):
        if self.userLineEdit.text() == "admin" and self.passwordLineEdit.text() == "password":
            self.stackedWidget.setCurrentIndex(1)
        else:
            print("Invalid Credentials. Try 'admin' and 'password'")

    def on_view_availability(self):
        # Get the selected dates from the calendar widgets
        self.from_date = self.fromDateCalendar.selectedDate()
        self.to_date = self.toDateCalendar.selectedDate()

        # Check if both dates are selected
        if self.from_date and self.to_date:
            # Switch to the second page of the QStackedWidget
            self.stackedWidget.setCurrentIndex(2)
        else:
            # Handle the case where one or both dates are not selected
            print("Please select both 'from' and 'to' dates.")

    def on_currentlySelectedItemClicked(self, item):
        # Update the currently selected item
        self.currentlySelectedListItem = item

    def populate_list_widget(self):
        """
        Populate list widgets for different furniture categories (V2, Legacy, and Ultra)
        with items fetched from respective methods.
        """
        # Populating v2ListWidget with items from the V2 category
        for item_name in self.fetch_v2():
            item = QListWidgetItem(item_name)
            self.v2ListWidget.addItem(item)

        # Populating legacyListWidget with items from the Legacy category
        for item_name in self.fetch_legacy():
            item = QListWidgetItem(item_name) 
            self.legacyListWidget.addItem(item)

        # Populating ultraListWidget with items from the Ultra category
        for item_name in self.fetch_ultra():
            item = QListWidgetItem(item_name) 
            self.ultraListWidget.addItem(item)

        # Connecting item clicked signals to the handler for each category
        self.v2ListWidget.itemClicked.connect(self.on_item_clicked)
        self.legacyListWidget.itemClicked.connect(self.on_item_clicked)
        self.ultraListWidget.itemClicked.connect(self.on_item_clicked)

    def show_existing_bookings(self):
        """
        Retrieve and display existing bookings from the database
        that fall within the selected date range.
        """
        cursor = self.conn.cursor()
        from_date_string = self.from_date.toString("yyyy-MM-dd")
        to_date_string = self.to_date.toString("yyyy-MM-dd")

        # SQL query to find bookings that overlap with the selected date range
        query = '''
        SELECT booking_id, item_id, quantity FROM bookings
        WHERE (from_date <= ? AND to_date >= ?) 
        OR (from_date <= ? AND to_date >= ?)
        '''
        cursor.execute(query, (from_date_string, from_date_string, to_date_string, to_date_string))

        # Process each booking and add it to the existingBookingsListWidget
        bookings = cursor.fetchall()
        for booking in bookings:
            booking_number, item_id, quantity = booking
            item_name = self.get_item_name(str(item_id))
            booking_info = '{}: {}  Q: {}'.format(booking_number, item_name, quantity)
            self.existingBookingsListWidget.addItem(booking_info)

        cursor.close()

    def fetch_v2(self):
        """
        Return a list of V2 category furniture items.
        """
        return ["Package: V2 Lounge 98", "Package: V2 Lounge 99", "Package: V2 Lounge 100", "Package: V2 Lounge 101", 
                "V2 Armless Chair", "V2 Corner Chair", "V2 Ottoman", "V2 Square"]

    def fetch_legacy(self):
        """
        Return a list of Legacy category furniture items.
        """
        return ["Package: Legacy Lounge 99","Package: Legacy Lounge 100","Package: Legacy Lounge 101",
                "Package: Legacy Bronze", "Package: Legacy Silver", "Package: Legacy Gold", 
                "Legacy Armless Chair", "Legacy Corner Chair", "Legacy Ottoman", "Legacy Square",
                "Legacy Big Ottoman", "Legacy Backed Ottoman", "Legacy Rectangle"]

    def fetch_ultra(self):
        """
        Return a list of Ultra category furniture items.
        """
        return ["Package: Ultra Lounge 98", "Package: Ultra Lounge 99","Package: Ultra Lounge 100","Package: Ultra Lounge 101", 
                "Ultra Bench", "Ultra Serpentine", "Ultra Round"]

    def on_item_clicked(self, item):
        """
        Show on terminal when an item in the list widget is clicked.
        """
        print("Clicked item:", item.text())
        self.currently_selected_item = item

    def on_item_selected(self):
        """
        Handle the selection of an item in the list widget and 
        adjust the maximum available quantity for that item.
        """
        # Get the currently active list widget and its selected item
        current_list_widget = self.get_active_list_widget()
        selected_item = current_list_widget.currentItem()
        
        if selected_item:
            self.selected_item_name = selected_item.text()
        else:
            self.selected_item_name = None
        print(self.selected_item_name)

        # Calculate the maximum quantity available for the selected item
        max_quantity = self.get_max_quantity(self.selected_item_name)

        # Check if the item is already present in the currentlySelectedListWidget
        # and adjust the available quantity accordingly        
        for i in range(self.currentlySelectedListWidget.count()):
            item_widget = self.currentlySelectedListWidget.item(i)
            item_text = item_widget.text()
            selected_item, selected_qty = self.parse_selected_item(item_text)
            max_quantity = self.adjust_quantity_based_on_selection(selected_item, selected_qty, max_quantity)
        
        # Update the maximum quantity and enable/disable the add button accordingly
        self.spinBox.setMaximum(max(max_quantity, 0))
        self.addPushButton.setEnabled(max_quantity>0)

    def get_max_quantity(self, item_name):
        '''     
        Calculate the maximum available quantity for a given item name.
        '''
        if item_name and item_name[0] == 'P':  # Check if it's a package
            return self.unpack_and_get_max_quantity(item_name)
        else:
            return get_available_quantity(self.conn, self.get_item_id(item_name), 
                                        self.from_date.toString("yyyy-MM-dd"), 
                                        self.to_date.toString("yyyy-MM-dd"))

    def parse_selected_item(self, item_text):
        """
        Parse the item text to get the item name and quantity
        """
        parts = item_text.split(" - Quantity: ")
        item_name = parts[0]
        quantity = int(parts[1]) if len(parts) > 1 else 0
        return item_name, quantity

    def adjust_quantity_based_on_selection(self, selected_item, selected_qty, max_quantity):
        """
        Adjust the maximum quantity based on the already selected items.
        """
        if selected_item in self.package_contents:
            # Adjust quantity for each item in the package
            for item, qty in self.package_contents[selected_item].items():
                max_quantity = self.calculate_new_max(item, qty * selected_qty, max_quantity)
        else:
            # Directly adjust quantity for individual items
            max_quantity = self.calculate_new_max(selected_item, selected_qty, max_quantity)
        return max_quantity

    def calculate_new_max(self, item, qty, max_quantity):
        """
        Recalculate the maximum available quantity based on current selections.
        """
        for i in range(self.currentlySelectedListWidget.count()):
            widget_text = self.currentlySelectedListWidget.item(i).text()
            widget_item, widget_qty = self.parse_selected_item(widget_text)
            if widget_item == item or (widget_item in self.package_contents and item in self.package_contents[widget_item]):
                max_quantity -= widget_qty
        return max_quantity
        
    def unpack_and_get_max_quantity(self, item_name):
        ''' 
        Determine the maximum number of packages that can be created
        based on the available quantity of items in the package.
        (Handle item_and_inStock here [8,8,8,4,4] for example)
        '''
         # Get the package configuration based on item_name
        package_configuration = self.package_configurations.get(item_name)
        
        if package_configuration is None:
            return 0  # Handle the case where the package configuration is not found

        item_and_inStock = self.loop_and_unpack(package_configuration)
        if(item_and_inStock[1] == False):
            return 0
        else:
            item_list = item_and_inStock[0] # in format [q1,q2,q3,q4]
            # WeakLink: Minimum item count to make up a package
            weakLink = item_list[0] // package_configuration[0][1]
            for i, item_amount in enumerate(item_list):
                quantity = item_amount // package_configuration[i][1]
                weakLink = min(weakLink, quantity)
            print(weakLink, item_and_inStock[1])
            return weakLink
        
    def loop_and_unpack(self, pkg):
        """
        Loop through each item in a package and calculate its available quantity.
        """       
        quantities = []
        enough = True
        for item in pkg:
            quantity = get_available_quantity(self.conn, item[0], 
                                            self.from_date.toString("yyyy-MM-dd"),
                                            self.to_date.toString("yyyy-MM-dd"))
            if quantity is None or quantity < item[1]:
                print(f"not enough of item_id: {item[0]}")
                enough = False # Cannot make an entire package due to quantity
                # Consider breaking out of the loop if one item is not enough
            else:
                quantities.append(quantity)  
        return (quantities, enough)
    
    def on_add_item_clicked(self):
        """
        Handle the event when the 'Add Item' button is clicked.
        This function adds the selected item along with its quantity 
        to the currentlySelectedListWidget.
        """
        # Checks if an item has been selected and the quantity is more than 0
        if self.selected_item_name is not None and self.spinBox.value() > 0:
            quantity = self.spinBox.value()
            item_with_quantity = f"{self.selected_item_name} - Quantity: {quantity}"

            # Add the selected item's text to the currentlySelectedListWidget
            self.currentlySelectedListWidget.addItem(item_with_quantity)

            # Clear the currently selected item to be init. again
            self.selected_item_name = None
        else:
            # Case for no item selected or zero in quantity field
            if self.selected_item_name is None:
                print("No item selected")  # Or show a message to the user
            else:
                print("Quantity cannot be zero")  # Or show a message to the user

    def on_remove_item_clicked(self):
        """
        Handle the event when the 'Remove Item' button is clicked.
        This function removes the currently selected item from 
        the currentlySelectedListWidget.
        """
        if self.currentlySelectedListItem:
            # Remove the selected item from the list
            row = self.currentlySelectedListWidget.row(self.currentlySelectedListItem)
            self.currentlySelectedListWidget.takeItem(row)

            # Reset the currently selected item
            self.currentlySelectedListItem = None
        else:
            print("No item selected to remove")

    def get_active_list_widget(self):
        """
        Return the active QListWidget based on the currently selected tab.
        """
        # Returns the QListWidget corresponding to the current tab
        current_tab_index = self.tabWidget.currentIndex()
        if current_tab_index == 0:
            return self.v2ListWidget
        elif current_tab_index == 1:
            return self.ultraListWidget
        elif current_tab_index == 2:
            return self.legacyListWidget
        # TODO: Add more conditions for other tabs
        else:
            return None

    def on_done_clicked(self):
        """
        Handle the event when the 'Done' button is clicked.
        This function saves the current selections and proceeds to create bookings.
        """
        # Save the current state of the currentlySelectedListWidget
        self.saved_items = []
        for i in range(self.currentlySelectedListWidget.count()):
            item_text = self.currentlySelectedListWidget.item(i).text()
            self.saved_items.append(item_text)

        items_to_process = []
        for i in range(self.currentlySelectedListWidget.count()):
            item_text = self.currentlySelectedListWidget.item(i).text()
            item_name, item_quantity = self.parse_item_and_quantity(item_text)
            item_id = self.get_item_id(item_name)
            items_to_process.append((item_id, item_quantity))
        
        # Items to book list will look like: [(10125473, 4), ("V299", 1)] <- list of tuples
        # Calls database function to create booking on processed items
        self.create_booking(items_to_process)
        self.stackedWidget.setCurrentIndex(3) # Move to new page
        self.populate_summary_table()

        
    def parse_item_and_quantity(self, item_text):
        """
        Parse a text string to extract the item name and quantity.
        """
        name_part, quantity_part = item_text.split(" - Quantity: ")
        quantity = int(quantity_part)
        return name_part, quantity

    def get_item_id(self, item_name):
        """
        Retrieve the unique ID associated with a given item name.
        This ID is used for database and internal logic operations.
        """
        match item_name: # TODO: add id for LED: 56556348
            case "Package: V2 Lounge 99":
                return "V2_99"
            case "Package: V2 Lounge 100":
                return "V2_100"
            case "Package: V2 Lounge 101":
                return "V2_101"
            case "Package: V2 Lounge 98":
                return "V2_98"
            case "Legacy Backed Ottoman":
                return "10125473"
            case "Legacy Big Ottoman":
                return "92857097"
            case "Legacy Corner Chair":
                return "63321077"
            case "Legacy Square":
                return "90442326"
            case "Legacy Armless Chair":
                return "42212173"
            case "Legacy Ottoman":
                return "18612390"
            case "Legacy Rectangle":
                return "16177294"
            case "V2 Ottoman":
                return "12775351"
            case "V2 Corner Chair":
                return "25942155"
            case "V2 Armless Chair":
                return "29591065"
            case "V2 Square":
                return "55453976"
            case _:
                return 0      

    #param: items_to_book: tuple (item(id), quantity)
    def create_booking(self, items_to_book):
        """
        Create a booking entry in the database with the selected items and their quantities.
        """
        from_date_string = self.from_date.toString("yyyy-MM-dd")
        to_date_string = self.to_date.toString("yyyy-MM-dd")
        # print(from_date_string, to_date_string) # Error checking in terminal
        create_booking(self.conn, items_to_book, from_date_string, to_date_string)

    def populate_summary_table(self):
        """
        Populate the summary table with the items selected for booking.
        Each row in the table will display the item name, quantity, and calculated price.
        """
        # Clear the table before adding new items
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Item", "Quantity", "Price"])

        for item_text in self.saved_items:
            row_count = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_count)

            item_name, item_quantity = self.parse_item_and_quantity(item_text)
            price = self.calculate_price(item_name, item_quantity)

            item_widget = QTableWidgetItem(item_name)
            quantity_widget = QTableWidgetItem(str(item_quantity))
            price_widget = QTableWidgetItem(f"${price:.2f}")

            self.tableWidget.setItem(row_count, 0, item_widget)
            self.tableWidget.setItem(row_count, 1, quantity_widget)
            self.tableWidget.setItem(row_count, 2, price_widget)
        
        self.adjust_table_row_heights() # Fits content easier

    def adjust_table_row_heights(self):
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.resizeRowToContents(row)

    def calculate_price(self, item_name, quantity):
        """
        Calculate the price for a given item and quantity.
        The price is determined based on the item type and its quantity.
        """
        price = self.get_price(item_name, quantity)
        return price 
    
    def get_price(self, item_name, quantity):
        """
        Fetch the price of an item from the database or a predefined list.
        This function handles different pricing logic for packages and individual items.
        """
        price = 0
        if item_name.startswith('P'): # Checks if its a package shortcut
            match item_name:
                case "Package: V2 Lounge 99":
                    price = 360.00
                case "Package: V2 Lounge 100":
                    price = 695.00
                case "Package: V2 Lounge 101":
                    price = 1095.00
                case "Package: V2 Lounge 98":
                    price = 270.00
                case "Package: Legacy Lounge 99":
                    price = 360.00
                case "Package: Legacy Lounge 100":
                    price = 695.00
                case "Package: Legacy Lounge 101":
                    price = 1095.00
        else:
            # NOT a package, so fetches item individually from DB.
            id = self.get_item_id(item_name)
            cursor = self.conn.cursor()
            query = "SELECT price FROM furniture_items WHERE item_id = ?"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            price = result[0] if result else 0

        return price * quantity

    def on_confirm_button_clicked(self):
        """
        Upon the user clicking confirm data from forms are saved to finalize the
        booking which includes saving the booking and generating a rental agreement
        """
        # Collect data from LineEdits forms, conjoined for use
        line_edit_data = [
            self.lineEdit_1.text(), 
            self.lineEdit_2.text(), 
            self.lineEdit_3.text(),
            self.lineEdit_4.text(),
            self.lineEdit_5.text(),
            self.lineEdit_6.text(),
            self.lineEdit_7.text(),
            self.lineEdit_8.text(),
            self.lineEdit_9.text()
            ]
        # Collect data from QTableWidget
        table_data = []
        for row in range(self.tableWidget.rowCount()):
            row_data = []
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                row_data.append(item.text() if item else "")
            table_data.append(row_data)

        # Generating HTML mockup of rental agreement
        html_content = self.generate_html_content(line_edit_data, self.tableWidget)

        file_name, _ = QFileDialog.getSaveFileName(self, "Save Agreement", "", "HTML Files (*.html)")
        if file_name:
            with open(file_name, 'w') as file:
                file.write(html_content)

    def generate_html_content(self, line_edit_data, table_widget):
        """
        Generates html page using css file, and fills empty boxes with
        user defined data from page 3.
        """
        with open('gui/css/modern_style.css', 'r') as css_file:
            css_content = css_file.read()    
        
        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
            {css_content}
            </style>
            <title>Rental Agreement</title>
        </head>
        <body>
            <div class="agreement-container">
                <h1>Rental Agreement</h1>
                    <p>By signing this agreement, the Customer (hereinafter referred to as "the Renter") agrees to the following terms and conditions:</p>
                    <ol>
                        <li>The Renter agrees to take proper care of the rented items and ensure they are used in a manner consistent with their intended purpose.</li>
                        <li>The Renter acknowledges that the items are in good condition at the time of rental and agrees to return them in the same condition, barring normal wear and tear.</li>
                        <li>The Renter agrees to be fully responsible for the loss or any damage to the rented items during the rental period.</li>
                        <li>In case of damage or loss, the Renter agrees to compensate the rental company at the current replacement value of the items.</li>
                        <li>The Renter shall not sublease or transfer the rented items to any other party without the prior written consent of the rental company.</li>
                        <li>The Renter agrees to use the items safely and adhere to all laws and regulations related to the use of such items.</li>
                        <li>The rental company is not responsible for any accidents or injuries caused by the use or misuse of the rented items.</li>
                        <li>The Renter agrees to return the items on or before the agreed-upon return date. Late returns may be subject to additional fees.</li>
                    </ol>

                <h2>Customer Information</h2>
                <p>Name: {line_edit_data[0]}</p>
                <p>Email: {line_edit_data[1]}</p>
                <p>Phone Number: {line_edit_data[2]}</p>
                <p>Day of Event Phone: {line_edit_data[3]}</p>
                <p>Full Contact Address: {line_edit_data[4]}</p>
                <p>Name of Event: {line_edit_data[5]}</p>
                <p>Event Location: {line_edit_data[6]}</p>
                <p>Date of Event: {line_edit_data[7]}</p>
                <p>Start & End Time: {line_edit_data[8]}</p>

                <h2>Order Details</h2>
                <ul>
        """
        for row in range(table_widget.rowCount()):
            item_name = table_widget.item(row, 0).text() if table_widget.item(row, 0) else ''
            quantity = table_widget.item(row, 1).text() if table_widget.item(row, 1) else ''
            price = table_widget.item(row, 2).text() if table_widget.item(row, 2) else ''
            html_template += f"<li>{item_name} - Quantity: {quantity} - Price: {price}</li>"
        
        html_template += """
                </ul>
                <h2>Signature</h2>
                <p>Customer Signature:</p>
                <div class="signature-area"></div>
            </div>
        </body>
        </html>
        """
        return html_template


    def format_agreement_text(self, line_edit_data, table_data):
        """
        Formats the data into a string that will be written to the file
        """
        agreement_text = "Rental Agreement\n\n"
        agreement_text += "Details:\n"
        for data in line_edit_data:
            agreement_text += data + "\n"

        agreement_text += "\nRental Items:\n"
        for row in table_data:
            agreement_text += ", ".join(row) + "\n"

        return agreement_text

    def get_database_connection(self):
        """
        Database connection with hardcoded database path
        (Replace "path_to_your_database.db" with full/relative db path)
        """
        from database.connection import create_connection
        return create_connection("path_to_your_database.db")



    ''' 
    TODO: Additions to make:
    --mileage: api calls to google maps 
    --time for mileage: worker cost, mpg of truck
    --allow users to add items into the database and change inventory
    --update excel sheet
    --view rental agreement preview in app
    --splash page to see week at a glance
    '''