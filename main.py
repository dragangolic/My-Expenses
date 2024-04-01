from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QComboBox, QPushButton, QLineEdit, QDateEdit, QTableWidget, \
    QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtCore import QDate, Qt
import sys


# App Class
class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        # Main App Objects/Widgets
        # Create Objects
        self.resize(550, 500)
        self.setWindowTitle("My-Expenses")

        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()

        self.add_button = QPushButton("Add Expense")
        self.delete_button = QPushButton("Delete Expense")

        self.table = QTableWidget()
        self.table.setColumnCount(5)  # Id, date, category, amount, description
        self.table.setHorizontalHeaderLabels(['Id', 'Date', 'Category', 'Amount', 'Description'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.sortByColumn(1, Qt.DescendingOrder)

        # Design App with Layouts

        self.dropdown.addItems(["Food", "Transportation", "Rent", "Shopping", "Entertainment", "Bills", "Other"])

        self.setStyleSheet("""
                            QWidget {
                                    background-color: #b8c9e1;
                                    }
                            QLabel {
                                    color: #333
                                    font-size: 14px;
                                    }
                                    
                            QlineEdit, QComboBox, QDateEdit, QPushButton{
                                    background-color: #b8c9e1;
                                    color: #333;
                                    border: 1px solid #444;
                                    padding: 5px;
                                    }
                                    
                            QTableWidget{
                                    background-color: #b8c9e1;
                                    color: #333;
                                    border: 1px solid #444;
                                    selection-background-color: #ddd;    
                                    }
                            QPushButton{
                                    background-color: #4caf50;
                                    color: #fff;
                                    border: none;
                                    padding: 8px 16px;
                                    font-size:14px;
                                    }
                            QPushButton:hover{
                                    background-color: #45a049;
                                    }
                            """)

        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.addWidget(QLabel("Date:"))
        self.row1.addWidget(self.date_box)
        self.row1.addWidget(QLabel("Category:"))
        self.row1.addWidget(self.dropdown)

        self.row2.addWidget(QLabel("Amount:"))
        self.row2.addWidget(self.amount)
        self.row2.addWidget(QLabel("Description:"))
        self.row2.addWidget(self.description)

        self.row3.addWidget(self.add_button)
        self.row3.addWidget(self.delete_button)
        self.add_button.clicked.connect(self.add_expense)
        self.delete_button.clicked.connect(self.delete_expense)

        self.master_layout.addLayout(self.row1)
        self.master_layout.addLayout(self.row2)
        self.master_layout.addLayout(self.row3)

        self.master_layout.addWidget(self.table)

        self.setLayout(self.master_layout)

        self.load_table()

    def load_table(self):
        self.table.setRowCount(0)

        query = QSqlQuery("SELECT * FROM expenses")
        row = 0
        while query.next():
            expense_id = query.value(0)
            date = query.value(1)
            category = query.value(2)
            amount = query.value(3)
            description = query.value(4)

            # Add values to Table
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(expense_id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(category))
            self.table.setItem(row, 3, QTableWidgetItem(str(amount)))
            self.table.setItem(row, 4, QTableWidgetItem(description))

            row += 1

    def add_expense(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        category = self.dropdown.currentText()
        amount = self.amount.text()
        description = self.description.text()

        query = QSqlQuery()
        query.prepare("""
                        INSERT INTO expenses(date, category, amount, description)
                        VALUES(?, ?, ?, ?)
                        """)
        # Add binding value
        query.addBindValue(date)
        query.addBindValue(category)
        query.addBindValue(amount)
        query.addBindValue(description)
        query.exec_()

        # Prepare for the next input
        self.date_box.setDate(QDate.currentDate())
        self.dropdown.setCurrentIndex(0)
        self.amount.clear()
        self.description.clear()

        self.load_table()

    def delete_expense(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "No expense Chosen", "Please choose an expense to delete!")
            return

        expense_id = int(self.table.item(selected_row, 0).text())
        confirm = QMessageBox.question(self, "Are you sure?", "Delete Expense?", QMessageBox.Yes | QMessageBox.No)

        if confirm == QMessageBox.No:
            return

        query = QSqlQuery()
        query.prepare("Delete from expenses where id = ?")
        query.addBindValue(expense_id)
        query.exec_()

        self.load_table()

# Create database


database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName("expense.db")
if not database.open():
    QMessageBox.critical(None, "Error", "Could not open your Database")
    sys.exit()

# Initial query
query = QSqlQuery()
query.exec_("""
        CREATE TABLE IF NOT EXISTS expenses(
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT,
            Category TEXT,
            Amount REAL,
            Description TEXT
        )
        """)

# Run the App
if __name__ in "__main__":
    app = QApplication([])
    main = ExpenseApp()
    main.show()
    app.exec_()