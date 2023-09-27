import sys, datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
import mysql.connector


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Login.ui", self)
        self.setWindowTitle("Login")

        self.login_button.clicked.connect(self.check_login)

        # Initialize a database connection
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )

    def check_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Replace with your actual table name and column names
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM login_admin WHERE username = %s AND password = %s",
            (username, password),
        )
        result = cursor.fetchone()

        if result:
            self.accept()  # Close the login window if login is successful
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")


# ``````````````````````````````````````
# ``````````````````````````````````````


class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("LMS1.ui", self)
        self.setWindowTitle("Library Management System")
        self.Handel_Buttons()

    def Handel_Buttons(self):
        self.pushButton_5.clicked.connect(self.open_Status_Tab)
        self.pushButton_8.clicked.connect(self.open_Books_Tab)
        self.pushButton_7.clicked.connect(self.open_Student_Tab)
        self.pushButton_6.clicked.connect(self.open_Admin_Tab)

        self.pushButton.clicked.connect(self.Add_Status)
        self.pushButton_14.clicked.connect(self.Show_All_Status)
        self.pushButton_13.clicked.connect(self.Show_All_Students)

        self.pushButton_2.clicked.connect(self.Add_New_Books)
        self.pushButton_4.clicked.connect(self.Search_Books)
        self.pushButton_3.clicked.connect(self.Delete_Books)
        self.pushButton_9.clicked.connect(self.Show_All_Books)

        self.pushButton_12.clicked.connect(self.Add_New_User)
        self.pushButton_11.clicked.connect(self.Search_User)
        self.pushButton_10.clicked.connect(self.Delete_User)

    # Tab Opening Btns -------------------------------------
    def open_Status_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_Student_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_Admin_Tab(self):
        self.tabWidget.setCurrentIndex(3)

    # Books Tab Functions ----------------------------------
    # ---------------------
    def Add_New_Books(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        book_code = self.lineEdit_5.text()
        book_title = self.lineEdit_2.text()
        book_author = self.lineEdit_4.text()
        book_price = self.lineEdit_7.text()
        cursor = self.db.cursor()
        cursor.execute(
            """
            INSERT INTO books (book_code,book_title,book_author,book_price)
            VALUES (%s , %s , %s , %s)
        """,
            (
                book_code,
                book_title,
                book_author,
                book_price,
            ),
        )
        self.db.commit()
        self.plainTextEdit.setPlainText(
            f"""
            Added Book : {book_title}\n
            Added Book Code : {book_code}\n
            Added Book Author : {book_author}\n
            Added Book price : {book_price}\n
        """
        )
        self.statusBar().showMessage("New Book Added")

        self.db.close()

    # ---------------------
    def Search_Books(self):
        book_title_inpt = self.book_title_srch.text()
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM books WHERE book_title = %s", [(book_title_inpt)])
        data = cursor.fetchone()

        if data:
            self.lineEdit_8.setText(data[2])
            self.lineEdit_6.setText(data[1])
            self.lineEdit_9.setText(data[3])
            self.plainTextEdit_2.setPlainText(
                f"""
            Book Found\n
            Book Code : {data[1]}\n
            Book Author : {data[2]}\n
            Book price : {data[3]}\n
            """
            )
        else:
            self.plainTextEdit_2.setPlainText("No Book Found")

        self.db.close()

    # ---------------------
    def Delete_Books(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cursor = self.db.cursor()

        book_title_inpt = self.book_title_srch.text()

        warning = QMessageBox.warning(
            self, "Delete Book", "Are you sure", QMessageBox.Yes | QMessageBox.No
        )
        if warning == QMessageBox.Yes:
            cursor.execute(
                "DELETE FROM books WHERE book_title = %s", [(book_title_inpt)]
            )
            self.db.commit()
            self.statusBar().showMessage("Book Deleted")

        self.db.close()

    # ---------------------
    def Show_All_Books(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cursor = self.db.cursor()

        cursor.execute("SELECT * FROM books")
        data = cursor.fetchall()
        # print(data)

        self.tableWidget_3.setRowCount(0)
        self.tableWidget_3.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_3.rowCount()
            self.tableWidget_3.insertRow(row_position)

        self.db.close()

    # Admins Tab Functions ----------------------------------
    # ---------------------
    def Add_New_User(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cursor = self.db.cursor()

        username = self.lineEdit_10.text()
        email = self.lineEdit_11.text()
        password = self.lineEdit_13.text()
        cpassword = self.lineEdit_12.text()

        if password == cpassword:
            cursor.execute(
                """
                INSERT INTO login_admin (username , email , password)
                VALUES (%s , %s , %s)
            """,
                (username, email, password),
            )
            self.db.commit()
            self.label_22.setText("New Admin Added")
            # self.statusBar().showMessage("New Admin Added")
            self.lineEdit_10.setText("")
            self.lineEdit_11.setText("")
            self.lineEdit_12.setText("")
            self.lineEdit_13.setText("")
        else:
            self.label_22.setText("please add a valid password twice")

        self.db.close()

    # ---------------------
    def Search_User(self):
        username_inpt = self.lineEdit_17.text()
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cursor = self.db.cursor()
        cursor.execute(
            "SELECT * FROM login_admin WHERE username = %s", [(username_inpt)]
        )
        data = cursor.fetchone()
        if data:
            self.lineEdit_19.setText(data[1])
            self.lineEdit_16.setText(data[2])
        else:
            self.statusBar().showMessage("No Admin Found")
            self.lineEdit_19.setText("")
            self.lineEdit_16.setText("")

        self.db.close()

    # ---------------------
    def Delete_User(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cursor = self.db.cursor()

        username_inpt = self.lineEdit_17.text()

        warning = QMessageBox.warning(
            self, "Delete User", "Are you sure", QMessageBox.Yes | QMessageBox.No
        )
        if warning == QMessageBox.Yes:
            cursor.execute(
                "DELETE FROM login_admin WHERE username = %s", [(username_inpt)]
            )
            self.db.commit()
            self.statusBar().showMessage("User Deleted")
            self.lineEdit_19.setText("")
            self.lineEdit_17.setText("")
            self.lineEdit_16.setText("")

        self.db.close()

    # ---------------------
    def Add_Status(self):
        book_title_inpt = self.lineEdit.text()
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM books WHERE book_title = %s", [(book_title_inpt)])
        data = cursor.fetchone()

        if not data:
            warning = QMessageBox.warning(
                self, "Sorry", "This book is not Available", QMessageBox.Ok
            )
            return

        student_Name = self.lineEdit_3.text()
        student_Email = self.lineEdit_14.text()
        duration_days = self.comboBox_2.currentIndex() + 1
        from_date = datetime.date.today()
        to_date = from_date + datetime.timedelta(days=duration_days)

        cursor.execute(
            """
            INSERT INTO lib_status 
            (student_name,student_email,rent_book,rent_duration_days,from_day,to_day)
            VALUES (%s , %s , %s , %s, %s , %s)
        """,
            (
                student_Name,
                student_Email,
                book_title_inpt,
                duration_days,
                from_date,
                to_date,
            ),
        )
        self.db.commit()
        self.statusBar().showMessage("New Status Added")
        self.lineEdit.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_14.setText("")
        self.comboBox_2.setCurrentIndex(0)

        self.db.close()

    # ---------------------
    def Show_All_Status(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cursor = self.db.cursor()

        cursor.execute(
            "SELECT student_name, rent_book , from_day, to_day FROM lib_status"
        )
        data = cursor.fetchall()
        # print(data)

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                # print(row, column, (str(item)))
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

        self.db.close()

    # ---------------------
    def Show_All_Students(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="lms1",
        )
        cursor = self.db.cursor()

        cursor.execute(
            """SELECT student_name, student_email, rent_book ,rent_duration_days 
            FROM lib_status"""
        )
        data = cursor.fetchall()
        # print(data)

        self.tableWidget_4.setRowCount(0)
        self.tableWidget_4.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1
            row_position = self.tableWidget_4.rowCount()
            self.tableWidget_4.insertRow(row_position)

        self.db.close()

    # ---------------------
    def m1(self):
        pass

    # Utility Functions


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        main_window = LibraryApp()
        main_window.show()
        sys.exit(app.exec_())
