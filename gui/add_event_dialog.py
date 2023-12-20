from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout, QTimeEdit
from PyQt5.QtCore import Qt

class AddEventDialog(QDialog):
    def __init__(self, packages, parent=None):
        super().__init__(parent)

        self.packages = packages
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title
        self.title_edit = QLineEdit(self)
        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_edit)

        # Time
        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm")
        layout.addWidget(QLabel("Time:"))
        layout.addWidget(self.time_edit)

        # Contact Name
        self.contact_edit = QLineEdit(self)
        layout.addWidget(QLabel("Contact Name:"))
        layout.addWidget(self.contact_edit)

        # Package Choice
        self.package_combo = QComboBox(self)
        self.package_combo.addItems(self.packages)
        layout.addWidget(QLabel("Package:"))
        layout.addWidget(self.package_combo)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK", self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(self.ok_button)
        buttons_layout.addWidget(self.cancel_button)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)
