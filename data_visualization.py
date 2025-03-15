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
    - Top 10 des catégories de livres (anglais et français)
    - Diagramme circulaire des 10 principales catégories (anglais et français)
    - Distribution de toutes les catégories (barres horizontales) (anglais et français)
    - Violin plot des prix par rating
    - Boxplot des prix pour le top 10 des catégories (anglais et français)
Les graphiques sont affichés et sauvegardés sous forme d'images PNG dans le dossier 'images'
avec une résolution de 300 dpi.
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
    """Graphique en barres pour la distribution des livres par rating."""
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
    """Graphique en barres pour la distribution des livres par catégorie de prix."""
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
    """Histogramme des prix avec courbe KDE."""
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
    """Boxplot des prix par rating."""
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

# Graphiques utilisant les catégories en anglais
def plot_top_categories_distribution_en(df):
    """Graphique en barres pour le top 10 des catégories (anglais)."""
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    cat_counts = df['category'].value_counts().nlargest(10).reset_index()
    cat_counts.columns = ['category', 'count']
    ax = sns.barplot(x='category', y='count', data=cat_counts, hue='category',
                     palette="coolwarm", dodge=False)
    ax.set_title("Top 10 des catégories de livres (Anglais)", fontsize=14)
    ax.set_xlabel("Catégorie", fontsize=12)
    ax.set_ylabel("Nombre de livres", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "top_categories_distribution_en.png"), dpi=300)
    plt.show()

def plot_category_pie_chart_en(df):
    """Diagramme circulaire pour le top 10 des catégories (anglais)."""
    plt.figure(figsize=(8, 8))
    cat_counts = df['category'].value_counts().nlargest(10)
    plt.pie(cat_counts.values, labels=cat_counts.index, autopct='%1.1f%%', startangle=140,
            colors=sns.color_palette("pastel"))
    plt.title("Répartition des 10 principales catégories (Anglais)", fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "category_pie_chart_en.png"), dpi=300)
    plt.show()

def plot_all_categories_distribution_en(df):
    """Graphique en barres horizontales pour toutes les catégories (anglais)."""
    plt.figure(figsize=(10, 12))
    sns.set_style("whitegrid")
    cat_counts = df['category'].value_counts().sort_values(ascending=True).reset_index()
    cat_counts.columns = ['category', 'count']
    ax = sns.barplot(x='count', y='category', data=cat_counts, hue='category',
                     palette="viridis", dodge=False)
    ax.set_title("Distribution de toutes les catégories de livres (Anglais)", fontsize=14)
    ax.set_xlabel("Nombre de livres", fontsize=12)
    ax.set_ylabel("Catégorie", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "all_categories_distribution_en.png"), dpi=300)
    plt.show()

def plot_boxplot_price_by_category_en(df):
    """Boxplot des prix pour le top 10 des catégories (anglais)."""
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    top10 = df['category'].value_counts().nlargest(10).index
    subset = df[df['category'].isin(top10)]
    ax = sns.boxplot(x='category', y='price', data=subset, hue='category', palette="Set1", dodge=False)
    ax.set_title("Boxplot des prix pour le top 10 des catégories (Anglais)", fontsize=14)
    ax.set_xlabel("Catégorie", fontsize=12)
    ax.set_ylabel("Prix", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "boxplot_price_by_category_en.png"), dpi=300)
    plt.show()

# Graphiques utilisant les catégories en français
def plot_top_categories_distribution_fr(df):
    """Graphique en barres pour le top 10 des catégories (français)."""
    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    cat_counts = df['category_fr'].value_counts().nlargest(10).reset_index()
    cat_counts.columns = ['category_fr', 'count']
    ax = sns.barplot(x='category_fr', y='count', data=cat_counts, hue='category_fr',
                     palette="coolwarm", dodge=False)
    ax.set_title("Top 10 des catégories de livres (Français)", fontsize=14)
    ax.set_xlabel("Catégorie (FR)", fontsize=12)
    ax.set_ylabel("Nombre de livres", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "top_categories_distribution_fr.png"), dpi=300)
    plt.show()

def plot_category_pie_chart_fr(df):
    """Diagramme circulaire pour le top 10 des catégories (français)."""
    plt.figure(figsize=(8, 8))
    cat_counts = df['category_fr'].value_counts().nlargest(10)
    plt.pie(cat_counts.values, labels=cat_counts.index, autopct='%1.1f%%', startangle=140,
            colors=sns.color_palette("pastel"))
    plt.title("Répartition des 10 principales catégories (Français)", fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "category_pie_chart_fr.png"), dpi=300)
    plt.show()

def plot_all_categories_distribution_fr(df):
    """Graphique en barres horizontales pour toutes les catégories (français)."""
    plt.figure(figsize=(10, 12))
    sns.set_style("whitegrid")
    cat_counts = df['category_fr'].value_counts().sort_values(ascending=True).reset_index()
    cat_counts.columns = ['category_fr', 'count']
    ax = sns.barplot(x='count', y='category_fr', data=cat_counts, hue='category_fr',
                     palette="viridis", dodge=False)
    ax.set_title("Distribution de toutes les catégories de livres (Français)", fontsize=14)
    ax.set_xlabel("Nombre de livres", fontsize=12)
    ax.set_ylabel("Catégorie (FR)", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "all_categories_distribution_fr.png"), dpi=300)
    plt.show()

def plot_boxplot_price_by_category_fr(df):
    """Boxplot des prix pour le top 10 des catégories (français)."""
    plt.figure(figsize=(12, 6))
    sns.set_style("whitegrid")
    top10 = df['category_fr'].value_counts().nlargest(10).index
    subset = df[df['category_fr'].isin(top10)]
    ax = sns.boxplot(x='category_fr', y='price', data=subset, hue='category_fr', palette="Set1", dodge=False)
    ax.set_title("Boxplot des prix pour le top 10 des catégories (Français)", fontsize=14)
    ax.set_xlabel("Catégorie (FR)", fontsize=12)
    ax.set_ylabel("Prix", fontsize=12)
    legend = ax.get_legend()
    if legend is not None:
        legend.remove()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(image_dir, "boxplot_price_by_category_fr.png"), dpi=300)
    plt.show()

def plot_violin_price_by_rating(df):
    """Violin plot des prix par rating."""
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

def main():
    df = load_data()  # Charge depuis 'output/books_clean.csv'
    if df is None:
        return
    plot_rating_distribution(df)
    plot_price_category_distribution(df)
    plot_price_histogram(df)
    plot_boxplot_price_by_rating(df)
    # Graphiques en anglais
    plot_top_categories_distribution_en(df)
    plot_category_pie_chart_en(df)
    plot_all_categories_distribution_en(df)
    plot_boxplot_price_by_category_en(df)
    # Graphiques en français
    plot_top_categories_distribution_fr(df)
    plot_category_pie_chart_fr(df)
    plot_all_categories_distribution_fr(df)
    plot_boxplot_price_by_category_fr(df)
    # Autre graphique commun
    plot_violin_price_by_rating(df)

if __name__ == '__main__':
    main()