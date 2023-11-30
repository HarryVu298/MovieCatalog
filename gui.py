import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import mysql.connector


def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='minhkhoa2003dn',
            database='movies'
        )
        return connection
    except mysql.connector.Error as err:
        QMessageBox.critical(None, "Database Connection Error", f"Error connecting to database: {err}")
        return None


class MovieApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main widget and layout
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.central_widget.setStyleSheet(
            "background-color: #f0f0f0; color: black;")  # Set background color and text color
        font = QFont("Arial", 20)  # Set font type and size
        self.central_widget.setFont(font)  # Apply font to the central widget, affecting all child widgets

        # Dropdown for selecting the streaming service
        self.service_dropdown = QComboBox(self)
        self.service_dropdown.addItems(["Netflix", "Hulu", "Amazon", "Disney"])
        self.service_dropdown.setFont(font)

        # Search bar and button
        self.search_bar = QLineEdit(self)
        self.search_bar.setFont(font)
        self.search_button = QPushButton('Search', self)
        self.search_button.setFont(font)
        self.search_button.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        transition-duration: 0.4s;
                        cursor: pointer;
                    }
                    QPushButton:hover {
                        background-color: white;
                        color: black;
                    }
                """)
        self.search_button.clicked.connect(self.search_movies)

        # Table for displaying movie data
        self.table = QTableWidget(self)
        self.table.setColumnCount(11)  # Adjusting columns
        self.table.setHorizontalHeaderLabels(
            ['Type', 'Title', 'Director', 'Cast', 'Country', 'Date Added', 'Release Year', 'Rating', 'Duration',
             'Listed In', 'Description'])
        header = self.table.horizontalHeader()
        header.setFont(font)
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Make columns spread evenly

        # Layout adjustments
        service_label = QLabel('Select Service:')
        service_label.setFont(font)
        self.layout.addWidget(service_label)
        self.layout.addWidget(self.service_dropdown)

        search_label = QLabel('Search for a Movie:')
        search_label.setFont(font)
        self.layout.addWidget(search_label)
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.table)

        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Movie Database Application")
        self.showMaximized()  # Maximize the window


    def search_movies(self):
        search_term = self.search_bar.text()
        selected_service = self.service_dropdown.currentText()
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            query = f"SELECT * FROM {selected_service} WHERE title LIKE %s OR director LIKE %s"  # Modify query as needed
            cursor.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
            results = cursor.fetchall()
            self.update_table(results)
            cursor.close()
            connection.close()


    def update_table(self, data):
        self.table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for column_index, column_data in enumerate(row_data):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(column_data)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MovieApp()
    sys.exit(app.exec_())
