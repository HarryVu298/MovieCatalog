import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QComboBox, QHeaderView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
import mysql.connector
import pycountry

# Global variables for connection
# so that we do not have to open and
# close the connection multiple times - expensive
connection = None
cursor = None

# This is function to connect to the database (Connection + cursor)
def create_db_connection():
    # Try connect to the database
    # Show error if cannot connect
    try:
        global connection, cursor
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='minhkhoa2003dn',
            database='movies'
        )
        cursor = connection.cursor()
        return connection, cursor
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

        # Dropdown for selecting the streaming service/To-watch list
        self.service_dropdown = QComboBox()
        self.service_dropdown.addItems(["Netflix", "Hulu", "Amazon Prime", "Disney Plus", "My To-watch list"])
        self.service_dropdown.setFont(font)

        # Initialize other dropdowns and search fields
        self.type_dropdown = QComboBox()
        self.country_dropdown = QComboBox()
        countries = [country.name for country in pycountry.countries]
        self.country_dropdown.addItems(['']+ countries)
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
        service_label = QLabel('Select Streaming Service / Your to-watch list:')
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
        s1 = QLabel('Year:')
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
        s1 = QLabel('Actor/Actress:')
        s1.setFont(font)
        second_line_layout.addWidget(s1)
        second_line_layout.addWidget(self.cast_search)
        self.main_layout.addLayout(second_line_layout)

        # Search button
        self.search_button = QPushButton('Search', self)
        bold_font = QFont("Arial", 16, QFont.Bold)
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
        # Call search movies function when the user click the search button
        self.search_button.clicked.connect(self.search_movies)
        self.main_layout.addWidget(self.search_button)

        # Table for displaying movie data
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels(
            ['Type', 'Title', 'Director', 'Cast', 'Country', 'Date Added', 'Release Year', 'Rating', 'Duration', 'Listed In', 'Description', 'Action'])
        header = self.table.horizontalHeader()
        header_font = QFont("Arial", 12)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_layout.addWidget(self.table)
        self.table.cellClicked.connect(self.show_cell_content)

        # Set central widget and its layout
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)
        self.setWindowTitle("Movie Database Application")
        self.showMaximized()

    # Function to show cell content
    # when the user click on the cell
    def show_cell_content(self, row, column):
        # Retrieve the content of the clicked cell
        cell_content = self.table.item(row, column).text()
        # Display the content in a QMessageBox
        QMessageBox.information(self, "Cell Content", cell_content)

    # Populate the dropdowns options for search options
    # based on options available in the database
    def populate_dropdowns(self):
        dropdown_mappings = {
            "type": self.type_dropdown,
            # "country": self.country_dropdown,
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
            dropdown.addItems([''] + [str(result[0]) for result in results])


    # Method to search for movies based on search options
    def search_movies(self):
        # Get selected service
        if self.service_dropdown.currentText() == "Amazon Prime":
            selected_service = "amazon"
        elif self.service_dropdown.currentText() == "Disney Plus":
            selected_service = "disney"
        elif self.service_dropdown.currentText() == "My To-watch list":
            selected_service = "towatch"
        else:
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

        # Construct the WHERE clause
        where_clause = ' AND '.join(query_conditions) if query_conditions else '1'

        # Final query
        query = f"SELECT type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description FROM {selected_service} WHERE {where_clause} ORDER BY release_year DESC "

        # Execute the query
        cursor.execute(query)
        results = cursor.fetchall()
        self.update_table(results)

    # Method to update the table based on the data get from the database
    def update_table(self, data):
        if not data:
            # No data returned, display a message
            self.table.setRowCount(1)
            # Set to 1 column to display the message
            self.table.setColumnCount(1)
            self.table.setItem(0, 0, QTableWidgetItem("No movie matches your criteria."))
            # Clear other columns if they exist
            for i in range(1, 12):
                self.table.setItem(0, i, QTableWidgetItem(""))
                # Change header to "Message" when there is no matches
            self.table.setHorizontalHeaderLabels(["Message"])
            return 0
        else:
            self.table.setRowCount(len(data))
            # Original number of columns
            # Reset the tables columns when there is data returned
            self.table.setColumnCount(12)
            self.table.setHorizontalHeaderLabels(
                ['Type', 'Title', 'Director', 'Cast', 'Country', 'Date Added', 'Release Year', 'Rating', 'Duration', 'Listed In', 'Description', 'Action'])
        # put the data into the table
        for row_index, row_data in enumerate(data):
            for column_index, column_data in enumerate(row_data):
                item = QTableWidgetItem(str(column_data))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row_index, column_index, item)

            # If it is not "to-watch list", then add 'Add to Watchlist'
            # button into the action column
            # Add "remove" otherwise
            if self.service_dropdown.currentText() != "My To-watch list":
                # Add "Add to Watchlist" button
                watchlist_button = QPushButton('Add to Watchlist')
                watchlist_button.setStyleSheet("""
                QPushButton {
                    background-color: #95e898;
                    color: black;
                    border: 2px solid #4CAF50;
                    border-radius: 10px;
                    transition-duration: 0.4s;
                    cursor: pointer;
                }
                QPushButton:hover {
                    background-color: white;
                    border: 2px solid #4CAF50;
                    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                }
            """)
                watchlist_button.clicked.connect(lambda checked, row=row_index: self.add_to_watchlist(row))
                self.table.setCellWidget(row_index, 11, watchlist_button)
            else:
                # Add "Remove" button
                remove_button = QPushButton('Remove')
                remove_button.setStyleSheet("""
                                QPushButton {
                                    background-color: #95e898;
                                    color: black;
                                    border: 2px solid #4CAF50;
                                    border-radius: 10px;
                                    transition-duration: 0.4s;
                                    cursor: pointer;
                                }
                                QPushButton:hover {
                                    background-color: white;
                                    border: 2px solid #4CAF50;
                                    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                                }
                            """)
                remove_button.clicked.connect(lambda checked, row=row_index: self.remove_from_watchlist(row))
                self.table.setCellWidget(row_index, 11, remove_button)

    # Function to add the movie to watchlist when the user click the button
    def add_to_watchlist(self, row):
        # Retrieve movie details from the row
        movie_data = [self.table.item(row, col).text() for col in range(self.table.columnCount() - 1)]

        # Connect to the database and check if the movie is already in the watchlist
        # Ensure the 'towatch' table exists
        # if not, create one
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movies.towatch (
                id INT AUTO_INCREMENT PRIMARY KEY,
                type varchar(7),
                title varchar(1040),
                director varchar(2080),
                cast varchar(3000),
                country varchar(248),
                date_added varchar(19),
                release_year varchar(4),
                rating varchar(100),
                duration varchar(10),
                listed_in varchar(79),
                description varchar(3000)
            );
        """)

        # Check if the movie is already in the watchlist
        check_query = "SELECT count(*) FROM movies.towatch WHERE title = %s"
        # movie_data[1] is the title
        cursor.execute(check_query, (movie_data[1],))
        if cursor.fetchone()[0] > 0:
            QMessageBox.information(self, "Already Added", f"'{movie_data[1]}' has already been added to your watchlist before.")
        else:
            # Add movie to the 'towatch' table if not already present
            insert_query = "insert into movies.towatch (type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, tuple(movie_data))
            connection.commit()
            # Message when add successfully
            QMessageBox.information(self, "Added to Watchlist", f"'{movie_data[1]}' has been added to your watchlist.")

    # Remove from the watchlist function
    def remove_from_watchlist(self, row):
        # Retrieve the title of the movie from the row
        title = self.table.item(row, 1).text()
        # Connect to the database to remove the movie from the watchlist
        # SQL query to delete the movie from the 'towatch' table
        delete_query = "delete from movies.towatch where title = %s"
        cursor.execute(delete_query, (title,))
        connection.commit()
        # Message for remove successfully
        QMessageBox.information(self, "Removed from Watchlist", f"'{title}' has been removed from your watchlist.")
        self.search_movies()


if __name__ == "__main__":
    create_db_connection()
    app = QApplication(sys.argv)
    mainWin = MovieApp()
    exit_code = app.exec_()
    if connection.is_connected():
        cursor.close()
        connection.close()
    sys.exit(exit_code)
