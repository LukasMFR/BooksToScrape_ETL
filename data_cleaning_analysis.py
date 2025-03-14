#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de nettoyage et d'analyse des données pour Books to Scrape.
Ce script charge les données à partir du fichier CSV (situé dans le dossier 'output'),
nettoie et prépare les données en effectuant :
    - Conversion des types de données
    - Gestion des valeurs manquantes
    - Ajout de colonnes calculées pertinentes
    - Normalisation des catégories (textes et colonnes catégorielles)
Les données nettoyées sont ensuite sauvegardées dans un nouveau fichier CSV dans le dossier 'output'.
"""

import os
import pandas as pd
import numpy as np
import unicodedata

def load_data(filename=None):
    """Charge les données à partir du fichier CSV situé dans le dossier 'output'."""
    if filename is None:
        filename = os.path.join("output", "books.csv")
    try:
        df = pd.read_csv(filename, encoding='utf-8')
        print("Données chargées avec succès depuis", filename)
        return df
    except Exception as e:
        print("Erreur lors du chargement des données :", e)
        return None

def normalize_text(text):
    """Normalise le texte : supprime les accents et convertit en minuscules."""
    if isinstance(text, str):
        # Supprimer les accents
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        # Convertir en minuscules
        return text.lower().strip()
    return text

def clean_data(df):
    """Nettoyage et préparation des données."""
    print("Premières lignes des données brutes:")
    print(df.head())

    # Affichage des valeurs manquantes initiales
    print("\nValeurs manquantes par colonne AVANT nettoyage:")
    print(df.isnull().sum())

    # Gestion des valeurs manquantes
    df['title'] = df['title'].fillna("inconnu")
    df['price'] = df['price'].fillna(0)
    df['rating'] = df['rating'].fillna(0)
    df['product_link'] = df['product_link'].fillna("inconnu")

    # Conversion des types de données
    # Conversion du prix en nombre (float) : suppression éventuelle du symbole '£'
    if df['price'].dtype == object:
        df['price'] = df['price'].replace({'£': ''}, regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0)

    # Conversion du rating en entier puis en catégorie
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0).astype(int)

    # Normalisation du texte pour la colonne title (création d'une colonne normalisée)
    df['title_normalized'] = df['title'].apply(normalize_text)

    # Ajout d'une colonne calculée : catégorisation du prix
    # Exemple de catégorisation : Low (<20), Medium (20-50), High (>50)
    conditions = [
        (df['price'] < 20),
        (df['price'] >= 20) & (df['price'] <= 50),
        (df['price'] > 50)
    ]
    categories = ['Low', 'Medium', 'High']
    df['price_category'] = pd.cut(df['price'], bins=[-np.inf, 20, 50, np.inf], labels=categories)

    # Normalisation des colonnes catégorielles : conversion en type "category"
    df['price_category'] = df['price_category'].astype('category')
    df['rating'] = df['rating'].astype('category')

    # Affichage final des valeurs manquantes et des statistiques
    print("\nValeurs manquantes par colonne APRÈS nettoyage:")
    print(df.isnull().sum())
    print("\nStatistiques descriptives:")
    print(df.describe(include='all'))

    return df

def analyze_data(df):
    """Réalise quelques analyses descriptives sur les données nettoyées."""
    # Nombre de livres par rating
    rating_counts = df['rating'].value_counts().sort_index()
    print("\nNombre de livres par rating:")
    print(rating_counts)

    # Prix moyen par rating (attention : rating est une catégorie, on le convertit en int pour le calcul)
    df['rating_int'] = df['rating'].astype(int)
    avg_price_rating = df.groupby('rating_int')['price'].mean()
    print("\nPrix moyen par rating:")
    print(avg_price_rating)

    # Nombre de livres par catégorie de prix
    price_category_counts = df['price_category'].value_counts()
    print("\nNombre de livres par catégorie de prix:")
    print(price_category_counts)

def save_clean_data(df, filename=None):
    """Sauvegarde les données nettoyées dans un fichier CSV situé dans le dossier 'output'."""
    if filename is None:
        filename = os.path.join("output", "books_clean.csv")
    # Création du dossier de sortie s'il n'existe pas
    output_dir = os.path.dirname(filename)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    try:
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\nLes données nettoyées ont été sauvegardées dans {filename}")
    except Exception as e:
        print("Erreur lors de la sauvegarde des données :", e)

def main():
    df = load_data()
    if df is None:
        return

    df_clean = clean_data(df)
    analyze_data(df_clean)
    save_clean_data(df_clean)

if __name__ == '__main__':
    main()