#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Main interactive script for BooksToScrape_ETL.

This script provides an interactive menu to run:
1. Scraping and Database Insertion
2. Data Cleaning and Analysis
3. Data Visualization
4. Full ETL Pipeline
5. Exit

It uses the rich library to display colorful messages.
"""

import time
from rich.console import Console
from rich.panel import Panel

# Import project modules (ensure these are in the same directory)
import scraping
import data_cleaning_analysis
import data_visualization

console = Console()


def run_scraping():
    console.print(Panel("Starting Scraping Process...", style="bold green"))
    scraping.main()
    console.print(Panel("Scraping completed successfully.", style="bold green"))


def run_cleaning_analysis():
    console.print(Panel("Starting Data Cleaning and Analysis...", style="bold blue"))
    data_cleaning_analysis.main()
    console.print(Panel("Data Cleaning and Analysis completed successfully.", style="bold blue"))


def run_visualization():
    console.print(Panel("Starting Data Visualization...", style="bold magenta"))
    data_visualization.main()
    console.print(Panel("Data Visualization completed successfully.", style="bold magenta"))


def run_full_pipeline():
    console.print(Panel("Running Full ETL Pipeline...", style="bold yellow"))
    run_scraping()
    time.sleep(1)
    run_cleaning_analysis()
    time.sleep(1)
    run_visualization()
    time.sleep(1)
    console.print(Panel("Full ETL Pipeline executed successfully!", style="bold green"))


def interactive_menu():
    while True:
        console.print(Panel("BooksToScrape_ETL Interactive Menu", style="bold underline cyan"))
        console.print("[1] Run Scraping and Database Insertion")
        console.print("[2] Run Data Cleaning and Analysis")
        console.print("[3] Run Data Visualization")
        console.print("[4] Run Full ETL Pipeline")
        console.print("[5] Exit")

        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            run_scraping()
        elif choice == "2":
            run_cleaning_analysis()
        elif choice == "3":
            run_visualization()
        elif choice == "4":
            run_full_pipeline()
        elif choice == "5":
            console.print(Panel("Exiting. Goodbye!", style="bold red"))
            break
        else:
            console.print("[red]Invalid choice. Please try again.[/red]")
        console.print("\n")
        time.sleep(1)


def main():
    interactive_menu()


if __name__ == '__main__':
    main()
