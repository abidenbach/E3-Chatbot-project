CREATE TABLE
   menu (
      id_menu INT,
      actif BOOLEAN NOT NULL DEFAULT FALSE,
      chemin VARCHAR(255) NOT NULL,
      date_ DATETIME NOT NULL,
      PRIMARY KEY (id_menu)
   );

CREATE TABLE 
   style_musical (
      id_style INT,
      label VARCHAR(255) NOT NULL,
      PRIMARY KEY (id_style)
   );

CREATE TABLE
   menu_produit (
      id_produit INT,
      label VARCHAR(255) NOT NULL,
      prix DECIMAL(10, 2) NOT NULL,
      id_menu INT NOT NULL,
      PRIMARY KEY (id_produit),
      FOREIGN KEY (id_menu) REFERENCES menu (id_menu)
   );

CREATE TABLE
   utilisateur (
      id_utilisateur INT,
      nom VARCHAR(191) NOT NULL,
      prenom VARCHAR(191) NOT NULL,
      mail VARCHAR(191) NOT NULL UNIQUE,
      motdepasse_hash VARCHAR(255) NOT NULL,
      PRIMARY KEY (id_utilisateur)
   );

CREATE TABLE
   salle (
      id_salle INT,
      label VARCHAR(50) NOT NULL,
      chemin VARCHAR(255),
      PRIMARY KEY (id_salle)
   );

CREATE TABLE
   contact (
      id_contact INT,
      tel VARCHAR(20) NOT NULL,
      adresse TEXT NOT NULL,
      mail VARCHAR(255) NOT NULL,
      PRIMARY KEY (id_contact)
   );

CREATE TABLE
   prompt (
      id_prompt INT,
      contexte TEXT NOT NULL,
      label VARCHAR(255) NOT NULL,
      PRIMARY KEY (id_prompt)
   );

CREATE TABLE
   chat (
      uuid_chat CHAR(36),
      created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      id_utilisateur INT NOT NULL,
      id_prompt INT NOT NULL,
      PRIMARY KEY (uuid_chat),
      FOREIGN KEY (id_utilisateur) REFERENCES utilisateur (id_utilisateur),
      FOREIGN KEY (id_prompt) REFERENCES prompt (id_prompt)
   );

CREATE TABLE
   message (
      uuid_message CHAR(36),
      role ENUM ('user', 'assistant') NOT NULL,
      contenu TEXT NOT NULL,
      date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
      uuid_chat CHAR(36) NOT NULL,
      PRIMARY KEY (uuid_message),
      FOREIGN KEY (uuid_chat) REFERENCES chat (uuid_chat)
   );

CREATE TABLE
   artiste (
      id_artiste INT,
      nom VARCHAR(255) NOT NULL,
      prenom VARCHAR(255) NOT NULL,
      nom_scene VARCHAR(255) NOT NULL,
      id_style INT NOT NULL,
      PRIMARY KEY (id_artiste),
      FOREIGN KEY (id_style) REFERENCES style_musical (id_style)
   );

CREATE TABLE
   concert (
      id_concert INT,
      label VARCHAR(255) NOT NULL,
      description TEXT NOT NULL,
      date_debut DATETIME NOT NULL,
      date_fin DATETIME NOT NULL,
      id_salle INT NOT NULL,
      id_artiste INT NOT NULL,
      PRIMARY KEY (id_concert),
      FOREIGN KEY (id_salle) REFERENCES salle (id_salle),
      FOREIGN KEY (id_artiste) REFERENCES artiste (id_artiste)
   );

CREATE TABLE
   billet (
      id_billet INT,
      date_achat DATETIME NOT NULL,
      date_valide DATETIME,
      id_utilisateur INT NOT NULL,
      id_concert INT NOT NULL,
      PRIMARY KEY (id_billet),
      FOREIGN KEY (id_utilisateur) REFERENCES utilisateur (id_utilisateur),
      FOREIGN KEY (id_concert) REFERENCES concert (id_concert)
   );