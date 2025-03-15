#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de scraping pour Books to Scrape avec insertion dans la base de données MySQL.
Ce script extrait pour chaque livre :
    - Le titre
    - Le prix
    - La note (rating)
    - Le lien vers la fiche produit

Le script parcourt toutes les pages du site et sauvegarde les données extraites
dans des fichiers CSV, JSON, Excel (dans un dossier 'output'), puis insère ces données dans la base de données MySQL.
"""

import os
import requests
from bs4 import BeautifulSoup
import csv
import json
import pandas as pd
import mysql.connector
from mysql.connector import Error
import concurrent.futures

# Définir le dossier de sortie pour les fichiers exportés
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def fetch_page(url):
    """
    Télécharge le contenu HTML de la page spécifiée en gérant l'encodage Unicode.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text
    except Exception as e:
        print(f"Erreur lors du téléchargement de la page {url} : {e}")
        return None

def parse_books(html):
    """
    Analyse le HTML et extrait les données des livres.
    Retourne une liste de dictionnaires contenant :
        - title      : le titre du livre
        - price      : le prix (en nombre décimal)
        - rating     : la note (1, 2, 3, 4, 5)
        - product_link : le lien absolu vers le détail du produit
    """
    soup = BeautifulSoup(html, 'html.parser')
    books = []
    articles = soup.find_all('article', class_='product_pod')

    # Dictionnaire pour convertir la note en entier
    rating_mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    for article in articles:
        h3 = article.find('h3')
        a_tag = h3.find('a')
        title = a_tag.get('title', '').strip()

        link = a_tag.get('href', '').strip()
        product_link = requests.compat.urljoin("http://books.toscrape.com/", link)

        # Extraction et conversion du prix
        price_tag = article.find('p', class_='price_color')
        price_str = price_tag.text.strip() if price_tag else "0"
        # Suppression du symbole '£' et conversion en float
        price_value = float(price_str.replace('£', '').strip())

        # Extraction et conversion de la note (rating)
        rating_tag = article.find('p', class_='star-rating')
        rating = 0  # valeur par défaut
        if rating_tag:
            classes = rating_tag.get("class", [])
            for cls in classes:
                if cls in rating_mapping:
                    rating = rating_mapping[cls]
                    break

        books.append({
            "title": title,
            "price": price_value,
            "rating": rating,
            "product_link": product_link
        })
    return books

def fetch_all_pages(base_url):
    """
    Parcourt toutes les pages du site en suivant la pagination.
    Retourne la liste complète des livres extraits.
    """
    current_url = base_url
    all_books = []
    while current_url:
        print("Scraping page :", current_url)
        html = fetch_page(current_url)
        if html is None:
            break
        books = parse_books(html)
        all_books.extend(books)
        soup = BeautifulSoup(html, 'html.parser')
        next_li = soup.find('li', class_='next')
        if next_li:
            next_a = next_li.find('a')
            if next_a:
                next_href = next_a.get('href')
                current_url = requests.compat.urljoin(current_url, next_href)
            else:
                break
        else:
            break
    return all_books

def fetch_all_pages_concurrent(base_url):
    """
    Parcourt toutes les pages du site en parallèle en suivant la pagination.
    On part du principe que le site comporte 50 pages (ou on peut extraire ce nombre depuis la première page).
    Retourne la liste complète des livres extraits.
    """
    # Récupérer la première page pour tenter d'extraire le nombre total de pages
    first_page_html = fetch_page(base_url)
    if not first_page_html:
        return []
    soup = BeautifulSoup(first_page_html, 'html.parser')
    # Tente d'extraire le nombre de pages depuis le texte "Page 1 of 50"
    current_page_text = soup.find("li", class_="current")
    if current_page_text:
        try:
            # Ex: "Page 1 of 50" => on récupère 50
            num_pages = int(current_page_text.get_text(strip=True).split()[-1])
        except Exception as e:
            print("Impossible d'extraire le nombre de pages, utilisation de 50 par défaut.")
            num_pages = 50
    else:
        num_pages = 50

    # Générer la liste des URLs : la première page est base_url, puis les pages suivantes
    urls = [base_url]
    for i in range(2, num_pages + 1):
        page_url = f"http://books.toscrape.com/catalogue/page-{i}.html"
        urls.append(page_url)

    books = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_page, urls)
        for html in results:
            if html:
                books.extend(parse_books(html))
    return books

def save_data_csv(books, filename="books.csv"):
    """
    Sauvegarde la liste des livres dans un fichier CSV dans le dossier 'output'.
    """
    if not books:
        print("Aucun livre à sauvegarder en CSV.")
        return
    keys = books[0].keys()
    try:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for book in books:
                writer.writerow(book)
        print(f"Les données ont été sauvegardées dans le fichier {filepath}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde en CSV : {e}")

def save_data_json(books, filename="books.json"):
    """
    Sauvegarde la liste des livres dans un fichier JSON dans le dossier 'output'.
    """
    try:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, mode='w', encoding='utf-8') as f:
            json.dump(books, f, ensure_ascii=False, indent=4)
        print(f"Les données ont été sauvegardées dans le fichier {filepath}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde en JSON : {e}")

def save_data_excel(books, filename="books.xlsx"):
    """
    Sauvegarde la liste des livres dans un fichier Excel dans le dossier 'output'.
    """
    try:
        filepath = os.path.join(output_dir, filename)
        df = pd.DataFrame(books)
        df.to_excel(filepath, index=False)
        print(f"Les données ont été sauvegardées dans le fichier {filepath}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde en Excel : {e}")

def insert_data_mysql(books, host='localhost', user='root', password='12345678', database='books_scrape'):
    """
    Insère la liste des livres dans la table MySQL après avoir vidé la table.
    Ajuste les paramètres de connexion (host, user, password) selon ta configuration.
    """
    connection = None  # Initialisation de la variable connection
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            auth_plugin='mysql_native_password'  # Pour contourner l'erreur d'authentification
        )
        if connection.is_connected():
            cursor = connection.cursor()
            # Vider la table avant d'insérer de nouvelles données
            cursor.execute("TRUNCATE TABLE books;")
            connection.commit()

            insert_query = """
                INSERT INTO books (title, price, rating, product_link)
                VALUES (%s, %s, %s, %s)
            """
            for book in books:
                data = (book['title'], book['price'], book['rating'], book['product_link'])
                cursor.execute(insert_query, data)
            connection.commit()
            print("Les données ont été insérées dans la base de données MySQL après vidage de la table.")
    except mysql.connector.Error as e:
        print("Erreur lors de l'insertion dans MySQL :", e)
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

def main():
    base_url = "http://books.toscrape.com/"
    print("Début du scraping du site :", base_url)

    books = fetch_all_pages_concurrent(base_url)
    print(f"{len(books)} livres trouvés.")

    # Affichage de quelques livres pour vérification
    for book in books[:5]:
        print(book)

    # Sauvegarde des données dans différents formats dans le dossier 'output'
    save_data_csv(books)
    save_data_json(books)
    save_data_excel(books)

    # Insertion des données dans la base de données MySQL
    # Ajustez host, user et password selon votre configuration
    insert_data_mysql(books)

if __name__ == "__main__":
    main()