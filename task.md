# Plan de Progression MSPR - Projet Electio-Analytics
**Rôle :** Chef de Projet Data
**Objectif :** Finaliser le POC de prévision électorale sur la zone Nouvelle-Aquitaine.

Ce document sert de checklist interactive pour suivre l'avancement global d'ici la soutenance. Cochez les cases au fur et à mesure de l'accomplissement des tâches.

## Phase 1 : Cadrage & Justification
**Objectif :** Poser les fondations du projet et justifier notre approche.

- [ ] **Justification du Périmètre Géographique**
  - [ ] Rédiger l'argumentaire sur le choix de la Nouvelle-Aquitaine en tant que "microcosme" représentatif (diversité urbaine/rurale ciblée, disparités des revenus, etc.).
- [ ] **Définition des Indicateurs Socio-Économiques Clés**
  - [ ] Sélectionner et documenter les variables explicatives : Taux de chômage.
  - [ ] Sélectionner et documenter les variables explicatives : Indices de sécurité/délinquance.
  - [ ] Sélectionner et documenter les variables explicatives : Données démographiques (âge, densité de population).
- **Livrables attendus :** Document de cadrage (Note d'intention) ou slide dédié dans la présentation.

## Phase 2 : Data Engineering (ETL)
**Objectif :** Alimenter la base de données avec des flux propres et exploitables.

- [ ] **Extraction des Données (Extract)**
  - [ ] Automatiser/Documenter le téléchargement des sources depuis `data.gouv.fr` (et potentiellement INSEE, Ministère de l'Intérieur).
- [ ] **Nettoyage et Transformation (Transform)**
  - [ ] Uniformiser les libellés géographiques (codes insee, noms de communes).
  - [ ] Gérer les valeurs manquantes ou aberrantes avec Pandas (imputation, suppression).
  - [ ] Joindre les données électorales avec les indicateurs socio-économiques.
- [ ] **Stockage et Architecture (Load)**
  - [ ] Importer les dataframes propres dans une base de données SQL structurée (ou schématiser le flux pour le POC).
- **Livrables attendus :** Scripts Python (Jupyter Notebooks) pour le nettoyage, schéma de la chaîne de traitement de données (Pipeline ETL).

## Phase 3 : Data Science & Modélisation
**Objectif :** Entraîner et valider le modèle prédictif.

- [ ] **Préparation des Données pour l'Apprentissage**
  - [ ] Encodage des variables catégorielles.
  - [ ] Découpage du dataset en échantillons d'entraînement et de test (Train/Test split - ex: 80/20).
- [ ] **Entraînement du Modèle**
  - [ ] Implémenter l'algorithme d'apprentissage supervisé (Choix ciblé : **XGBoost**).
  - [ ] Ajuster les hyperparamètres du modèle.
- [ ] **Évaluation des Performances**
  - [ ] Calculer l'Accuracy globale (objectif cible : **82.4%** vérifiés en conditions réelles).
  - [ ] Analyser la matrice de confusion et l'importance des "features" (impact du chômage/sécurité sur le vote).
- **Livrables attendus :** Notebooks de modélisation (Train, Test, Évaluation), Export du modèle entraîné (ex: `.pkl`).

## Phase 4 : Data Visualisation & Prospective
**Objectif :** Restituer l'information aux utilisateurs finaux de façon digeste et fournir les projections.

- [ ] **Dashboard Interactif (Application Web)**
  - [ ] Mettre à jour l'application Flask/Frontend avec les visuels finaux.
- [ ] **Intégration des Visuels Manquants**
  - [ ] Générer et intégrer la **Matrice de corrélation** (lien entre indicateurs et vote).
  - [ ] Intégrer les **Heatmaps régionales** (Cartographie des résultats et des niveaux socio-éco).
  - [ ] Implémenter et afficher les **Courbes de prévision prospective (1 an, 2 ans, 3 ans)** selon différents scénarios simulés.
- **Livrables attendus :** Code de l'application (Dashboard) fonctionnel contenant tous les graphiques requis.

## Phase 5 : Synthèse & Soutenance
**Objectif :** Préparer les rendus finaux de l'EPSI et l'oral.

- [ ] **Modélisation Théorique**
  - [ ] Finaliser et intégrer le **Modèle Conceptuel de Données (MCD)** qui représente la structure des données du projet.
- [ ] **Dossier/Rapport Final**
  - [ ] Rédiger le rapport résumant la méthodologie, les défis techniques, l'argumentaire métier et les conclusions.
- [ ] **Support de Présentation (Oral de 20 min)**
  - [ ] Créer les slides de présentation (Context, Solution technique, Démo).
  - [ ] S'assurer que le fil rouge de la présentation respecte le timing pour la soutenance.
- **Livrables attendus :** Rapport de projet (PDF), Support de présentation (PPT/PDF).
