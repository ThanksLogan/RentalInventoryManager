from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QCalendarWidget, QLabel
from .calendar_view import CalendarView
from .inventory_view import InventoryView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the title and size of the main window
        self.setWindowTitle('Furniture Rental Inventory Manager')
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height

        # Create a central widget and set a layout for it
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create and add a calendar widget
        self.calendar = CalendarView(self)
        layout.addWidget(self.calendar)

        # Inside the MainWindow class
        self.inventory_view = InventoryView(self)
        layout.addWidget(self.inventory_view)

        # Create and add a label to display information
        self.info_label = QLabel('Select a date to view inventory', self)
        layout.addWidget(self.info_label)

        # Additional setup (e.g., connecting signals to slots) can go here

    # Method to update info label, can be connected to calendar signals
    def update_info_label(self, date):
        # Placeholder for logic to update the info label based on the selected date
        self.info_label.setText(f"Selected Date: {date.toString()}")
