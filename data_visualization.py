#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de visualisation pour Books to Scrape utilisant Seaborn.
Ce script charge les données nettoyées depuis le fichier CSV (situé dans le dossier 'output')
et génère plusieurs graphiques permettant d'analyser la répartition des livres :
    - Distribution des livres par rating
    - Distribution des livres par catégorie de prix
    - Histogramme des prix avec courbe KDE
    - Boxplot des prix par rating
Les graphiques sont affichés et sauvegardés sous forme d'images PNG dans le dossier 'images'
avec une résolution améliorée (dpi=300).
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Dossier de sortie pour les images
image_dir = "images"
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

def load_data(filename=None):
    """Charge les données nettoyées depuis le fichier CSV situé dans le dossier 'output'."""
    if filename is None:
        filename = os.path.join("output", "books_clean.csv")
    try:
        df = pd.read_csv(filename, encoding='utf-8')
        print("Données chargées pour visualisation depuis", filename)
        return df
    except Exception as e:
        print("Erreur lors du chargement des données :", e)
        return None

def plot_rating_distribution(df):
    """Crée un graphique en barres avec Seaborn pour la distribution des livres par rating."""
    plt.figure(figsize=(8, 6))
    sns.set_style("whitegrid")
    # Ajout de hue pour satisfaire la dépréciation et suppression de la légende
    ax = sns.countplot(x='rating_int', data=df, hue='rating_int', palette="viridis", order=sorted(df['rating_int'].unique()))
    ax.set_title("Nombre de livres par rating", fontsize=14)
    ax.set_xlabel("Rating", fontsize=12)
    ax.set_ylabel("Nombre de livres", fontsize=12)
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "rating_distribution_seaborn.png"), dpi=300)
    plt.show()

def plot_price_category_distribution(df):
    """Crée un graphique en barres avec Seaborn pour la distribution des livres par catégorie de prix."""
    plt.figure(figsize=(8, 6))
    sns.set_style("whitegrid")
    # Ajout de hue pour satisfaire la dépréciation et suppression de la légende
    ax = sns.countplot(x='price_category', data=df, hue='price_category', palette="Set2", order=['Low', 'Medium', 'High'])
    ax.set_title("Nombre de livres par catégorie de prix", fontsize=14)
    ax.set_xlabel("Catégorie de prix", fontsize=12)
    ax.set_ylabel("Nombre de livres", fontsize=12)
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "price_category_distribution_seaborn.png"), dpi=300)
    plt.show()

def plot_price_histogram(df):
    """Crée un histogramme des prix des livres avec une courbe KDE en fond."""
    plt.figure(figsize=(8, 6))
    sns.set_style("whitegrid")
    ax = sns.histplot(df['price'], bins=30, kde=True, color='skyblue', edgecolor='black')
    ax.set_title("Histogramme des prix des livres", fontsize=14)
    ax.set_xlabel("Prix", fontsize=12)
    ax.set_ylabel("Fréquence", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "price_histogram_seaborn.png"), dpi=300)
    plt.show()

def plot_boxplot_price_by_rating(df):
    """Crée un boxplot des prix par rating avec Seaborn."""
    plt.figure(figsize=(8, 6))
    sns.set_style("whitegrid")
    # Ajout de hue pour satisfaire la dépréciation et suppression de la légende
    ax = sns.boxplot(x='rating_int', y='price', data=df, hue='rating_int', palette="Set3", order=sorted(df['rating_int'].unique()))
    ax.set_title("Boxplot des prix par rating", fontsize=14)
    ax.set_xlabel("Rating", fontsize=12)
    ax.set_ylabel("Prix", fontsize=12)
    if ax.get_legend() is not None:
        ax.get_legend().remove()
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "boxplot_price_by_rating_seaborn.png"), dpi=300)
    plt.show()

def main():
    df = load_data()  # Charge depuis 'output/books_clean.csv'
    if df is None:
        return
    plot_rating_distribution(df)
    plot_price_category_distribution(df)
    plot_price_histogram(df)
    plot_boxplot_price_by_rating(df)

if __name__ == '__main__':
    main()