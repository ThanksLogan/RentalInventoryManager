from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QPoint

class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Spacer to push buttons to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(spacer)

        # Stylish buttons
        self.minimize_button = QPushButton("−")
        #self.maximize_button = QPushButton("□")
        self.close_button = QPushButton("×")

        # Button Styling
        button_style = "QPushButton { background-color: #444; border: none; } QPushButton:hover { background-color: #666; }"
        self.minimize_button.setStyleSheet(button_style)
        #self.maximize_button.setStyleSheet(button_style)
        self.close_button.setStyleSheet("QPushButton { background-color: #d00; border: none; } QPushButton:hover { background-color: #e00; }")

        # Button Size
        button_size = 30
        self.minimize_button.setFixedSize(button_size, button_size)
        #self.maximize_button.setFixedSize(button_size, button_size)
        self.close_button.setFixedSize(button_size, button_size)

        # Connect the buttons to their functions
        self.minimize_button.clicked.connect(self.minimize)
        #self.maximize_button.clicked.connect(self.toggle_maximize)
        self.close_button.clicked.connect(self.close)

        # Adding widgets to the layout
        #self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.minimize_button)
        #self.layout.addWidget(self.maximize_button)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

        self._is_maximized = False
        self._mouse_pressed = False

    def minimize(self):
        self.parent().showMinimized()

    """def toggle_maximize(self):
        if self._is_maximized:
            self.parent().showNormal()
        else:
            self.parent().showMaximized()
        self._is_maximized = not self._is_maximized"""

    def close(self):
        self.parent().close()

    def mousePressEvent(self, event):
        self._mouse_pressed = True
        self._mouse_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self._mouse_pressed = False

    def mouseMoveEvent(self, event):
        if self._mouse_pressed:
            delta = QPoint(event.globalPos() - self._mouse_pos)
            self.parent().move(self.parent().pos() + delta)
            self._mouse_pos = event.globalPos()
