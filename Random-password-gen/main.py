import sys, random, string
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QMessageBox

# from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi


class PasswdGenApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("PasswordGen.ui", self)
        self.setWindowTitle("Random Password Generator")
        self.Handel_Buttons()

        # Required Variables
        # self.typing_started = False
        # self.start_time = None

        # Initial Setup
        self.password_field.setReadOnly(True)
        self.password_field.setText("")
        self.copy_success_label.setText("")

    def Handel_Buttons(self):
        self.password_length_slider.valueChanged.connect(self.update_slider_label)
        self.generate_button.clicked.connect(self.generate_password)
        self.copy_button.clicked.connect(self.copy_password)

    # ````````````````````````````````````````
    # ---------------------
    def update_slider_label(self, value):
        self.slider_label.setText(f"Password Length: {value}")

    # ---------------------
    def generate_password(self):
        password_length = self.password_length_slider.value()
        include_numbers = self.include_numbers_checkbox.isChecked()
        include_special_chars = self.include_specialChars_checkbox.isChecked()

        characters = string.ascii_letters
        if include_numbers:
            characters += string.digits
        if include_special_chars:
            characters += string.punctuation

        if not characters:
            QMessageBox.warning(self, "Warning", "Please select at least one option.")
            return

        password = "".join(random.choice(characters) for _ in range(password_length))
        self.password_field.setText(password)
        self.copy_success_label.setText("")

    # ---------------------
    def copy_password(self):
        password = self.password_field.toPlainText()
        if password:
            clipboard = QApplication.clipboard()
            clipboard.setText(password)
            self.copy_success_label.setText("Password copied to clipboard")
        else:
            self.copy_success_label.setText("No password to copy")

    # ````````````````````````````````````````

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = PasswdGenApp() 
    main_window.show()
    sys.exit(app.exec_())
