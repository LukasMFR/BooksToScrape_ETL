# BooksToScrape_ETL

**BooksToScrape_ETL** est un projet de données complet qui extrait les données (y compris la **catégorie** des livres) du site [Books to Scrape](http://books.toscrape.com/), transforme et nettoie ces données, les stocke dans une base de données MySQL et visualise les principaux indicateurs à l'aide de Python. Ce projet illustre un pipeline ETL (Extraction, Transformation, Chargement) ainsi que des techniques de nettoyage, d'analyse et de **visualisation avancée** des données.

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

Ce projet a été développé dans le cadre d’un projet final pour un sprint data. Il comprend :

- **Scraping** : Extraction des informations des livres (titre, prix, note, lien du produit et **catégorie**) depuis toutes les pages du site Books to Scrape, avec un **scraping concurrent** pour accélérer l’exécution.
- **Insertion en base de données** : Stockage des données extraites dans une base de données MySQL après transformation.
- **Nettoyage et Analyse des données** :  
  - Conversion des types de données (prix, rating, etc.).  
  - Gestion des valeurs manquantes.  
  - Ajout de colonnes calculées (par exemple, **catégories de prix**, normalisation du titre et de la catégorie).  
  - Normalisation des données catégorielles (dont la colonne *category*).
- **Visualisation** : Création de **multiples** graphiques (diagrammes en barres, histogrammes, boxplots, **violin plots**, répartition des catégories, etc.) à l’aide de Seaborn et Matplotlib pour mieux visualiser les résultats.

## Structure du projet

```plaintext
BooksToScrape_ETL/
├── images/                     # Dossier pour les images de visualisation (PNG)
├── output/                     # Dossier pour les fichiers générés (CSV, JSON, Excel, books_clean.csv)
├── scraping.py                 # Script pour le scraping et l'insertion en base de données MySQL
├── data_cleaning_analysis.py   # Script pour le nettoyage et l'analyse des données
├── data_visualization.py       # Script pour la création des visualisations avancées
├── main.py                     # Script principal interactif orchestrant tout le pipeline
├── database.sql                # Script SQL pour créer la base de données et les tables MySQL
├── requirements.txt            # Liste des dépendances Python
└── README_FR.md                # Ce fichier (documentation en français)
```

## Fonctionnalités

- **Pipeline ETL** :  
  - **Scraping concurrent** via `concurrent.futures` pour parcourir rapidement toutes les pages du site.  
  - Extraction de la **catégorie** de chaque livre (par exemple "Historical Fiction").
- **Intégration MySQL** :  
  - Insertion des données dans une base MySQL avec support Unicode complet.  
  - Table `books` contenant les colonnes (title, price, rating, product_link, **category**, etc.).
- **Nettoyage des données** :  
  - Conversion des types (float, int, category).  
  - Gestion des valeurs manquantes.  
  - **Normalisation** du texte (suppression des accents, mise en minuscules).  
  - Colonnes calculées (catégorisation du prix, etc.).
- **Visualisations avancées** :  
  - Diagrammes en barres (répartition des ratings, top 10 catégories, etc.).  
  - **Violin plots**, boxplots, histogrammes avec KDE.  
  - Répartition des catégories (top 10, pie chart, distribution de **toutes** les catégories).  
  - Sauvegarde en haute résolution (300 dpi).
- **Structure modulaire** : Chaque étape (scraping, nettoyage, visualisation) est gérée par un script dédié, et un script **main** propose un menu interactif pour tout orchestrer.

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
- [tqdm](https://github.com/tqdm/tqdm)  
- [Rich](https://github.com/Textualize/rich)

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
- **Description :**  
  Ce script récupère les données des livres (titre, prix, rating, **catégorie**, lien) depuis le site Books to Scrape, les enregistre dans **output** (CSV, JSON, Excel) et insère ces données dans une base MySQL.  
  Il utilise la **parallélisation** via `ThreadPoolExecutor` pour parcourir plus rapidement les pages du site.
- **Exécution :**

  ```bash
  python scraping.py
  ```

### Nettoyage et Analyse des données

- **Script :** `data_cleaning_analysis.py`
- **Description :**  
  Ce script charge le fichier CSV brut (`output/books.csv`), nettoie et analyse les données :  
  - Conversion des types (prix en float, rating en int/catégorie).  
  - Gestion des valeurs manquantes.  
  - Ajout de colonnes calculées (par ex. `price_category`, normalisation de `title` et `category`).  
  - Sauvegarde du fichier nettoyé en `output/books_clean.csv`.
- **Exécution :**

  ```bash
  python data_cleaning_analysis.py
  ```

### Visualisation des données

- **Script :** `data_visualization.py`
- **Description :**  
  Ce script charge les données nettoyées (`output/books_clean.csv`) et génère **plusieurs** visualisations :  
  - Distribution des livres par rating (bar chart, violin plot).  
  - Distribution par catégorie de prix.  
  - Histogramme des prix (avec KDE).  
  - Boxplot des prix par rating.  
  - **Distribution des catégories** (top 10, pie chart, toutes les catégories).  
  - Boxplot des prix par catégorie (top 10).  
  Les graphiques sont sauvegardés dans **images** avec une résolution de **300 dpi**.
- **Exécution :**

  ```bash
  python data_visualization.py
  ```

### Script Principal Interactif

- **Script :** `main.py`
- **Description :**  
  Ce script interactif propose un **menu** permettant de lancer :  
  - Le scraping et l’insertion MySQL,  
  - Le nettoyage et l’analyse,  
  - La visualisation des données,  
  - Ou **l’ensemble du pipeline** d’un seul coup.  
  Il utilise la bibliothèque **rich** pour afficher des messages colorés et plus conviviaux dans la console.
- **Exécution :**

  ```bash
  python main.py
  ```

## Environnement de développement

Ce projet a été développé avec [PyCharm](https://www.jetbrains.com/pycharm/), offrant d’excellents outils pour le débogage, la gestion du code et les tests. Vous pouvez importer le projet dans PyCharm en ouvrant simplement le dossier du projet. L’utilisation de l’environnement virtuel (venv) de PyCharm est recommandée pour gérer les dépendances.

## Configuration de la base de données

- **Script SQL :** `database.sql`
- **Description :**  
  Utilisez ce script dans MySQL Workbench ou votre client MySQL favori pour créer la base de données et la table nécessaires au projet. Il configure la base `books_scrape` et la table `books`, en prenant en charge l’Unicode et en incluant une colonne **category**.

## Licence

Ce projet est sous licence MIT. Consultez le fichier [LICENSE](LICENSE) pour plus de détails.
