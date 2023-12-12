#driver program 
import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow  # Make sure to import correctly based on your project structure

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
