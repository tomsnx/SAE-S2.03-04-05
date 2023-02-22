DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS gant;
DROP TABLE IF EXISTS type_gant;
DROP TABLE IF EXISTS taille;
DROP TABLE IF EXISTS utilisateur;

CREATE TABLE utilisateur (
    id_utilisateur INT AUTO_INCREMENT PRIMARY KEY,
    login VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255),
    role VARCHAR(255),
    nom VARCHAR(255)
);

CREATE TABLE taille (
    id_taille INT AUTO_INCREMENT PRIMARY KEY,
    libelle_taille VARCHAR(255)
);

CREATE TABLE type_gant (
    id_type_gant INT AUTO_INCREMENT PRIMARY KEY,
    libelle_type_gant VARCHAR(255)
);

CREATE TABLE gant (
    id_gant INT AUTO_INCREMENT PRIMARY KEY,
    nom_gant VARCHAR(255),
    prix_gant NUMERIC(6,2),
    image_gant VARCHAR(255),
    stock_gant INT,
    id_taille INT,
    id_type_gant INT,
    FOREIGN KEY (id_taille) REFERENCES taille(id_taille),
    FOREIGN KEY (id_type_gant) REFERENCES type_gant(id_type_gant)
);

CREATE TABLE etat (
    id_etat INT AUTO_INCREMENT PRIMARY KEY,
    libelle_etat VARCHAR(255)
);

CREATE TABLE commande (
    id_commande INT AUTO_INCREMENT PRIMARY KEY,
    date_achat DATE,
    id_utilisateur INT,
    id_etat INT,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (id_etat) REFERENCES etat(id_etat)
);

CREATE TABLE ligne_commande (
    id_ligne_commande INT AUTO_INCREMENT PRIMARY KEY,
    id_commande INT,
    id_gant INT,
    prix NUMERIC(6,2),
    quantite INT,
    FOREIGN KEY (id_commande) REFERENCES commande(id_commande),
    FOREIGN KEY (id_gant) REFERENCES gant(id_gant)
);

CREATE TABLE ligne_panier (
    id_ligne_panier INT AUTO_INCREMENT PRIMARY KEY,
    id_utilisateur INT,
    id_gant INT,
    quantite INT,
    date_ajout DATE,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur),
    FOREIGN KEY (id_gant) REFERENCES gant(id_gant)
);

INSERT INTO utilisateur(id_utilisateur, login, email,
                        password,
                        role, nom)
VALUES (1, 'admin', 'admin@admin.fr',
        'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
        'ROLE_admin', 'admin'), 
       (2, 'client', 'client@client.fr',
        'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
        'ROLE_client', 'client'), 
       (3, 'client2', 'client2@client2.fr',
        'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
        'ROLE_client', 'client2');

INSERT INTO taille(id_taille, libelle_taille)
VALUES (null, 'XS'),
       (null, 'S'),
       (null, 'M'),
       (null, 'L'),
       (null, 'XL');

INSERT INTO type_gant(id_type_gant, libelle_type_gant)
VALUES (null, 'Gants de jardinage'),
       (null, 'Gants ignifugés'),
       (null, 'Gants de protection chimique'),
       (null, 'Gants de protection au froid');

INSERT INTO gant(id_gant, nom_gant, prix_gant, image_gant, stock_gant, id_taille, id_type_gant)
VALUES (null, 'super gant', 4000.99, 'gants1.png', 5, 2, 2),
       (null, 'gant de jardinage', 5.30, 'gants1.png', 5, 4, 1),
       (null, 'gant de savant', 8.60, 'gants1.png', 3, 3, 3),
       (null, 'gant en plastique jaune', 3.99, 'gants1.png', 12, 3, 3),
       (null, 'mouffle', 4.99, 'gants1.png', 9, 1, 4),
       (null, 'mitaine', 5.00, 'gants1.png', 1, 2, 4),
(null, 'gant en plastique violet', 3.99, 'gants1.png', 10, 1, 3),
(null, 'gant en plastique bleu', 3.99, 'gants1.png', 14, 2, 3),
(null, 'gant de pompier', 12.00, 'gants1.png', 1, 5, 2),
(null, 'gant de maître jardinier', 7.30, 'gants1.png', 8, 5, 1),
(null, 'gant de jardinier amateur', 3.30, 'gants1.png', 2, 3, 1);