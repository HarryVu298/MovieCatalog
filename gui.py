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
        self.main_layout = QVBoxLayout(self.central_widget)
        self.central_widget.setStyleSheet("background-color: #f0f0f0; color: black;")
        font = QFont("Arial", 14)
        self.central_widget.setFont(font)

        # Dropdown for selecting the streaming service
        self.service_dropdown = QComboBox()
        self.service_dropdown.addItems(["Netflix", "Hulu", "Amazon", "Disney"])
        self.service_dropdown.setFont(font)

        # Initialize other dropdowns and search fields
        self.type_dropdown = QComboBox()
        self.country_dropdown = QComboBox()
        self.release_year_dropdown = QComboBox()
        self.rating_dropdown = QComboBox()
        self.title_search = QLineEdit()
        self.director_search = QLineEdit()
        self.cast_search = QLineEdit()

        # Set font for all dropdowns and search fields
        for widget in [self.type_dropdown, self.country_dropdown, self.release_year_dropdown,
                       self.rating_dropdown, self.title_search, self.director_search, self.cast_search]:
            widget.setFont(font)

        # Populate dropdowns with data from the database
        self.populate_dropdowns()

        # Layout for streaming service selection
        service_layout = QHBoxLayout()
        service_label = QLabel('Select Streaming Service:')
        service_label.setFont(font)
        service_layout.addWidget(service_label, alignment=Qt.AlignRight)
        service_layout.addWidget(self.service_dropdown)
        self.main_layout.addLayout(service_layout)

        # Layout for the first line of search options (Title, Type, Country, Release Year, Rating)
        first_line_layout = QHBoxLayout()
        s1 = QLabel('Title:')
        s1.setFont(font)
        first_line_layout.addWidget(s1)
        first_line_layout.addWidget(self.title_search)
        s1 = QLabel('Type:')
        s1.setFont(font)
        first_line_layout.addWidget(s1)
        first_line_layout.addWidget(self.type_dropdown)
        s1 = QLabel('Country:')
        s1.setFont(font)
        first_line_layout.addWidget(s1)
        first_line_layout.addWidget(self.country_dropdown)
        s1 = QLabel('Release Year:')
        s1.setFont(font)
        first_line_layout.addWidget(s1)
        first_line_layout.addWidget(self.release_year_dropdown)
        s1 = QLabel('Rating:')
        s1.setFont(font)
        first_line_layout.addWidget(s1)
        first_line_layout.addWidget(self.rating_dropdown)
        self.main_layout.addLayout(first_line_layout)

        # Layout for the second line of search options (Director, Cast)
        second_line_layout = QHBoxLayout()
        s1 = QLabel('Director:')
        s1.setFont(font)
        second_line_layout.addWidget(s1)
        second_line_layout.addWidget(self.director_search)
        s1 = QLabel('Cast:')
        s1.setFont(font)
        second_line_layout.addWidget(s1)
        second_line_layout.addWidget(self.cast_search)
        self.main_layout.addLayout(second_line_layout)

        # Search button
        self.search_button = QPushButton('Search', self)
        bold_font = QFont("Arial", 16, QFont.Bold)  # Bold font
        self.search_button.setFont(bold_font)
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 10px 20px;
                font-size: 20px;
                margin: 4px 2px;
                transition-duration: 0.4s;
                cursor: pointer;
            }
            QPushButton:hover {
                background-color: white;
                color: black;
                border: 2px solid #4CAF50;
                box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
            }
        """)
        self.search_button.clicked.connect(self.search_movies)
        self.main_layout.addWidget(self.search_button)

        # Table for displaying movie data
        self.table = QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels(
            ['Type', 'Title', 'Director', 'Cast', 'Country', 'Date Added', 'Release Year', 'Rating', 'Duration', 'Listed In', 'Description'])
        header = self.table.horizontalHeader()
        header_font = QFont("Arial", 12)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_layout.addWidget(self.table)

        # Set central widget and its layout
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Movie Database Application")
        self.showMaximized()


    def populate_dropdowns(self):
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            dropdown_mappings = {
                "type": self.type_dropdown,
                "country": self.country_dropdown,
                "release_year": self.release_year_dropdown,
                "rating": self.rating_dropdown
            }
            for column, dropdown in dropdown_mappings.items():
                query = f"""
                SELECT DISTINCT {column} FROM movies.netflix
                UNION
                SELECT DISTINCT {column} FROM movies.hulu
                UNION
                SELECT DISTINCT {column} FROM movies.amazon
                UNION
                SELECT DISTINCT {column} FROM movies.disney
                ORDER BY {column};
                """
                cursor.execute(query)
                results = cursor.fetchall()
                dropdown.addItems([''] + [str(result[0]) for result in results if result[0] is not None])
            cursor.close()
            connection.close()

    def search_movies(self):
        # Get selected service
        selected_service = self.service_dropdown.currentText()

        # Gather search terms from dropdowns and text fields
        type_search = self.type_dropdown.currentText()
        country_search = self.country_dropdown.currentText()
        release_year_search = self.release_year_dropdown.currentText()
        rating_search = self.rating_dropdown.currentText()
        title_search = self.title_search.text()
        director_search = self.director_search.text()
        cast_search = self.cast_search.text()

        # Initialize a list to hold query conditions
        query_conditions = []

        # Add conditions based on user input
        if type_search:
            query_conditions.append(f"type LIKE '%{type_search}%'")
        if country_search:
            query_conditions.append(f"country LIKE '%{country_search}%'")
        if release_year_search:
            query_conditions.append(f"release_year = '{release_year_search}'")
        if rating_search:
            query_conditions.append(f"rating LIKE '%{rating_search}%'")
        if title_search:
            query_conditions.append(f"title LIKE '%{title_search}%'")
        if director_search:
            query_conditions.append(f"director LIKE '%{director_search}%'")
        if cast_search:
            query_conditions.append(f"cast LIKE '%{cast_search}%'")

        # Construct the WHERE clause of the query
        where_clause = ' AND '.join(query_conditions) if query_conditions else '1'

        # Final query
        query = f"SELECT type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description FROM {selected_service} WHERE {where_clause}"

        # Execute the query
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            self.update_table(results)
            cursor.close()
            connection.close()

    def update_table(self, data):
        self.table.setRowCount(len(data))
        for row_index, row_data in enumerate(data):
            for column_index, column_data in enumerate(row_data):
                item = QTableWidgetItem(str(column_data))
                # Set the item to be non-editable
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_index, column_index, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MovieApp()
    sys.exit(app.exec_())
