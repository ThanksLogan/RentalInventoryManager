from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
from PyQt5.QtWidgets import QListWidget

from .add_event_dialog import AddEventDialog
from business_logic import package_definitions
from database.operations import create_booking
from scripts import view_db
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'LujoIMS_UI_v1.1.ui')
        uic.loadUi(ui_path, self)

        '''Initializations'''
        self.selected_item_name = None  # Initialize selected_item_name

        self.init_ui()
        #self.currently_selected_item = None  # Attribute to store the selected item


    def init_ui(self):
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
        # Connect the Done button 
        self.doneButton.clicked.connect(self.on_done_clicked)

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
        return ["V2 Lounge 98", "V2 Lounge 99", "V2 Lounge 100", "V2 Lounge 101", "V2 Armless Chair", "V2 Corner Chair", "V2 Ottoman", "V2 Square"]  # item headers
    def fetch_legacy(self):
        return ["Legacy Lounge 98", "Legacy Lounge 99","Legacy Lounge 100","Legacy Lounge 101", 
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
        
    def parse_item_and_quantity(self, item_text):
        # Example item_text: "ItemName - Quantity: 4"
        name_part, quantity_part = item_text.split(" - Quantity: ")
        quantity = int(quantity_part)
        return name_part, quantity

    def get_item_id(self, item_name):
        # Implement logic to retrieve item ID based on item name
        match item_name: # TODO: id for LED: 56556348
            case "V2 Lounge 99":
                return "V2_99"
            case "V2 Lounge 100":
                return "V2_100"
            case "V2 Lounge 101":
                return "V2_101"
            case "V2 Lounge 98":
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
        conn = self.get_database_connection()
        # Implement or call a function to handle booking logic
        from_date_string = self.from_date.toString("yyyy-MM-dd")
        to_date_string = self.to_date.toString("yyyy-MM-dd")
        print(from_date_string, to_date_string)
        create_booking(conn, items_to_book, from_date_string, to_date_string)


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