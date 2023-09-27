import sys
import random
import string
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSlider,
    QCheckBox,
    QPushButton,
    QLabel,
    QLineEdit,
    QMessageBox,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QClipboard


class PasswordGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Random Password Generator")
        self.setGeometry(100, 100, 400, 250)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Password Length Slider
        self.slider_label = QLabel("Password Length: 0")
        layout.addWidget(self.slider_label)

        self.password_length_slider = QSlider(Qt.Horizontal)
        self.password_length_slider.setMinimum(0)
        self.password_length_slider.setMaximum(100)
        layout.addWidget(self.password_length_slider)

        # Checkboxes
        self.include_numbers_checkbox = QCheckBox("Include Numbers")
        self.include_special_chars_checkbox = QCheckBox("Include Special Characters")
        layout.addWidget(self.include_numbers_checkbox)
        layout.addWidget(self.include_special_chars_checkbox)

        # Generate Password Button
        self.generate_button = QPushButton("Generate Password")
        layout.addWidget(self.generate_button)

        # Password Display Label
        self.password_label = QLabel("Generated Password will appear here")
        layout.addWidget(self.password_label)

        # Copy Button
        self.copy_button = QPushButton("Copy")
        layout.addWidget(self.copy_button)

        # Copy Success Label
        self.copy_success_label = QLabel("")
        layout.addWidget(self.copy_success_label)

        # Signals and Slots
        self.password_length_slider.valueChanged.connect(self.update_slider_label)
        self.generate_button.clicked.connect(self.generate_password)
        self.copy_button.clicked.connect(self.copy_password)

    def update_slider_label(self, value):
        self.slider_label.setText(f"Password Length: {value}")

    def generate_password(self):
        password_length = self.password_length_slider.value()
        include_numbers = self.include_numbers_checkbox.isChecked()
        include_special_chars = self.include_special_chars_checkbox.isChecked()

        characters = string.ascii_letters
        if include_numbers:
            characters += string.digits
        if include_special_chars:
            characters += string.punctuation

        if not characters:
            QMessageBox.warning(self, "Warning", "Please select at least one option.")
            return

        password = "".join(random.choice(characters) for _ in range(password_length))
        self.password_label.setText(password)
        self.copy_success_label.setText("")

    def copy_password(self):
        password = self.password_label.text()
        if password:
            clipboard = QApplication.clipboard()
            clipboard.setText(password)
            self.copy_success_label.setText("Password copied to clipboard")
        else:
            self.copy_success_label.setText("No password to copy")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())
