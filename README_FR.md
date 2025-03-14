# BooksToScrape_ETL

**BooksToScrape_ETL** est un projet de données complet qui extrait les données du site [Books to Scrape](http://books.toscrape.com/), transforme et nettoie les données, les stocke dans une base de données MySQL et visualise les principaux indicateurs à l'aide de Python. Ce projet illustre un pipeline ETL (Extraction, Transformation, Chargement) ainsi que des techniques de nettoyage, d'analyse et de visualisation de données.

## Table des matières

- [Vue d'ensemble](#vue-densemble)
- [Structure du projet](#structure-du-projet)
- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Utilisation](#utilisation)
  - [Scraping et Insertion dans la base de données](#scraping-et-insertion-dans-la-base-de-données)
  - [Nettoyage et Analyse des données](#nettoyage-et-analyse-des-données)
  - [Visualisation des données](#visualisation-des-données)
  - [Script Principal Interactif](#script-principal-interactif)
- [Environnement de développement](#environnement-de-développement)
- [Configuration de la base de données](#configuration-de-la-base-de-données)
- [Licence](#licence)

## Vue d'ensemble

Ce projet a été développé dans le cadre d'un projet final pour un cours de sprint data. Il comprend :

- **Scraping** : Extraction des informations des livres (titre, prix, note et lien du produit) depuis toutes les pages du site Books to Scrape.
- **Insertion en base de données** : Stockage des données extraites dans une base de données MySQL après transformation.
- **Nettoyage et Analyse des données** : Chargement des données extraites, conversion des types de données, gestion des valeurs manquantes, création de colonnes calculées (ex. : catégories de prix) et normalisation des données catégorielles.
- **Visualisation** : Création de graphiques (diagrammes en barres, histogrammes, boxplots) à l’aide de Seaborn et Matplotlib pour mieux visualiser les résultats.

## Structure du projet

```plaintext
BooksToScrape_ETL/
├── images/                     # Dossier pour les images de visualisation (PNG)
├── input/                      # Dossier pour les fichiers d'entrée bruts (ex: books.csv)
├── output/                     # Dossier pour les fichiers générés (books.csv, books.json, books.xlsx, books_clean.csv)
├── scraping.py                 # Script pour le scraping et l'insertion en base de données MySQL
├── data_cleaning_analysis.py   # Script pour le nettoyage et l'analyse des données
├── data_visualization.py       # Script pour la création des visualisations
├── database.sql                # Script SQL pour créer la base de données et les tables MySQL
├── requirements.txt            # Liste des dépendances Python
├── README.md                   # Documentation en anglais (ce fichier)
└── README_FR.md                # Documentation en français (ce fichier)
```

## Fonctionnalités

- **Pipeline ETL** : Extraction automatisée des données depuis Books to Scrape.
- **Intégration MySQL** : Insertion des données dans une base MySQL avec prise en charge de l’Unicode.
- **Nettoyage des données** : Gestion des conversions, des valeurs manquantes, de la normalisation et ajout de colonnes calculées.
- **Visualisation des données** : Génération de visualisations en haute résolution (300 dpi) avec Seaborn et Matplotlib.
- **Structure modulaire** : Chaque étape du pipeline est encapsulée dans un script dédié.

## Prérequis

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

1. **Cloner le dépôt :**

   ```bash
   git clone https://github.com/your-username/BooksToScrape_ETL.git
   cd BooksToScrape_ETL
   ```

2. **Créer un environnement virtuel (optionnel mais recommandé) :**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. **Installer les dépendances :**

   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

### Scraping et Insertion dans la base de données

- **Script :** `scraping.py`
- **Description :** Ce script récupère les données des livres depuis le site Books to Scrape, les sauvegarde aux formats CSV, JSON et Excel dans le dossier **output**, et insère ces données dans une base de données MySQL.
- **Exécution :**

  ```bash
  python scraping.py
  ```

### Nettoyage et Analyse des données

- **Script :** `data_cleaning_analysis.py`
- **Description :** Ce script charge le fichier CSV brut (dans **output/books.csv**), nettoie et analyse les données (conversion, gestion des valeurs manquantes, normalisation et ajout de colonnes calculées), puis sauvegarde le fichier nettoyé en **output/books_clean.csv**.
- **Exécution :**

  ```bash
  python data_cleaning_analysis.py
  ```

### Visualisation des données

- **Script :** `data_visualization.py`
- **Description :** Ce script charge les données nettoyées depuis **output/books_clean.csv** et génère plusieurs visualisations (distribution des ratings, distribution des catégories de prix, histogramme des prix, boxplot des prix par rating). Les graphiques sont sauvegardés dans le dossier **images** en haute résolution (300 dpi).
- **Exécution :**

  ```bash
  python data_visualization.py
  ```

### Script Principal Interactif

- **Script :** `main.py`
- **Description :**  
  Ce script interactif orchestre l'ensemble du pipeline ETL en proposant un menu. Vous pouvez choisir d'exécuter individuellement les étapes de Scraping et Insertion en base de données, de Nettoyage et Analyse des données, ou de Visualisation des données, ou encore de lancer l'ensemble du pipeline d'un seul coup. Il utilise la bibliothèque **rich** pour afficher des messages colorés et conviviaux dans la console.
- **Exécution :**

  ```bash
  python main.py
  ```

## Environnement de développement

Ce projet a été développé avec [PyCharm](https://www.jetbrains.com/pycharm/), qui offre d'excellents outils pour le débogage, la gestion du code et les tests. Vous pouvez importer ce projet dans PyCharm en sélectionnant le répertoire du projet et en l'ouvrant comme nouveau projet. L'utilisation de l'environnement virtuel intégré de PyCharm est recommandée pour gérer les dépendances.

## Configuration de la base de données

- **Script SQL :** `database.sql`
- **Description :** Utilisez ce script dans MySQL Workbench ou votre client MySQL préféré pour créer la base de données et la table nécessaire au projet. Il configure la base de données `books_scrape` et une table `books` avec un support complet de l'Unicode.

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.
