import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QCalendarWidget

class CalendarApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the calendar widget
        self.calendar = QCalendarWidget(self)

        # Set the size and position of the calendar
        self.calendar.setGeometry(50, 50, 400, 300)

        # Set the window title
        self.setWindowTitle("Calendar Example")

        # Set the size of the main window
        self.setGeometry(100, 100, 500, 400)

        # Show the main window
        self.show()

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = CalendarApp()
    sys.exit(app.exec_())
