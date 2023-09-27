import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi


class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("Calculator.ui", self)
        self.setWindowTitle("Basic Calculator")
        self.Handel_Buttons()

    def Handel_Buttons(self):
        # Operation Btns
        self.ac_btn.clicked.connect(lambda: self.press_it("AC"))
        self.del_btn.clicked.connect(self.delete_last)
        self.result_btn.clicked.connect(self.calculate)

        # Operator Btns
        self.modulud_btn.clicked.connect(lambda: self.op_pressed("%"))
        self.divide_btn.clicked.connect(lambda: self.op_pressed("/"))
        self.multiply_btn.clicked.connect(lambda: self.op_pressed("*"))
        self.add_btn.clicked.connect(lambda: self.op_pressed("+"))
        self.substract_btn.clicked.connect(lambda: self.op_pressed("-"))

        # Operand Btns
        self.dot_btn.clicked.connect(self.dot_pressed)
        self.num0_btn.clicked.connect(lambda: self.press_it("0"))
        self.num1_btn.clicked.connect(lambda: self.press_it("1"))
        self.num2_btn.clicked.connect(lambda: self.press_it("2"))
        self.num3_btn.clicked.connect(lambda: self.press_it("3"))
        self.num4_btn.clicked.connect(lambda: self.press_it("4"))
        self.num5_btn.clicked.connect(lambda: self.press_it("5"))
        self.num6_btn.clicked.connect(lambda: self.press_it("6"))
        self.num7_btn.clicked.connect(lambda: self.press_it("7"))
        self.num8_btn.clicked.connect(lambda: self.press_it("8"))
        self.num9_btn.clicked.connect(lambda: self.press_it("9"))

    # ````````````````````````````````````````
    # ---------------------
    def calculate(self):
        displayedContent = self.display_box.text()
        last_char = displayedContent[-1]
        if last_char in ["%", "/", "*", "+", "-"] or last_char == ".":
            displayedContent = displayedContent[:-1]
        try:
            result = str(eval(displayedContent))
            self.display_box.setText(result)
        except:
            self.display_box.setText("Error Encountered")

    # ---------------------
    def delete_last(self):
        displayedContent = self.display_box.text()
        displayedContent = displayedContent[:-1]
        self.display_box.setText(displayedContent)

    # ---------------------
    def dot_pressed(self):
        displayedContent = self.display_box.text()
        current_part = displayedContent.split()[-1]
        operator_signs = ["+", "-", "*", "/"]
        operator_exist = any(
            operator in displayedContent for operator in operator_signs
        )
        if operator_exist:
            last_operator_index = max(
                displayedContent.rfind(op) for op in operator_signs
            )
            if "." in current_part and current_part.rfind(".") > last_operator_index:
                return
        if "." not in current_part or operator_exist:
            self.display_box.setText(f"{displayedContent}.")

    # ---------------------
    def op_pressed(self, operator):
        displayedContent = self.display_box.text()
        last_char = displayedContent[-1]

        if last_char in ["%", "/", "*", "+", "-"] or last_char == ".":
            displayedContent = displayedContent[:-1]

        displayedContent += operator
        self.display_box.setText(displayedContent)

    # ---------------------
    def press_it(self, pressed):
        if pressed == "AC":
            self.display_box.setText("0")
        else:
            if self.display_box.text() == "0":
                self.display_box.setText("")
            self.display_box.setText(f"{self.display_box.text()}{pressed}")

    # ````````````````````````````````````````


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CalculatorApp()
    main_window.show()
    sys.exit(app.exec_())
