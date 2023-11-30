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
        font = QFont("Arial", 12)  # Set font type and size
        self.central_widget.setFont(font)  # Apply font to the central widget, affecting all child widgets

        # Dropdown for selecting the streaming service
        self.service_dropdown = QComboBox(self)
        self.service_dropdown.addItems(["Netflix", "Hulu", "Amazon", "Disney"])
        self.service_dropdown.setFont(font)

        # Initialize other dropdowns and search fields
        self.type_dropdown = QComboBox(self)
        self.country_dropdown = QComboBox(self)
        self.release_year_dropdown = QComboBox(self)
        self.rating_dropdown = QComboBox(self)
        self.title_search = QLineEdit(self)
        self.director_search = QLineEdit(self)
        self.cast_search = QLineEdit(self)

        # Populate dropdowns with data from the database
        self.populate_dropdowns()



        # Search bar and button
        self.search_bar = QLineEdit(self)
        self.search_bar.setFont(font)
        self.search_button = QPushButton('Search', self)
        self.search_button.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: 2px solid #4CAF50;
                        border-radius: 10px;
                        padding: 10px 20px;
                        text-align: center;

                        display: inline-block;
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

        # Table for displaying movie data
        self.table = QTableWidget(self)
        self.table.setColumnCount(11)  # Adjusting columns
        self.table.setHorizontalHeaderLabels(
            ['Type', 'Title', 'Director', 'Cast', 'Country', 'Date Added', 'Release Year', 'Rating', 'Duration',
             'Listed In', 'Description'])
        header = self.table.horizontalHeader()
        header_font = QFont("Arial", 12)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setFont(header_font)
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # Make columns spread evenly



        # Layout adjustments
        service_label = QLabel('Select Service:')
        service_label.setFont(font)
        self.layout.addWidget(service_label)
        self.layout.addWidget(self.service_dropdown)

        # search_label = QLabel('Search for a Movie:')
        # search_label.setFont(font)
        # self.layout.addWidget(search_label)
        # self.layout.addWidget(self.search_bar)
        # Layout for search options
        search_layout = QHBoxLayout()

        # Adding widgets to the search layout
        search_layout.addWidget(QLabel('Type:'))
        search_layout.addWidget(self.type_dropdown)
        search_layout.addWidget(QLabel('Country:'))
        search_layout.addWidget(self.country_dropdown)
        search_layout.addWidget(QLabel('Release Year:'))
        search_layout.addWidget(self.release_year_dropdown)
        search_layout.addWidget(QLabel('Rating:'))
        search_layout.addWidget(self.rating_dropdown)
        search_layout.addWidget(QLabel('Title:'))
        search_layout.addWidget(self.title_search)
        search_layout.addWidget(QLabel('Director:'))
        search_layout.addWidget(self.director_search)
        search_layout.addWidget(QLabel('Cast:'))
        search_layout.addWidget(self.cast_search)

        # Adding search layout to the main layout
        self.layout.addLayout(search_layout)
        self.layout.addWidget(self.search_button)
        self.layout.addWidget(self.table)

        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Movie Database Application")
        self.showMaximized()  # Maximize the window

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
