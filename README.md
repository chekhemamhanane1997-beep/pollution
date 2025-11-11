# 🌍 Projet 1 : Analyse de la Qualité de l'Air et de la Pollution

**Cours**: 420-IAA-TT - Intelligence Artificielle 1  
**Institution**: Institut Teccart  
**Session**: Automne 2025  
**Professeur**: Benfriha Hichem

---

## 📋 Description du Projet

Ce projet consiste en une analyse complète des données de pollution atmosphérique au Canada. Il comprend une application web interactive développée avec Streamlit permettant d'explorer les données, de visualiser les tendances et d'interpréter les résultats de manière intuitive.

L'objectif principal est de comprendre comment différents facteurs environnementaux et démographiques (température, humidité, polluants chimiques, densité de population, proximité industrielle) influencent la qualité de l'air.

---

## 🎯 Objectifs

- ✅ Explorer et comprendre la structure du jeu de données
- ✅ Identifier les relations entre facteurs environnementaux et qualité de l'air
- ✅ Déterminer les variables les plus corrélées avec la pollution
- ✅ Créer une application Streamlit interactive
- ✅ Présenter un rapport complet et professionnel

---

## 📊 Données

Le jeu de données `pollution.csv` contient **5000 échantillons** avec les variables suivantes :

### Variables Environnementales
- **Temperature** (°C) : Température moyenne de la région
- **Humidity** (%) : Humidité relative
- **PM2.5** (µg/m³) : Particules fines en suspension
- **PM10** (µg/m³) : Particules grossières en suspension
- **NO2** (ppb) : Dioxyde d'azote
- **SO2** (ppb) : Dioxyde de soufre
- **CO** (ppm) : Monoxyde de carbone

### Variables Démographiques
- **Proximity_to_Industrial_Areas** (km) : Distance à la zone industrielle
- **Population_Density** (hab/km²) : Densité de population

### Variable Cible
- **Air_Quality** : Niveau de qualité de l'air
  - 0 = Bonne (air propre)
  - 1 = Modérée (acceptable)
  - 2 = Mauvaise (problèmes pour groupes sensibles)
  - 3 = Dangereuse (graves risques)

---

## 🚀 Installation et Exécution

### Prérequis
- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
pip install pandas numpy matplotlib seaborn scipy streamlit
```

### Exécution de l'analyse complète

```bash
python3.11 analyse_pollution.py
```

Ce script effectue :
- Chargement et exploration des données
- Nettoyage (valeurs manquantes et aberrantes)
- Statistiques descriptives complètes
- Analyse des corrélations
- Sauvegarde des données nettoyées

### Génération des visualisations

```bash
python3.11 visualisations.py
```

Ce script génère 11 visualisations professionnelles :
1. Distribution de la qualité de l'air
2. Histogrammes de toutes les variables
3. Histogrammes détaillés PM2.5 et PM10
4. Boxplots de toutes les variables
5. Boxplots détaillés PM2.5 et PM10
6. Graphes de densité
7. Heatmap de corrélation
8. Matrice de dispersion
9. Pairplot complet
10. Corrélations avec Air_Quality
11. Scatter plots des top 3 corrélations

### Lancement de l'application Streamlit

```bash
streamlit run app_streamlit.py
```

L'application sera accessible à l'adresse : `http://localhost:8501`

---

## 📁 Structure du Projet

```
projet_pollution/
│
├── pollution.csv                  # Données brutes
├── pollution_clean.csv            # Données nettoyées
│
├── analyse_pollution.py           # Script d'analyse complète
├── visualisations.py              # Script de génération des graphiques
├── app_streamlit.py               # Application web interactive
│
├── images/                        # Dossier des visualisations
│   ├── 01_distribution_air_quality.png
│   ├── 02_histogrammes_variables.png
│   ├── 03_histogrammes_pm25_pm10.png
│   ├── 04_boxplots_variables.png
│   ├── 05_boxplots_pm25_pm10.png
│   ├── 06_graphes_densite.png
│   ├── 07_heatmap_correlation.png
│   ├── 08_scatter_matrix.png
│   ├── 09_pairplot_complet.png
│   ├── 10_correlations_air_quality.png
│   └── 11_scatter_top3_correlations.png
│
├── rapport_final.md               # Rapport complet du projet
├── notes_analyse.md               # Notes d'analyse et observations
└── README.md                      # Ce fichier
```

---

## 📈 Résultats Principaux

### Top 3 des Contributeurs à la Pollution

1. **Température** (r = 0.743) - Corrélation forte positive
2. **SO₂** (r = 0.679) - Corrélation modérée positive
3. **NO₂** (r = 0.651) - Corrélation modérée positive

### Statistiques PM2.5 et PM10

| Statistique | PM2.5 (µg/m³) | PM10 (µg/m³) |
|-------------|---------------|--------------|
| Moyenne     | 18.023        | 28.221       |
| Médiane     | 12.000        | 21.700       |
| Écart-type  | 17.230        | 20.616       |

### Quartiles du CO

- Q1 (25%) : 1.030 ppm
- Q2 (50%) : 1.410 ppm
- Q3 (75%) : 1.840 ppm

---

## 🔍 Fonctionnalités de l'Application Streamlit

### 🏠 Accueil
- Présentation du projet
- Aperçu des données brutes
- Description des variables

### 🔍 Exploration des Données
- Types de données
- Dimensions du jeu de données
- Valeurs manquantes et traitement
- Statistiques descriptives complètes
- Distribution de la variable cible

### 📊 Visualisations
- Histogrammes interactifs
- Boîtes à moustaches
- Graphes de densité
- Diagrammes de dispersion
- Pairplots colorés

### 🔗 Étude de Corrélation
- Matrice de corrélation complète
- Heatmap interactive
- Top 3 des contributeurs
- Analyse détaillée des relations

### 📈 Analyse Approfondie
- Corrélation Humidité / Air Quality
- Lien Densité de Population / PM2.5
- Quartiles du CO
- Explorateur de statistiques interactif

---

## 📝 Réponses aux Questions du Projet

### 1. Types de données
Toutes les variables sont **quantitatives continues** (numériques).

### 2. Dimensions
**5000 échantillons** × **10 colonnes** (9 features + 1 target)

### 3. Valeurs manquantes
Quelques valeurs manquantes détectées dans les données brutes, **toutes traitées** dans le jeu nettoyé.

### 4. Technique de traitement
**Imputation par la médiane** (robuste aux outliers).

### 5. Facteurs les plus corrélés
Temperature (0.743), SO₂ (0.679), NO₂ (0.651), Humidity (0.624)

### 6. Trois principaux contributeurs
1. Temperature, 2. SO₂, 3. NO₂

### 7. Valeurs aberrantes PM2.5/PM10
Oui, détectées et **traitées par winsorisation**.

### 8. Statistiques PM2.5 et PM10
Voir tableau dans la section "Résultats Principaux".

### 9. Corrélation Humidité / Air Quality
**r = 0.624** (modérée positive)

### 10. Lien Population / PM2.5
**r = 0.009** (très faible)

### 11. Quartiles CO
Voir section "Résultats Principaux".

---

## 🎓 Recommandations

1. **Réglementation des émissions industrielles** : Renforcer les normes pour SO₂ et NO₂
2. **Politiques de transport urbain** : Réduire les émissions de NO₂ liées au trafic
3. **Prise en compte météorologique** : Intégrer la température dans les alertes pollution
4. **Surveillance ciblée** : Prioriser les zones proches des industries

---

## 👨‍💻 Auteur

Projet réalisé dans le cadre du cours 420-IAA-TT  
Institut Teccart - Automne 2025  
Professeur : Benfriha Hichem

---

## 📄 Licence

Ce projet est réalisé à des fins éducatives dans le cadre du programme d'Intelligence Artificielle de l'Institut Teccart.
