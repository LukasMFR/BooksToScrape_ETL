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
    - Top 10 des catégories de livres (barres)
    - Diagramme circulaire des 10 principales catégories
    - Distribution de toutes les catégories (barres horizontales)
    - Violin plot des prix par rating
    - Boxplot des prix pour les 10 catégories les plus représentées
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
        # Création de la colonne rating_int à partir de la colonne rating (convertie en int)
        if 'rating' in df.columns:
            df['rating_int'] = df['rating'].astype(int)
        return df
    except Exception as e:
        print("Erreur lors du chargement des données :", e)
        return None

def plot_rating_distribution(df):
    """Crée un graphique en barres avec Seaborn pour la distribution des livres par rating."""
    plt.figure(figsize=(8, 6))
    sns.set_style("whitegrid")
    ax = sns.countplot(x='rating_int', data=df, hue='rating_int', palette="viridis",
                       order=sorted(df['rating_int'].unique()), dodge=False)
    ax.set_title("Nombre de livres par rating", fontsize=14)
    ax.set_xlabel("Rating", fontsize=12)
    ax.set_ylabel("Nombre de livres", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "rating_distribution_seaborn.png"), dpi=300)
    plt.show()

def plot_price_category_distribution(df):
    """Crée un graphique en barres avec Seaborn pour la distribution des livres par catégorie de prix."""
    plt.figure(figsize=(8, 6))
    sns.set_style("whitegrid")
    ax = sns.countplot(x='price_category', data=df, hue='price_category', palette="Set2",
                       order=['Low', 'Medium', 'High'], dodge=False)
    ax.set_title("Nombre de livres par catégorie de prix", fontsize=14)
    ax.set_xlabel("Catégorie de prix", fontsize=12)
    ax.set_ylabel("Nombre de livres", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
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
    ax = sns.boxplot(x='rating_int', y='price', data=df, hue='rating_int', palette="Set3",
                     order=sorted(df['rating_int'].unique()), dodge=False)
    ax.set_title("Boxplot des prix par rating", fontsize=14)
    ax.set_xlabel("Rating", fontsize=12)
    ax.set_ylabel("Prix", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "boxplot_price_by_rating_seaborn.png"), dpi=300)
    plt.show()

def plot_top_categories_distribution(df):
    """Crée un graphique en barres pour les 10 catégories les plus représentées."""
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    cat_counts = df['category'].value_counts().nlargest(10).reset_index()
    cat_counts.columns = ['category', 'count']
    ax = sns.barplot(x='category', y='count', data=cat_counts, hue='category', palette="coolwarm", dodge=False)
    ax.set_title("Top 10 des catégories de livres", fontsize=14)
    ax.set_xlabel("Catégorie", fontsize=12)
    ax.set_ylabel("Nombre de livres", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "top_categories_distribution.png"), dpi=300)
    plt.show()

def plot_category_pie_chart(df):
    """Crée un diagramme circulaire pour les 10 catégories les plus représentées."""
    plt.figure(figsize=(8, 8))
    cat_counts = df['category'].value_counts().nlargest(10)
    plt.pie(cat_counts.values, labels=cat_counts.index, autopct='%1.1f%%', startangle=140,
            colors=sns.color_palette("pastel"))
    plt.title("Répartition des 10 principales catégories", fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "category_pie_chart.png"), dpi=300)
    plt.show()

def plot_all_categories_distribution(df):
    """Crée un graphique en barres horizontales affichant la distribution de toutes les catégories."""
    plt.figure(figsize=(10, 12))
    sns.set_style("whitegrid")
    cat_counts = df['category'].value_counts().sort_values(ascending=True).reset_index()
    cat_counts.columns = ['category', 'count']
    ax = sns.barplot(x='count', y='category', data=cat_counts, hue='category', palette="viridis", dodge=False)
    ax.set_title("Distribution de toutes les catégories de livres", fontsize=14)
    ax.set_xlabel("Nombre de livres", fontsize=12)
    ax.set_ylabel("Catégorie", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "all_categories_distribution.png"), dpi=300)
    plt.show()

def plot_violin_price_by_rating(df):
    """Crée un violin plot pour visualiser la distribution des prix par rating."""
    plt.figure(figsize=(8, 6))
    sns.set_style("whitegrid")
    ax = sns.violinplot(x='rating_int', y='price', data=df, hue='rating_int', palette="Set2", dodge=False)
    ax.set_title("Violin plot des prix par rating", fontsize=14)
    ax.set_xlabel("Rating", fontsize=12)
    ax.set_ylabel("Prix", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "violin_price_by_rating.png"), dpi=300)
    plt.show()

def plot_boxplot_price_by_category(df):
    """Crée un boxplot des prix pour les 10 catégories les plus représentées."""
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    top10 = df['category'].value_counts().nlargest(10).index
    subset = df[df['category'].isin(top10)]
    ax = sns.boxplot(x='category', y='price', data=subset, hue='category', palette="Set1", dodge=False)
    ax.set_title("Boxplot des prix pour les 10 catégories les plus représentées", fontsize=14)
    ax.set_xlabel("Catégorie", fontsize=12)
    ax.set_ylabel("Prix", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "boxplot_price_by_category.png"), dpi=300)
    plt.show()

def main():
    df = load_data()  # Charge depuis 'output/books_clean.csv'
    if df is None:
        return
    plot_rating_distribution(df)
    plot_price_category_distribution(df)
    plot_price_histogram(df)
    plot_boxplot_price_by_rating(df)
    plot_top_categories_distribution(df)
    plot_category_pie_chart(df)
    plot_all_categories_distribution(df)
    plot_violin_price_by_rating(df)
    plot_boxplot_price_by_category(df)

if __name__ == '__main__':
    main()