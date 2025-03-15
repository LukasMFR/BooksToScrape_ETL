# BooksToScrape_ETL

**BooksToScrape_ETL** is an end-to-end data project that extracts data (including book **categories**) from the [Books to Scrape](http://books.toscrape.com/) website, transforms and cleans the data, stores it in a MySQL database, and visualizes key insights using Python. This project demonstrates an ETL (Extract, Transform, Load) pipeline along with data cleaning, analysis, and advanced visualization techniques.

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

- **Scraping**: Extracting book details (title, price, rating, product link, and **category**) from all pages of the Books to Scrape website. The scraping process uses **concurrent** requests for faster execution.
- **Database Insertion**: Storing the scraped data in a MySQL database after proper transformation.
- **Data Cleaning and Analysis**:  
  - Converting data types (price, rating).  
  - Handling missing values.  
  - Adding calculated columns (e.g., price categories, normalized titles/categories).  
  - Normalizing categorical data (including **category**).
- **Visualization**: Creating **multiple** visual representations (bar charts, histograms, boxplots, **violin plots**, category distributions, etc.) using Seaborn and Matplotlib for deeper insights.

## Project Structure

```plaintext
BooksToScrape_ETL/
├── images/                     # Folder for visualization images (PNG)
├── output/                     # Folder for generated files (CSV, JSON, Excel, cleaned data)
├── scraping.py                 # Script for scraping and inserting data into MySQL
├── data_cleaning_analysis.py   # Script for cleaning and analyzing the scraped data
├── data_visualization.py       # Script for generating multiple visualizations (including category-based)
├── main.py                     # Main interactive script orchestrating the entire pipeline
├── database.sql                # SQL script to create the MySQL database and tables
├── requirements.txt            # List of Python package dependencies
└── README.md                   # This file
```

## Features

- **ETL Pipeline**: Automated scraping from the Books to Scrape website with **multi-threaded** concurrency.
- **Category Extraction**: Collects both primary categories (e.g., "Historical Fiction") for each book via the breadcrumb.
- **MySQL Integration**: Inserts data into a MySQL database with proper Unicode support.
- **Data Cleaning**:  
  - Type conversion (float, int, category).  
  - Missing value handling.  
  - **Normalization** of text (e.g., removing accents, converting to lowercase).  
  - **Calculated columns** (e.g., price category, normalized category).  
- **Data Visualization**:  
  - Bar charts, histograms, boxplots, violin plots.  
  - **Category distribution** (top 10 and all categories).  
  - **Pie chart** for category proportions.  
  - High-resolution (300 dpi) visualizations using Seaborn and Matplotlib.
- **Modular Code Structure**: Each step of the pipeline is encapsulated in its own script, plus an interactive main script to tie everything together.

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
- [tqdm](https://github.com/tqdm/tqdm)
- [Rich](https://github.com/Textualize/rich)

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
- **Description:**  
  This script scrapes book data (including **category**) from the Books to Scrape website, saves the data in CSV, JSON, and Excel formats into the **output** folder, and inserts the data into a MySQL database.  
  It uses **concurrent.futures.ThreadPoolExecutor** to speed up scraping by processing multiple pages simultaneously.
- **Run the script:**

  ```bash
  python scraping.py
  ```

### Data Cleaning and Analysis

- **Script:** `data_cleaning_analysis.py`
- **Description:**  
  This script loads the raw CSV (`output/books.csv`), cleans and analyzes the data:  
  - Converts data types (price to float, rating to int/category).  
  - Handles missing values.  
  - Adds calculated columns (e.g., `price_category`, normalized `title` and `category`).  
  - Saves the cleaned data as `books_clean.csv` in the **output** folder.
- **Run the script:**

  ```bash
  python data_cleaning_analysis.py
  ```

### Data Visualization

- **Script:** `data_visualization.py`
- **Description:**  
  This script loads the cleaned data (`output/books_clean.csv`) and generates **multiple** visualizations:
  - Distribution of books by rating (bar chart, violin plot).  
  - Distribution of books by price category (bar chart).  
  - Histogram of prices with KDE.  
  - Boxplot of prices by rating.  
  - **Category distribution** (top 10 categories, pie chart, all categories in a horizontal bar chart).  
  - Boxplot of prices by category (top 10).  
  These visualizations are saved in the **images** folder with **300 dpi** resolution.
- **Run the script:**

  ```bash
  python data_visualization.py
  ```

### Main Interactive Script

- **Script:** `main.py`
- **Description:**  
  This interactive script orchestrates the entire ETL pipeline by offering a menu. You can choose to run individual parts—Scraping and Database Insertion, Data Cleaning and Analysis, Data Visualization—or run the full pipeline in one go. It uses the **rich** library for colorful, user-friendly console output.
- **Usage:**

  ```bash
  python main.py
  ```

## Development Environment

This project was developed using [PyCharm](https://www.jetbrains.com/pycharm/) for debugging, code management, and testing. You can import the project into PyCharm by opening the project directory. PyCharm's virtual environment support is recommended for dependency management.

## Database Setup

- **SQL Script:** `database.sql`
- **Description:**  
  Use this script in MySQL Workbench or your preferred MySQL client to create the database and table structure required for the project. It sets up the `books_scrape` database and a `books` table with proper Unicode settings, including a **category** column.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
