from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QListWidget, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QFontDatabase
from PyQt5 import QtGui 
from PyQt5.QtCore import Qt

from .fancyWindow import CustomTitleBar  # Importing CustomTitleBar


from .add_event_dialog import AddEventDialog
from business_logic import package_definitions
from database.operations import create_booking, get_available_quantity
from scripts import view_db
import os

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
        self.selected_item_name = None  # Initialize selected_item_name
        self.saved_items = None

        self.init_ui()
        #self.currently_selected_item = None  # Attribute to store the selected item


    def init_ui(self):
        self.apply_stylesheet() 
        self.label.setPixmap(QtGui.QPixmap("C:/InventoryManager/RentalInventoryManager/gui/qt images/lujoLogo.png"))
# C:\InventoryManager\RentalInventoryManager\gui
        # database connection
        self.conn = self.get_database_connection()

        # lists of packages with items and their quantities
        # order: armless, ottoman, squares, corners
        self.v2_99 = [(29591065, 2), (12775351, 2), (55453976, 2), (25942155, 1)]
        self.v2_100 = [(29591065, 4), (12775351, 4), (55453976, 4), (25942155, 2)]
        self.v2_101 = [(29591065, 8), (12775351, 8), (55453976, 8), (25942155, 4)]

        # Connect the calendar widgets to update methods
        self.fromDateCalendar.selectionChanged.connect(self.update_from_date_time)
        self.toDateCalendar.selectionChanged.connect(self.update_to_date_time)

        # Assuming the object names are fromDateCalendar, toDateCalendar, and viewAvailabilityButton
        # Connect the View Availability button
        self.viewAvailabilityButton.clicked.connect(self.on_view_availability)

        # Initialize attributes for the selected dates
        self.from_date = None
        self.to_date = None

        self.populate_list_widget()

        # Connect the itemClicked signal of each QListWidget in the tabs
        self.v2ListWidget.itemClicked.connect(self.on_item_selected)
        self.legacyListWidget.itemClicked.connect(self.on_item_selected)
        self.ultraListWidget.itemClicked.connect(self.on_item_selected)
        # Repeat for other QListWidgets in other tabs

        # Connect the Add button
        self.addPushButton.clicked.connect(self.on_add_item_clicked)

        # Connect the Remove Button
        self.removePushButton.clicked.connect(self.on_remove_item_clicked)

        # Connect the Done button 
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
            font-size: 10pt;
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
            font-size: 10pt; /* Adjust the font size as needed */
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

    def update_from_date_time(self):
        selected_date = self.fromDateCalendar.selectedDate()
        self.fromDateTimeEdit.setDateTime(selected_date.startOfDay())
    def update_to_date_time(self):
        selected_date = self.toDateCalendar.selectedDate()
        self.toDateTimeEdit.setDateTime(selected_date.startOfDay())

    def on_view_availability(self):
        # Get the selected dates from the calendar widgets
        self.from_date = self.fromDateCalendar.selectedDate()
        self.to_date = self.toDateCalendar.selectedDate()

        # Check if both dates are selected
        if self.from_date and self.to_date:
            # Switch to the second page of the QStackedWidget
            # Assuming your QStackedWidget's name is mainStackedWidget
            self.stackedWidget.setCurrentIndex(1)
        else:
            # Handle the case where one or both dates are not selected
            print("Please select both 'from' and 'to' dates.")

    def populate_list_widget(self):
        # Assuming your QListWidget's name is furnitureListWidget
        for item_name in self.fetch_v2():
            item = QListWidgetItem(item_name)
            self.v2ListWidget.addItem(item)

        for item_name in self.fetch_legacy():
            item = QListWidgetItem(item_name) 
            self.legacyListWidget.addItem(item)
        # Connect item click signal
        self.v2ListWidget.itemClicked.connect(self.on_item_clicked)
        self.legacyListWidget.itemClicked.connect(self.on_item_clicked)

    def fetch_v2(self):
        # Fetch furniture items from your database or data source
        return ["Package: V2 Lounge 98", "Package: V2 Lounge 99", "Package: V2 Lounge 100", "Package: V2 Lounge 101", "V2 Armless Chair", "V2 Corner Chair", "V2 Ottoman", "V2 Square"]  # item headers
    def fetch_legacy(self):
        return ["Package: Legacy Lounge 98", "Package: Legacy Lounge 99","Package: Legacy Lounge 100","Package: Legacy Lounge 101", 
                "Legacy Armless Chair", "Legacy Corner Chair", "Legacy Ottoman", "Legacy Square",
                "Legacy Big Ottoman", "Legacy Backed Ottoman", "Legacy Rectangle"]
    

    def on_item_clicked(self, item):
        print("Clicked item:", item.text())
        self.currently_selected_item = item

    def on_item_selected(self):

        # Get the selected item from the active QListWidget
        current_list_widget = self.get_active_list_widget()
        selected_item = current_list_widget.currentItem()
        if selected_item:
            self.selected_item_name = selected_item.text()
        else:
            self.selected_item_name = None

        ''' check if it's a package or an individual item '''
        if(self.selected_item_name[0] == 'P'):
            max_quantity = self.unpack_and_get_max_quantity(self.selected_item_name)
        else:
            max_quantity = get_available_quantity(self.conn,
                                                  self.get_item_id(self.selected_item_name), 
                                                   self.from_date.toString("yyyy-MM-dd"), 
                                                   self.to_date.toString("yyyy-MM-dd"))
        self.spinBox.setMaximum(max_quantity)
        
    def unpack_and_get_max_quantity(self, item_name):
        ''' 
        Check amount of pkgs you can make 
        handle item_and_inStock here [8,8,8,4] for example
        '''
        match item_name:
            case "Package: V2 Lounge 99":
                item_and_inStock = self.loop_and_unpack(self.v2_99)
                item_list = item_and_inStock[0] # [#,#,#,#]
                weakLink = item_list[0] // self.v2_99[0][1] # starter
                print("item_list: ", item_list, "  weaklink: ", weakLink, " v2_99[3][1]", self.v2_99[3][1])
                for i, item_amount in enumerate(item_list):
                    # this gets the amount for the package and divides whats available
                    quantity = item_amount // self.v2_99[i][1]
                    if(weakLink >= quantity):
                        weakLink = quantity
                    # weak link should equal the max amount of pkgs u can make out of whats available

            case "Package: V2 Lounge 100":
                item_and_inStock = self.loop_and_unpack(self.v2_100)
                item_list = item_and_inStock[0] # [#,#,#,#]
                weakLink = item_list[0] // self.v2_100[0][1] # starter
                for i, item_amount in enumerate(item_list):
                    # this gets the amount for the package and divides whats available
                    quantity = item_amount // self.v2_100[i][1]
                    if(weakLink >= quantity):
                        weakLink = quantity
                    # weak link should equal the max amount of pkgs u can make out of whats available


            case "Package: V2 Lounge 101":
                item_and_inStock = self.loop_and_unpack(self.v2_101)
                item_list = item_and_inStock[0] # item_list will be in form: [#,#,#,#]
                weakLink = item_list[0] // self.v2_101[0][1] # starter: first item of list is [0] // armless
                for i, item_amount in enumerate(item_list):
                    # this gets the amount for the package and divides whats available
                    quantity = item_amount // self.v2_101[i][1]
                    if(weakLink >= quantity):
                        weakLink = quantity
                    # weak link should equal the max amount of pkgs u can make out of whats available
        ''' If you cant make a full package, return 0 as the max quantity'''
        if(item_and_inStock[1] == False):
            return 0 
        else:
            return weakLink
        
        
    def loop_and_unpack(self, pkg):
        quantities = []
        enough = True
        for item in pkg:
            quantity = get_available_quantity(self.conn, item[0], 
                                            self.from_date.toString("yyyy-MM-dd"),
                                            self.to_date.toString("yyyy-MM-dd"))
            if quantity is None or quantity < item[1]:
                print(f"not enough of item_id: {item[0]}")
                enough = False
                # Consider breaking out of the loop if one item is not enough
            else:
                quantities.append(quantity)  # Use append instead of extend
        return (quantities, enough)


    '''def get_selected_items(self):
        # Logic to get the selected item's identifier from the list widget
        pass

    def get_selected_dates(self):
        # Logic to get the selected 'from' and 'to' dates from the calendar
        # Tuple?
        return (self.from_date, self.to_date)
  '''
    
    def on_add_item_clicked(self):
        # Check if an item has been selected
        if self.selected_item_name is not None:
            quantity = self.spinBox.value()
            item_with_quantity = f"{self.selected_item_name} - Quantity: {quantity}"

            # Add the selected item's text to the secondListWidget
            self.currentlySelectedListWidget.addItem(item_with_quantity)

            # Optionally, clear the currently selected item
            self.selected_item_name = None
        else:
            print("No item selected")  # Or show a message to the user

    def on_remove_item_clicked(self):
        # Check if an item is selected
        if self.selected_item_name:
            # Find the row of the selected item
            row = self.currentlySelectedListWidget.row(self.selected_item_name)
            # Remove the item from the list
            self.currentlySelectedListWidget.takeItem(row)
        else:
            print("No item selected to remove")  # Or show a message to the user


    def get_active_list_widget(self):
        # Assuming you have a QTabWidget named tabWidget
        current_tab_index = self.tabWidget.currentIndex()
        # Return the QListWidget corresponding to the current tab
        if current_tab_index == 0:
            return self.v2ListWidget
        elif current_tab_index == 1:
            return self.legacyListWidget
        elif current_tab_index == 2:
            return self.ultraListWidget
        # Add more conditions for other tabs
        # ...
        else:
            return None

    def on_done_clicked(self):
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
        # Gather item IDs from the second list
        # items to book list will look like: [("10125473", 4), ("V299", 1)] <- list of tuples
        # Call database function to create booking
        self.create_booking(items_to_process)
        self.stackedWidget.setCurrentIndex(2)  # Assuming page 3 is at index 2
        self.populate_summary_table()

        
    def parse_item_and_quantity(self, item_text):
        # Example item_text: "ItemName - Quantity: 4"
        name_part, quantity_part = item_text.split(" - Quantity: ")
        quantity = int(quantity_part)
        return name_part, quantity

    def get_item_id(self, item_name):
        # Implement logic to retrieve item ID based on item name
        match item_name: # TODO: id for LED: 56556348
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
        #conn = self.get_database_connection()
        # Implement or call a function to handle booking logic
        from_date_string = self.from_date.toString("yyyy-MM-dd")
        to_date_string = self.to_date.toString("yyyy-MM-dd")
        print(from_date_string, to_date_string)
        create_booking(self.conn, items_to_book, from_date_string, to_date_string)

    def populate_summary_table(self):
        # Clear the table before adding new items
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Item", "Quantity", "Price"])

        for item_text in self.saved_items:
            row_count = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_count)

            item_name, item_quantity = self.parse_item_and_quantity(item_text)
            # Assume an arbitrary price, modify this part as per your actual pricing logic
            price = self.calculate_price(item_name, item_quantity)

            # Create QTableWidgetItem for each piece of data
            item_widget = QTableWidgetItem(item_name)
            quantity_widget = QTableWidgetItem(str(item_quantity))
            price_widget = QTableWidgetItem(f"${price:.2f}")

            # Add items to the table
            self.tableWidget.setItem(row_count, 0, item_widget)
            self.tableWidget.setItem(row_count, 1, quantity_widget)
            self.tableWidget.setItem(row_count, 2, price_widget)
        # Adjust the heights of rows to fit the content
        self.adjust_table_row_heights()

    def adjust_table_row_heights(self):
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.resizeRowToContents(row)

    def calculate_price(self, item_name, quantity):
        # Placeholder function to calculate price, modify as needed
        # Example: return a fixed price per item
        return 10 * quantity  # Example: $10 per item

    def on_confirm_button_clicked(self):
        # Collect data from LineEdits
        line_edit_data = [
            self.lineEdit_1.text(), 
            self.lineEdit_2.text(), 
            self.lineEdit_3.text(),
            self.lineEdit_4.text(),
            self.lineEdit_5.text(),
            self.lineEdit_6.text(),
            self.lineEdit_7.text(),
            self.lineEdit_8.text(),
            self.lineEdit_9.text()]

        # Collect data from QTableWidget
        table_data = []
        for row in range(self.tableWidget.rowCount()):
            row_data = []
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                row_data.append(item.text() if item else "")
            table_data.append(row_data)

        # Format the data into a string
        agreement_text = self.format_agreement_text(line_edit_data, table_data)

        # Save the file
        self.save_agreement_to_file(agreement_text)

    def format_agreement_text(self, line_edit_data, table_data):
        # Format the data into a string that will be written to the file
        # Customize this according to your needs
        agreement_text = "Rental Agreement\n\n"
        agreement_text += "Details:\n"
        for data in line_edit_data:
            agreement_text += data + "\n"

        agreement_text += "\nRental Items:\n"
        for row in table_data:
            agreement_text += ", ".join(row) + "\n"

        return agreement_text

    def save_agreement_to_file(self, agreement_text):
        # Open a file dialog for the user to choose where to save the file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Agreement", "", "Text Files (*.txt)", options=options)
        
        if file_name:
            with open(file_name, 'w') as file:
                file.write(agreement_text)


    def get_database_connection(self):
        # Implement the logic to create and return a database connection
        from database.connection import create_connection
        return create_connection("path_to_your_database.db")


# The rest of your class remains unchanged
# DELIVERY FEES <- edit, add additional fees for: mileage, big orders
    ''' additions to make:
    --mileage: api calls to google maps 
    --time for mileage: worker cost, mpg of truck
    '''