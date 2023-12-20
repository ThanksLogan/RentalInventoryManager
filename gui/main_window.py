from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem
from .add_event_dialog import AddEventDialog
from business_logic import package_definitions
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(__file__), 'LujoIMS_UI_v1.1.ui')
        uic.loadUi(ui_path, self)

        self.init_ui()

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

    def on_item_selected(self):
        selected_item = self.get_selected_item()  # Implement this method
        selected_dates = self.get_selected_dates()  # Implement this method
        availability = self.check_availability(selected_item, selected_dates)
        self.display_availability(availability)

    def get_selected_item(self):
        # Logic to get the selected item's identifier from the list widget
        pass

    def get_selected_dates(self):
        # Logic to get the selected 'from' and 'to' dates from the calendar
        pass

    def check_availability(self, item, dates):
        # Logic to check the database for the item's availability
        # This involves querying the bookings table
        pass

    def display_availability(self, availability):
        # Logic to display the availability status to the user
        pass
    


# The rest of your class remains unchanged
