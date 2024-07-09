# Harry Vu
20 November 2023

## PROJECT DOCUMENTATION
**Project Name:** Movie Database Application

### Overview
This project focuses on developing a graphical user interface (GUI) that enables users to filter movies from multiple streaming platforms and manage their personal watchlists. The data is maintained in a database, with SQL used for data retrieval.

### 1. Source Code
Source code files are included in the “source_code” folder which has these 2 files:
- `gui.py`: Python source code for the GUI
- `database.sql`: SQL file to create the schema and tables for GUI functionality.

Extra:
- “data_downloaded” folder: Contains 4 CSV files with original data before SQL conversion.

### 2. Documentation about the project
#### a. Reference to datasets
**Dataset Descriptions:** This dataset comprises movie information from four distinct streaming services: Amazon Prime, Disney+, Hulu, and Netflix.
- Amazon Prime Movies and TV Shows. https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows. Accessed 20 Nov. 2023.
- Disney+ Movies and TV Shows. https://www.kaggle.com/datasets/shivamb/disney-movies-and-tv-shows. Accessed 20 Nov. 2023.
- Hulu Movies and TV Shows. https://www.kaggle.com/datasets/shivamb/hulu-movies-and-tv-shows. Accessed 20 Nov. 2023.
- Netflix Movies and TV Shows. https://www.kaggle.com/datasets/shivamb/netflix-shows. Accessed 20 Nov. 2023.

#### b. References to external libraries
- `sys`: Used for interacting with the Python interpreter, accessing command-line arguments, and system-specific parameters.
- `PyQt5`: Creates graphical user interfaces (GUIs) for Python applications using the Qt framework.
- `mysql.connector`: Connects Python applications to MySQL databases for executing SQL queries, data retrieval, and database operations.
- `pycountry`: Provides access to ISO standards data like country, language, and currency codes for internationalization purposes.

#### c. Installation instructions
- Make sure to have MySQL server, MySQL Workbench, and python3 installed on your local machine.
- Run `database.sql` in MySQL Workbench to create the schema and tables.
- Install libraries via Terminal:
  ```sh
  python -m pip install --upgrade pip
  pip install PyQt5
  pip install mysql-connector-python
  pip install pycountry
