# BooksToScrape_ETL

**BooksToScrape_ETL** is an end-to-end data project that extracts data from the [Books to Scrape](http://books.toscrape.com/) website, transforms and cleans the data, stores it in a MySQL database, and visualizes key insights using Python. This project demonstrates an ETL (Extract, Transform, Load) pipeline along with data cleaning, analysis, and visualization techniques.

🇫🇷 **French Version:** [README_FR.md](README_FR.md)

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Scraping and Database Insertion](#scraping-and-database-insertion)
  - [Data Cleaning and Analysis](#data-cleaning-and-analysis)
  - [Data Visualization](#data-visualization)
  - [Main Interactive Script](#main-interactive-script)
- [Development Environment](#development-environment)
- [Database Setup](#database-setup)
- [License](#license)

## Overview

This project was developed as a final project for a data sprint course. It involves:

- **Scraping**: Extracting book details (title, price, rating, and product link) from all pages of the Books to Scrape website.
- **Database Insertion**: Storing the scraped data in a MySQL database after proper transformation.
- **Data Cleaning and Analysis**: Loading the scraped data, converting data types, handling missing values, creating calculated columns (e.g., price categories), and normalizing categorical data.
- **Visualization**: Creating visual representations (bar charts, histograms, boxplots) using Seaborn and Matplotlib for better insights.

## Project Structure

```plaintext
BooksToScrape_ETL/
├── images/                     # Folder for visualization images (PNG)
├── input/                      # Folder for raw input files (e.g., books.csv)
├── output/                     # Folder for generated files (books.csv, books.json, books.xlsx, books_clean.csv)
├── scraping.py                 # Script for scraping and inserting data into MySQL
├── data_cleaning_analysis.py   # Script for cleaning and analyzing the scraped data
├── data_visualization.py       # Script for generating visualizations
├── database.sql                # SQL script to create the MySQL database and tables
├── requirements.txt            # List of Python package dependencies
└── README.md                   # This file
```

## Features

- **ETL Pipeline**: Automated scraping from the Books to Scrape website.
- **MySQL Integration**: Inserts data into a MySQL database with proper Unicode support.
- **Data Cleaning**: Handles type conversion, missing values, normalization, and adds calculated columns.
- **Data Visualization**: Generates high-resolution (300 dpi) visualizations using Seaborn and Matplotlib.
- **Modular Code Structure**: Each step of the pipeline is encapsulated in its own script.

## Requirements

- Python 3.x
- [Requests](https://docs.python-requests.org/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [Pandas](https://pandas.pydata.org/)
- [MySQL Connector/Python](https://dev.mysql.com/doc/connector-python/en/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [openpyxl](https://pypi.org/project/openpyxl/)
- [NumPy](https://numpy.org/)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/LukasMFR/BooksToScrape_ETL.git
   cd BooksToScrape_ETL
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Scraping and Database Insertion

- **Script:** `scraping.py`
- **Description:** This script scrapes book data from the Books to Scrape website, saves the data in CSV, JSON, and Excel formats into the **output** folder, and inserts the data into a MySQL database.
- **Run the script:**

  ```bash
  python scraping.py
  ```

### Data Cleaning and Analysis

- **Script:** `data_cleaning_analysis.py`
- **Description:** This script loads the raw CSV (from **output/books.csv**), cleans and analyzes the data (conversion, missing values, normalization, and calculated columns), and saves the cleaned data as **books_clean.csv** in the **output** folder.
- **Run the script:**

  ```bash
  python data_cleaning_analysis.py
  ```

### Data Visualization

- **Script:** `data_visualization.py`
- **Description:** This script loads the cleaned data from **output/books_clean.csv** and generates several visualizations (rating distribution, price category distribution, price histogram, boxplot of prices by rating). The visualizations are saved in the **images** folder with high resolution (300 dpi).
- **Run the script:**

  ```bash
  python data_visualization.py
  ```

### Main Interactive Script

- **Script:** `main.py`
- **Description:**  
  This interactive script orchestrates the entire ETL pipeline by offering a menu. You can choose to run individual parts—Scraping and Database Insertion, Data Cleaning and Analysis, or Data Visualization—or run the full pipeline in one go. It uses the **rich** library for colorful, user-friendly console output.
- **Usage:**

  ```bash
  python main.py
  ```

## Development Environment

This project was developed using [PyCharm](https://www.jetbrains.com/pycharm/), which provides excellent tools for debugging, code management, and testing. You can easily import the project into PyCharm by selecting the project directory and opening it as a new project. PyCharm's virtual environment support is recommended for managing dependencies.

## Database Setup

- **SQL Script:** `database.sql`
- **Description:** Use this script in MySQL Workbench or your preferred MySQL client to create the database and table structure required for the project. It sets up the `books_scrape` database and a `books` table with proper Unicode settings.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
