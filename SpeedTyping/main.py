import sys, time, random
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.uic import loadUi


class SpeedTypeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("speedTyping.ui", self)
        self.setWindowTitle("Speed Typing Test")
        self.Handel_Buttons()

        # Given Paragraphs
        self.paragraphs = [
            "The quick brown fox jumps over the lazy dog.",
            "Programming is a Skill that can be developed by dedication.",
            "Clean code always looks like it was written by someone who cares.",
            "I am grateful to the Universe",
            "The hard days are what make you stronger.Keep your eyes on the stars, and your feet on the ground.",
            "Trust yourself that you can do it and get it.",
        ]

        # Required Variables
        self.typing_started = False
        self.start_time = None

        # Initial Setup
        self.text_field.setPlaceholderText(
            ("\tInstructions : \n")
            + ("\tClick 'Start Test' & start typing\n")
            + ("\taccording to given Paragraph.\n")
            + ("\tAfter completion click 'Stop' button\n")
            + ("\tor Press 'CTRL + ENTER' to get result.")
        )
        self.text_field.setReadOnly(True)
        self.wpm_lbl.setText("")
        self.accuracy_lbl.setText("")
        self.given_paragraph.setText("^ - ^")

    def Handel_Buttons(self):
        self.startTest_btn.clicked.connect(self.Handle_Test)

    # ````````````````````````````````````````
    # ---------------------
    def get_random_paragraph(self):
        return random.choice(self.paragraphs)

    # ---------------------
    def Handle_Test(self):
        if not self.typing_started:
            self.typing_started = True
            self.start_time = time.time()
            self.startTest_btn.setText("Stop")
            self.text_field.setReadOnly(False)
            self.text_field.clear()
            self.given_paragraph.setText(self.get_random_paragraph())
            self.text_field.setFocus()
            self.wpm_lbl.setText("")
            self.accuracy_lbl.setText("")
        else:
            self.typing_started = False
            self.startTest_btn.setText("Start Again")
            self.text_field.setReadOnly(True)
            self.calculate_results()
        self.text_field.setPlaceholderText("")

    # ---------------------
    def calculate_results(self):
        typed_text = self.text_field.toPlainText()
        reference_text = self.given_paragraph.text()
        reference_words = reference_text.split()
        typed_words = typed_text.split()

        elapsed_time = time.time() - self.start_time
        words_per_minute = int(len(typed_words) / (elapsed_time / 60))

        correct_words = sum(
            1 for tw, rw in zip(typed_words, reference_words) if tw == rw
        )
        accuracy = (
            (correct_words / len(reference_words)) * 100 if reference_words else 0
        )

        result_wpm = f"WPM : {words_per_minute}"
        result_accuracy = f"Accuracy : {accuracy:.2f}%"

        self.wpm_lbl.setText(result_wpm)
        self.accuracy_lbl.setText(result_accuracy)

    # ---------------------
    def keyPressEvent(self, event):
        if (
            self.typing_started
            and event.key() == Qt.Key_Return
            and event.modifiers() == Qt.ControlModifier
        ):
            self.Handle_Test()

    # ````````````````````````````````````````


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = SpeedTypeApp()
    main_window.show()
    sys.exit(app.exec_())
