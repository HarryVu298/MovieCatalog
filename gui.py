import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
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

        # Search bar and button
        self.search_bar = QLineEdit(self)
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.search_movies)

        # Table for displaying movie data
        self.table = QTableWidget(self)
        self.table.setColumnCount(10)  # Adjust based on your data columns
        self.table.setHorizontalHeaderLabels(['Title', 'Director', 'Country', 'Release Year', 'Rating', 'Duration', 'Website', '...'])  # Add your headers here

        # Layout adjustments
        self.layout.addWidget(QLabel('Search for a Movie:'))
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.table)

        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Movie Database Application")



    def search_movies(self):
        search_term = self.search_bar.text()
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM movies WHERE title LIKE %s OR director LIKE %s"  # Modify query as needed
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
    mainWin.show()
    sys.exit(app.exec_())





