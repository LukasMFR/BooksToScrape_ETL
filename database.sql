-- Active: 1737537456443@@127.0.0.1@3306@books_scrape
-- Création de la base de données avec gestion des caractères Unicode
CREATE DATABASE IF NOT EXISTS books_scrape
    DEFAULT CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Sélection de la base de données
USE books_scrape;

-- Création de la table "books" avec les modifications pour le prix et le rating
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    price DECIMAL(6,2) NOT NULL,
    rating INT NOT NULL,
    product_link VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Pour afficher les tables et leur contenu :
SHOW TABLES;
DESCRIBE books;
SELECT * FROM books;