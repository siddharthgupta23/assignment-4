#"A simple billing system developed as a learning exercise to understand basic billing processes and Python programming.it is just example of billing system
import sys
import mysql.connector
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QTableWidget, QTableWidgetItem

# Database Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="123456789",
        database="billing_system_example"
    )

# Create Tables if not exists
def setup_database():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            amount DECIMAL(10,2) NOT NULL,
            description TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
        )
    """)
    db.commit()
    db.close()

# Main Application Class
class BillingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Billing System")
        self.setGeometry(100, 100, 600, 500)
        
        layout = QVBoxLayout()
        
        self.name_label = QLabel("Customer Name:")
        self.name_input = QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        
        self.phone_label = QLabel("Phone:")
        self.phone_input = QLineEdit()
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        
        self.amount_label = QLabel("Bill Amount:")
        self.amount_input = QLineEdit()
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        
        self.desc_label = QLabel("Description:")
        self.desc_input = QTextEdit()
        layout.addWidget(self.desc_label)
        layout.addWidget(self.desc_input)
        
        self.submit_button = QPushButton("Save Bill")
        self.submit_button.clicked.connect(self.save_bill)
        layout.addWidget(self.submit_button)
        
        self.retrieve_button = QPushButton("Retrieve Bills")
        self.retrieve_button.clicked.connect(self.retrieve_bills)
        layout.addWidget(self.retrieve_button)
        
        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)
        
        self.setLayout(layout)
    
    def save_bill(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()
        amount = self.amount_input.text()
        description = self.desc_input.toPlainText()
        
        if not (name and phone and email and amount):
            QMessageBox.warning(self, "Error", "All fields are required!")
            return
        
        db = connect_db()
        cursor = db.cursor()
        
        # Insert or retrieve customer
        cursor.execute("SELECT id FROM customers WHERE email = %s", (email,))
        customer = cursor.fetchone()
        if not customer:
            cursor.execute("INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s)", (name, phone, email))
            customer_id = cursor.lastrowid
        else:
            customer_id = customer[0]
        
        # Insert bill
        cursor.execute("INSERT INTO bills (customer_id, amount, description) VALUES (%s, %s, %s)", (customer_id, amount, description))
        db.commit()
        db.close()
        
        QMessageBox.information(self, "Success", "Bill Saved Successfully!")
    
    def retrieve_bills(self):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            SELECT customers.name, customers.phone, bills.amount, bills.description
            FROM bills INNER JOIN customers ON bills.customer_id = customers.id
        """)
        records = cursor.fetchall()
        db.close()
        
        self.result_table.setRowCount(len(records))
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Name", "Phone", "Amount", "Description"])
        
        for row_idx, row_data in enumerate(records):
            for col_idx, col_data in enumerate(row_data):
                self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

if __name__ == "__main__":
    setup_database()
    app = QApplication(sys.argv)
    window = BillingApp()
    window.show()
    sys.exit(app.exec())
