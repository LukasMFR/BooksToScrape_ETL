#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de scraping pour Books to Scrape avec insertion dans la base de données MySQL.
Ce script extrait pour chaque livre :
    - Le titre
    - Le prix
    - La note (rating)
    - Le lien vers la fiche produit
    - La catégorie (ex. "Historical Fiction")

Le script parcourt toutes les pages du site et sauvegarde les données extraites
dans des fichiers CSV, JSON, Excel (dans un dossier 'output'), puis insère ces données dans la base de données MySQL.
Il affiche également la durée totale du scraping.
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
from urllib.parse import urljoin
import time
from tqdm import tqdm  # pour afficher la progression
from tqdm import tqdm  # Pour afficher la progression

# Définir le dossier de sortie pour les fichiers exportés
output_dir = "output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Création d'une session globale pour réutiliser les connexions
session = requests.Session()

def fetch_page(url):
    """
    Télécharge le contenu HTML de la page spécifiée en gérant l'encodage Unicode.
    Retourne un tuple (html, effective_url) ou (None, url) en cas d'erreur.
    """
    try:
        response = session.get(url)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return response.text, response.url
    except Exception as e:
        print(f"Erreur lors du téléchargement de la page {url} : {e}")
        time.sleep(0.2)
        return None, url

def fetch_category(product_link):
    """
    Récupère la catégorie du livre en analysant la page détaillée (product_link).
    Retourne la catégorie (ex. 'Historical Fiction') ou None si introuvable.
    """
    detail_html, _ = fetch_page(product_link)
    if not detail_html:
        return None

    soup_detail = BeautifulSoup(detail_html, "html.parser")
    breadcrumb = soup_detail.find("ul", class_="breadcrumb")
    if breadcrumb:
        links = breadcrumb.find_all("a")
        # Sur Books To Scrape, le fil d'ariane typique est : Home > Books > [Category] > [Titre sans lien]
        if len(links) >= 3:
            return links[-1].get_text(strip=True)
    return None

def parse_books(html, page_url):
    """
    Analyse le HTML et extrait les données des livres de la page.
    Retourne une liste de dictionnaires contenant :
        - title        : le titre du livre
        - price        : le prix (float)
        - rating       : la note (1, 2, 3, 4, 5)
        - product_link : le lien absolu vers le détail du produit
        - category     : la catégorie extraite de la page de détail
    """
    soup = BeautifulSoup(html, 'html.parser')
    books_data = []
    articles = soup.find_all('article', class_='product_pod')

    # Dictionnaire pour convertir la note en entier
    rating_mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    # Première boucle : extraire les infos de base et collecter les liens produits
    product_links = []
    for article in articles:
        h3 = article.find('h3')
        a_tag = h3.find('a')
        title = a_tag.get('title', '').strip()

        link = a_tag.get('href', '').strip()
        # Utiliser page_url pour résoudre correctement les liens relatifs
        product_link = urljoin(page_url, link)
        product_links.append(product_link)

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

        books_data.append({
            "title": title,
            "price": price_value,
            "rating": rating,
            "product_link": product_link,
            "category": None  # à renseigner ensuite
        })

    # Deuxième boucle : récupérer les catégories en parallèle pour chaque produit
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        categories = list(tqdm(executor.map(fetch_category, product_links),
                               total=len(product_links),
                               desc="Récupération des catégories"))
    # Affecter les catégories aux livres
    for i, book in enumerate(books_data):
        book["category"] = categories[i]

    return books_data

def fetch_all_pages(base_url):
    """
    Parcourt toutes les pages du site en suivant la pagination.
    Retourne la liste complète des livres extraits.
    """
    current_url = base_url
    all_books = []
    while current_url:
        print("Scraping page :", current_url)
        html, effective_url = fetch_page(current_url)
        if html is None:
            break
        books = parse_books(html, effective_url)
        all_books.extend(books)
        soup = BeautifulSoup(html, 'html.parser')
        next_li = soup.find('li', class_='next')
        if next_li:
            next_a = next_li.find('a')
            if next_a:
                next_href = next_a.get('href')
                current_url = urljoin(effective_url, next_href)
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
    first_html, first_effective_url = fetch_page(base_url)
    if not first_html:
        return []
    soup = BeautifulSoup(first_html, 'html.parser')
    current_page_text = soup.find("li", class_="current")
    if current_page_text:
        try:
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
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(fetch_page, urls))
        # Utilisation de tqdm pour afficher la progression dans le traitement des pages
        for html, effective_url in tqdm(results, total=len(results), desc="Traitement des pages listing"):
            if html:
                books.extend(parse_books(html, effective_url))
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
    AVANT d'exécuter ce script, assurez-vous que la table 'books'
    contient bien une colonne 'category' (ex. ALTER TABLE books ADD COLUMN category VARCHAR(255);).
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("TRUNCATE TABLE books;")
            connection.commit()

            insert_query = """
                INSERT INTO books (title, price, rating, product_link, category)
                VALUES (%s, %s, %s, %s, %s)
            """
            for book in books:
                data = (
                    book['title'],
                    book['price'],
                    book['rating'],
                    book['product_link'],
                    book['category']
                )
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
    start_time = time.time()  # Démarrage du chronomètre

    books = fetch_all_pages_concurrent(base_url)
    duration = time.time() - start_time  # Durée totale du scraping
    print(f"{len(books)} livres trouvés en {duration:.2f} secondes.")

    # Affichage de quelques livres pour vérification
    for book in books[:5]:
        print(book)

    # Sauvegarde des données dans différents formats dans le dossier 'output'
    save_data_csv(books)
    save_data_json(books)
    save_data_excel(books)

    # Insertion des données dans la base de données MySQL
    insert_data_mysql(books)

if __name__ == "__main__":
    main()