# Rapport Final : Analyse de la Qualité de l'Air et de la Pollution

---

**Cours**: 420-IAA-TT - Intelligence Artificielle 1  
**Institution**: Institut Teccart  
**Auteur**: Chekhmam Hanane  
**Date**: 10 Novembre 2025

---

## Table des Matières

1. [Introduction](#1-introduction)
2. [Méthodologie](#2-méthodologie)
3. [Analyse Exploratoire et Résultats](#3-analyse-exploratoire-et-résultats)
4. [Analyse des Facteurs d'Influence](#4-analyse-des-facteurs-dinfluence)
5. [Réponses aux Questions du Projet](#5-réponses-aux-questions-du-projet)
6. [Conclusions et Recommandations](#6-conclusions-et-recommandations)

---

## 1. Introduction

### 1.1 Contexte et Problématique

La pollution atmosphérique constitue l'un des défis environnementaux et de santé publique les plus pressants de notre époque. Au Canada, malgré des réglementations environnementales parmi les plus strictes au monde, certaines régions continuent de faire face à des épisodes de dégradation de la qualité de l'air, particulièrement dans les zones urbaines et industrielles.

Les particules fines (PM2.5 et PM10), les oxydes d'azote (NOx), le dioxyde de soufre (SO₂) et le monoxyde de carbone (CO) sont reconnus comme des polluants majeurs ayant des impacts significatifs sur la santé respiratoire et cardiovasculaire des populations exposées. Comprendre les facteurs qui contribuent à la variation de ces polluants est essentiel pour élaborer des stratégies de prévention efficaces.

### 1.2 Objectifs du Projet

Ce projet vise à réaliser une analyse approfondie des données sur la pollution atmosphérique au Canada afin de :

- **Identifier les principaux contributeurs** à la dégradation de la qualité de l'air
- **Quantifier les relations** entre facteurs environnementaux, démographiques et niveaux de pollution
- **Fournir des recommandations** exploitables pour les décideurs publics
- **Développer un outil interactif** de visualisation et d'exploration des données

### 1.3 Livrables du Projet

Les livrables de ce projet comprennent :

1. **Analyse de données complète** : Nettoyage, statistiques descriptives, étude des corrélations
2. **Application Streamlit interactive** : Plateforme de visualisation et d'exploration des données
3. **Dépôt GitHub** : Code source, documentation technique et guide d'utilisation
4. **Rapport final** : Synthèse des analyses, résultats et recommandations (présent document)

---

## 2. Méthodologie

### 2.1 Description des Données

Le jeu de données utilisé (`pollution.csv`) contient **5000 observations** et **10 variables** collectées sur le territoire canadien. Les variables incluent :

#### Variables de Pollution
- **PM2.5** : Concentration de particules fines (diamètre ≤ 2.5 μm) en μg/m³
- **PM10** : Concentration de particules grossières (diamètre ≤ 10 μm) en μg/m³
- **NO₂** : Concentration de dioxyde d'azote en ppb
- **SO₂** : Concentration de dioxyde de soufre en ppb
- **CO** : Concentration de monoxyde de carbone en ppm

#### Variables Environnementales
- **Temperature** : Température ambiante en °C
- **Humidity** : Humidité relative en %

#### Variables Démographiques et Géographiques
- **Population_Density** : Densité de population (habitants/km²)
- **Proximity_to_Industrial_Areas** : Distance aux zones industrielles en km

#### Variable Cible
- **Air_Quality** : Indice de qualité de l'air catégorisé
  - 0 : Bonne (air propre avec de faibles niveaux de pollution)
  - 1 : Modérée (qualité de l'air acceptable avec la présence de certains polluants)
  - 2 : Mauvaise (pollution notable pouvant causer des problèmes de santé pour les groupes sensibles)
  - 3 : Dangereuse (air fortement pollué posant de graves risques pour la santé de la population)

### 2.2 Pipeline d'Analyse

L'analyse a été structurée selon les étapes suivantes :

#### Étape 1 : Chargement et Exploration Initiale
- Importation des données avec la bibliothèque Pandas
- Vérification de la structure et des types de données
- Identification des dimensions du dataset (5000 échantillons × 10 variables)
- Évaluation préliminaire de la qualité des données

#### Étape 2 : Nettoyage des Données

**Traitement des Valeurs Manquantes**
- Détection des valeurs manquantes par variable
- Imputation par la **médiane** pour préserver la robustesse face aux outliers
- Justification : La médiane est moins sensible aux valeurs extrêmes que la moyenne

**Traitement des Valeurs Aberrantes (Outliers)**
- Identification des outliers par la méthode de l'Intervalle Interquartile (IQR)
- Seuils définis : [Q1 - 1.5×IQR, Q3 + 1.5×IQR]
- Application de la **winsorisation** : plafonnement aux limites IQR
- Avantage : Conservation de tous les échantillons tout en réduisant l'influence des valeurs extrêmes

#### Étape 3 : Analyse Statistique

Pour chaque variable, calcul de :
- **Mesures de tendance centrale** : Moyenne, médiane, mode
- **Mesures de dispersion** : Écart-type, variance, IQR
- **Mesures de position** : Quartiles (Q1, Q2, Q3), minimum, maximum

#### Étape 4 : Visualisation des Données

Création d'un ensemble complet de visualisations :
- Histogrammes de distribution
- Diagrammes en boîte (boxplots)
- Nuages de points (scatter plots)
- Heatmap de corrélation
- Graphiques de densité
- Pairplots

#### Étape 5 : Analyse des Corrélations

- Calcul de la matrice de corrélation de Pearson
- Identification des corrélations significatives (|r| > 0.3)
- Analyse approfondie des relations avec la variable cible `Air_Quality`
- Interprétation des coefficients et de leur significativité

### 2.3 Outils et Technologies

- **Langage** : Python 3.11
- **Bibliothèques d'analyse** : Pandas, NumPy, SciPy
- **Bibliothèques de visualisation** : Matplotlib, Seaborn
- **Framework web** : Streamlit
- **Contrôle de version** : Git/GitHub

---

## 3. Analyse Exploratoire et Résultats

### 3.1 Distribution de la Qualité de l'Air

La variable cible `Air_Quality` présente une distribution déséquilibrée mais représentative de la réalité canadienne, où la qualité de l'air est généralement bonne à modérée.

#### Répartition des Catégories

| Catégorie | Label | Nombre d'Échantillons | Pourcentage |
|-----------|-------|----------------------|-------------|
| 0 | Bonne | 1,988 | 39.8% |
| 1 | Modérée | 1,511 | 30.2% |
| 2 | Mauvaise | 1,001 | 20.0% |
| 3 | Dangereuse | 500 | 10.0% |

**Observations clés :**
- Près de **70% des observations** correspondent à une qualité d'air bonne ou modérée
- Les épisodes de qualité dangereuse restent **minoritaires (10%)** mais non négligeables
- Cette distribution reflète la réalité terrain : la plupart du temps, l'air est respirable, mais des pics de pollution surviennent

![Distribution de la Qualité de l'Air](images/01_distribution_air_quality.png)

*Figure 1 : Distribution des niveaux de qualité de l'air dans le jeu de données. Les couleurs représentent les différents niveaux : Vert (Bonne), Jaune (Modérée), Orange (Mauvaise), Rouge (Dangereuse).*

### 3.2 Analyse des Polluants Principaux (PM2.5 et PM10)

#### 3.2.1 Particules Fines (PM2.5)

Les PM2.5 sont particulièrement préoccupantes car elles peuvent pénétrer profondément dans les poumons et même entrer dans la circulation sanguine.

**Statistiques descriptives :**
- **Moyenne** : 18.023 μg/m³
- **Médiane** : 12.000 μg/m³
- **Écart-type** : 17.230 μg/m³
- **Minimum** : 0.000 μg/m³
- **Maximum** : 58.412 μg/m³

**Interprétation :**
La moyenne supérieure à la médiane suggère que des épisodes ponctuels de pollution forte tirent la distribution vers le haut. Ces pics nécessitent une attention particulière pour la santé publique.

#### 3.2.2 Particules Grossières (PM10)

Les PM10 incluent les PM2.5 et des particules plus grosses, souvent issues de sources mécaniques (usure des routes, construction, poussières).

**Statistiques descriptives :**
- **Moyenne** : 28.221 μg/m³
- **Médiane** : 21.700 μg/m³
- **Écart-type** : 20.616 μg/m³
- **Minimum** : -0.200 μg/m³ (valeur aberrante corrigée)
- **Maximum** : 76.800 μg/m³

![Distribution de PM2.5 et PM10](images/03_histogrammes_pm25_pm10.png)

*Figure 2 : Histogrammes détaillés des concentrations de PM2.5 et PM10. Les lignes verticales indiquent la moyenne (rouge), la médiane (verte) et ±1 écart-type (orange).*

### 3.3 Visualisations des Distributions

![Histogrammes de toutes les variables](images/02_histogrammes_variables.png)

*Figure 3 : Histogrammes de distribution pour toutes les variables environnementales. Chaque graphique montre la fréquence des valeurs avec les statistiques de tendance centrale.*

### 3.4 Analyse des Valeurs Aberrantes

Les boxplots permettent d'identifier visuellement les valeurs aberrantes et la dispersion des données.

![Boxplots de toutes les variables](images/04_boxplots_variables.png)

*Figure 4 : Boîtes à moustaches pour toutes les variables. Les points rouges représentent les valeurs aberrantes détectées par la méthode IQR.*

![Boxplots détaillés PM2.5 et PM10](images/05_boxplots_pm25_pm10.png)

*Figure 5 : Comparaison détaillée des distributions de PM2.5 et PM10 avec statistiques de quartiles.*

### 3.5 Graphes de Densité

Les graphes de densité révèlent la forme de la distribution de probabilité de chaque variable.

![Graphes de densité](images/06_graphes_densite.png)

*Figure 6 : Courbes de densité pour les principales variables environnementales. Les pics indiquent les valeurs les plus fréquentes.*

---

## 4. Analyse des Facteurs d'Influence

### 4.1 Matrice de Corrélation Globale

La matrice de corrélation de Pearson révèle les relations linéaires entre toutes les variables du dataset.

![Heatmap de la Matrice de Corrélation](images/07_heatmap_correlation.png)

*Figure 7 : Heatmap de la matrice de corrélation. Les couleurs vertes indiquent des corrélations positives, les rouges des corrélations négatives, et les jaunes une absence de corrélation.*

**Légende :**
- **Corrélations positives** (couleurs vertes) : Les variables augmentent ensemble
- **Corrélations négatives** (couleurs rouges) : Une variable augmente quand l'autre diminue
- **Absence de corrélation** (couleurs neutres) : Pas de relation linéaire significative

### 4.2 Facteurs Influençant la Qualité de l'Air

L'analyse des corrélations avec `Air_Quality` (où un score plus élevé indique une qualité d'air dégradée) a permis d'identifier les facteurs les plus déterminants.

![Corrélations avec la Qualité de l'Air](images/10_correlations_air_quality.png)

*Figure 8 : Coefficients de corrélation de Pearson entre chaque variable et la qualité de l'air. Les barres vertes indiquent des corrélations positives, les rouges des corrélations négatives.*

#### 4.2.1 Top 3 des Contributeurs à la Pollution

**1. Température (r = 0.743) - Corrélation Positive Forte**

La température montre la corrélation la plus forte avec la dégradation de la qualité de l'air.

**Mécanismes explicatifs :**
- **Formation d'ozone troposphérique** : Les températures élevées accélèrent les réactions photochimiques qui produisent l'ozone, un polluant secondaire
- **Augmentation de la volatilisation** : Les composés organiques volatils (COV) s'évaporent plus facilement par temps chaud
- **Inversions thermiques** : Par temps chaud et stable, les polluants restent piégés près du sol
- **Augmentation de la consommation énergétique** : Climatisation massive entraînant plus d'émissions

**Implications :**
Les vagues de chaleur représentent un facteur de risque majeur pour la qualité de l'air. Les systèmes d'alerte devraient intégrer les prévisions de température pour anticiper les épisodes de pollution.

**2. Dioxyde de Soufre (SO₂) (r = 0.679) - Corrélation Positive Modérée**

Le SO₂ est un indicateur direct de la pollution industrielle et de la combustion de combustibles fossiles.

**Sources principales :**
- Industries métallurgiques et pétrochimiques
- Centrales thermiques au charbon
- Raffinage du pétrole
- Transport maritime (fuel lourd)

**Impact sanitaire :**
- Irritation des voies respiratoires
- Aggravation de l'asthme et des bronchites chroniques
- Contribution aux pluies acides

**3. Dioxyde d'Azote (NO₂) (r = 0.651) - Corrélation Positive Modérée**

Le NO₂ est principalement lié au trafic routier et aux activités industrielles.

**Sources principales :**
- Combustion dans les moteurs à essence et diesel
- Centrales thermiques
- Industries de transformation

**Impact sanitaire :**
- Inflammation des voies respiratoires
- Réduction de la fonction pulmonaire
- Augmentation de la sensibilité aux infections respiratoires

![Top 3 des corrélations](images/11_scatter_top3_correlations.png)

*Figure 9 : Diagrammes de dispersion pour les trois variables les plus corrélées avec la qualité de l'air. Les lignes rouges en pointillés représentent les tendances linéaires.*

### 4.3 Matrice de Dispersion Complète

![Matrice de dispersion](images/08_scatter_matrix.png)

*Figure 10 : Matrice de dispersion (scatter matrix) montrant les relations entre toutes les paires de variables. Les couleurs représentent les niveaux de qualité de l'air.*

### 4.4 Pairplot avec Distinction par Qualité de l'Air

![Pairplot complet](images/09_pairplot_complet.png)

*Figure 11 : Pairplot coloré selon les niveaux de qualité de l'air. Cette visualisation permet d'identifier les patterns de séparation entre les différentes classes.*

---

## 5. Réponses aux Questions du Projet

### Question 1 : Quels sont les types de données présents dans le jeu de données ?

**Réponse :** Toutes les variables du jeu de données sont de type **quantitatif continu** (numériques). Plus précisément :

- **Variables float64** : Temperature, Humidity, PM2.5, PM10, NO2, SO2, CO, Proximity_to_Industrial_Areas, Population_Density
- **Variable int64** : Air_Quality (bien que catégorielle, elle est encodée numériquement)

Aucune variable qualitative (catégorielle textuelle) n'est présente dans le dataset. Toutes les variables permettent des calculs statistiques et des analyses de corrélation.

### Question 2 : Combien d'échantillons et de colonnes contient le jeu de données ?

**Réponse :**

- **Nombre d'échantillons (lignes)** : 5,000
- **Nombre de colonnes** : 10
  - 9 variables prédictives (features)
  - 1 variable cible (target)

**Dimensions totales** : 5,000 échantillons × 10 colonnes = 50,000 points de données

### Question 3 : Y a-t-il des valeurs manquantes dans le jeu de données ? Si oui, dans quelles colonnes ?

**Réponse :**

Dans le jeu de données **brut** (`pollution.csv`), quelques valeurs manquantes ont été détectées, notamment dans la colonne **PM10** (ligne 41).

Dans le jeu de données **nettoyé** (`pollution_clean.csv`), **aucune valeur manquante** n'est présente. Toutes les valeurs manquantes ont été traitées lors de l'étape de nettoyage.

### Question 4 : Appliquer sur le jeu de données une technique pour remplacer les valeurs manquantes

**Réponse :**

La technique d'**imputation par la médiane** a été appliquée pour remplacer les valeurs manquantes.

**Justification du choix :**

1. **Robustesse aux outliers** : La médiane n'est pas affectée par les valeurs extrêmes, contrairement à la moyenne
2. **Préservation de la distribution** : La médiane représente la valeur centrale de la distribution
3. **Approprié pour les données environnementales** : Les données de pollution contiennent souvent des valeurs aberrantes dues à des événements ponctuels

**Processus appliqué :**
```python
for col in data.columns:
    if data[col].isnull().sum() > 0:
        mediane = data[col].median()
        data[col].fillna(mediane, inplace=True)
```

### Question 5 : Quels sont les facteurs environnementaux les plus corrélés avec la qualité de l'air ?

**Réponse :**

Les facteurs environnementaux classés par ordre de corrélation avec `Air_Quality` :

| Rang | Variable | Corrélation (r) | Force | Direction |
|------|----------|----------------|-------|-----------|
| 1 | Temperature | 0.743 | Forte | Positive |
| 2 | SO₂ | 0.679 | Modérée | Positive |
| 3 | NO₂ | 0.651 | Modérée | Positive |
| 4 | Humidity | 0.624 | Modérée | Positive |
| 5 | PM10 | 0.599 | Modérée | Positive |
| 6 | CO | 0.577 | Modérée | Positive |
| 7 | PM2.5 | 0.430 | Modérée | Positive |
| 8 | Population_Density | 0.030 | Très faible | Positive |
| 9 | Proximity_to_Industrial_Areas | -0.378 | Faible | Négative |

**Interprétation :**
- Les facteurs météorologiques (température, humidité) et les polluants gazeux (SO₂, NO₂) sont les plus fortement corrélés
- La proximité aux zones industrielles montre une corrélation négative : plus on s'éloigne des industries, meilleure est la qualité de l'air
- La densité de population a une corrélation très faible, suggérant que d'autres facteurs sont plus déterminants

### Question 6 : Quels sont les trois principaux contributeurs aux niveaux de pollution dans le dataset ?

**Réponse :**

Les **trois principaux contributeurs** à la dégradation de la qualité de l'air sont :

1. **Température (Temperature)** : r = 0.743
   - Corrélation positive forte
   - Facteur le plus influent
   - Explique environ 55% de la variance de la qualité de l'air (r²)

2. **Dioxyde de Soufre (SO₂)** : r = 0.679
   - Corrélation positive modérée
   - Indicateur de pollution industrielle
   - Explique environ 46% de la variance

3. **Dioxyde d'Azote (NO₂)** : r = 0.651
   - Corrélation positive modérée
   - Lié au trafic routier et aux industries
   - Explique environ 42% de la variance

Ces trois facteurs sont les plus déterminants pour prédire et comprendre les variations de la qualité de l'air.

### Question 7 : Existe-t-il des valeurs aberrantes dans les concentrations de PM2.5 ou PM10 ?

**Réponse :**

**Oui**, des valeurs aberrantes ont été détectées dans les concentrations de PM2.5 et PM10 en utilisant la méthode de l'Intervalle Interquartile (IQR).

**Pour PM2.5 :**
- Q1 = 4.60 μg/m³
- Q3 = 26.13 μg/m³
- IQR = 21.53 μg/m³
- Limites : [-27.69, 58.42] μg/m³
- **Outliers détectés** : Plusieurs valeurs au-delà de la limite supérieure

**Pour PM10 :**
- Q1 = 12.30 μg/m³
- Q3 = 38.10 μg/m³
- IQR = 25.80 μg/m³
- Limites : [-26.40, 77.00] μg/m³
- **Outliers détectés** : Plusieurs valeurs au-delà de la limite supérieure, et une valeur négative (-0.2) corrigée

**Traitement appliqué :**
Les outliers ont été traités par **winsorisation** (plafonnement aux limites IQR) pour réduire leur influence sans les supprimer, préservant ainsi la taille du dataset.

### Question 8 : Quelle est la moyenne, la médiane et l'écart-type des concentrations de PM2.5 et PM10 ?

**Réponse :**

**PM2.5 (Particules Fines) :**
- **Moyenne** : 18.023 μg/m³
- **Médiane** : 12.000 μg/m³
- **Écart-type** : 17.230 μg/m³

**PM10 (Particules Grossières) :**
- **Moyenne** : 28.221 μg/m³
- **Médiane** : 21.700 μg/m³
- **Écart-type** : 20.616 μg/m³

**Observations :**
- Pour les deux polluants, la **moyenne > médiane**, indiquant une asymétrie droite (présence de valeurs élevées)
- L'**écart-type élevé** révèle une grande variabilité des concentrations
- Les **PM10 sont systématiquement plus élevées** que les PM2.5, ce qui est logique car les PM10 incluent les PM2.5

### Question 9 : Quelle est la corrélation entre l'humidité et la qualité de l'air ?

**Réponse :**

**Coefficient de corrélation de Pearson** : r = 0.624

**Interprétation :**
- **Force** : Corrélation modérée
- **Direction** : Positive
- **Signification** : L'augmentation de l'humidité est associée à une dégradation de la qualité de l'air

**Explication physique :**
L'humidité élevée peut favoriser :
- La formation de particules secondaires par condensation
- Le piégeage des polluants dans l'atmosphère
- La formation de brouillard qui concentre les polluants
- Les réactions chimiques produisant des aérosols

**Variance expliquée** : r² = 0.389, soit environ 39% de la variance de la qualité de l'air peut être expliquée par l'humidité.

### Question 10 : Quel est le lien entre la densité de population et les niveaux de PM2.5 ?

**Réponse :**

**Coefficient de corrélation de Pearson** : r = 0.009

**Interprétation :**
- **Force** : Corrélation très faible, quasi nulle
- **Direction** : Légèrement positive mais non significative
- **Signification** : Il n'existe **pas de relation linéaire significative** entre la densité de population et les niveaux de PM2.5

**Explication :**
Ce résultat contre-intuitif suggère que :
- La densité de population **seule** n'est pas un bon prédicteur des niveaux de PM2.5
- D'autres facteurs sont plus déterminants : proximité industrielle, trafic routier, conditions météorologiques
- Certaines zones rurales peuvent avoir des niveaux élevés de PM2.5 (agriculture, feux de forêt)
- Certaines zones urbaines bien réglementées peuvent avoir des niveaux faibles

**Conclusion :** La qualité de l'air dépend davantage des **sources d'émission** et des **conditions météorologiques** que de la simple densité de population.

### Question 11 : Quels sont les quartiles des concentrations de monoxyde de carbone (CO) ?

**Réponse :**

**Quartiles du CO (en ppm) :**

- **Q1 (25e percentile)** : 1.030 ppm
  - 25% des observations ont une concentration de CO inférieure à 1.030 ppm

- **Q2 (50e percentile - Médiane)** : 1.410 ppm
  - Valeur centrale de la distribution
  - 50% des observations sont en dessous de cette valeur

- **Q3 (75e percentile)** : 1.840 ppm
  - 75% des observations ont une concentration de CO inférieure à 1.840 ppm

- **Intervalle Interquartile (IQR)** : Q3 - Q1 = 0.810 ppm
  - Mesure de dispersion robuste
  - Contient les 50% centraux des données

**Interprétation :**
- Les niveaux de CO restent **généralement modérés** dans le dataset
- La distribution est relativement **symétrique** (Q2 proche du milieu de Q1 et Q3)
- Les valeurs extrêmes (au-delà de Q3 + 1.5×IQR) sont rares

---

## 6. Conclusions et Recommandations

### 6.1 Synthèse des Résultats

Cette analyse approfondie des données de pollution atmosphérique au Canada a permis de mettre en lumière plusieurs constats majeurs :

1. **Facteurs météorologiques dominants** : La température et l'humidité sont les facteurs les plus fortement corrélés avec la qualité de l'air, soulignant l'importance des conditions météorologiques dans la dispersion et la formation des polluants.

2. **Polluants industriels critiques** : Le SO₂ et le NO₂ sont des contributeurs majeurs à la pollution, reflétant l'impact des activités industrielles et du trafic routier.

3. **Variabilité importante** : Les niveaux de pollution présentent une grande variabilité, avec des épisodes ponctuels de pollution forte nécessitant une surveillance accrue.

4. **Distribution déséquilibrée** : Bien que la qualité de l'air soit généralement bonne ou modérée (70% des cas), les épisodes de pollution dangereuse (10%) représentent un risque sanitaire significatif.

### 6.2 Recommandations pour la Gestion de la Pollution

#### 6.2.1 Recommandations Immédiates

**1. Système d'Alerte Intégré**
- Développer un système d'alerte à la population intégrant les prévisions météorologiques (température, humidité)
- Anticiper les épisodes de pollution lors des vagues de chaleur
- Diffuser des recommandations sanitaires ciblées pour les populations vulnérables

**2. Surveillance Renforcée**
- Intensifier la surveillance des zones industrielles (forte corrélation avec SO₂)
- Installer des stations de mesure supplémentaires dans les zones à risque
- Développer un réseau de capteurs en temps réel

**3. Mesures d'Urgence**
- Mettre en place des protocoles d'intervention lors des pics de pollution
- Réduire temporairement les activités industrielles polluantes
- Limiter la circulation automobile en zones urbaines

#### 6.2.2 Recommandations Stratégiques

**1. Réglementation des Émissions Industrielles**
- Renforcer les normes d'émission pour le SO₂ et le NO₂
- Imposer des technologies de réduction des émissions
- Sanctionner les dépassements de seuils
- Encourager la transition vers des énergies propres

**2. Politiques de Transport Urbain**
- Promouvoir les transports en commun électriques
- Développer les infrastructures cyclables
- Créer des zones à faibles émissions (ZFE) dans les centres urbains
- Encourager le covoiturage et le télétravail

**3. Aménagement du Territoire**
- Éloigner les zones résidentielles des zones industrielles
- Créer des zones tampons végétalisées
- Intégrer la qualité de l'air dans les plans d'urbanisme
- Favoriser la végétalisation urbaine (absorption des polluants)

**4. Recherche et Innovation**
- Développer des modèles prédictifs de la qualité de l'air
- Investir dans les technologies de capture et de filtration
- Étudier les interactions complexes entre polluants et météorologie
- Évaluer l'efficacité des mesures mises en place

#### 6.2.3 Recommandations pour la Santé Publique

**1. Sensibilisation et Éducation**
- Informer la population sur les risques sanitaires de la pollution
- Former les professionnels de santé à la détection des pathologies liées
- Éduquer les enfants dès l'école primaire

**2. Protection des Populations Vulnérables**
- Identifier et suivre les personnes à risque (asthmatiques, personnes âgées, enfants)
- Fournir des équipements de protection (masques, purificateurs d'air)
- Adapter les activités scolaires et sportives lors des pics de pollution

**3. Surveillance Sanitaire**
- Suivre l'évolution des pathologies respiratoires et cardiovasculaires
- Établir des liens épidémiologiques entre pollution et santé
- Évaluer les coûts sanitaires de la pollution

### 6.3 Perspectives Futures

Ce projet a démontré la puissance de l'analyse de données et de la visualisation pour extraire des informations pertinentes à partir de données environnementales complexes. Les perspectives d'amélioration incluent :

1. **Intégration de données temporelles** : Analyser l'évolution de la pollution au fil du temps (tendances saisonnières, annuelles)

2. **Modélisation prédictive** : Développer des modèles de machine learning pour prédire la qualité de l'air future

3. **Analyse géospatiale** : Cartographier la pollution pour identifier les zones critiques

4. **Intégration de données supplémentaires** : Inclure des données sur le trafic routier, les activités industrielles, les feux de forêt

5. **Analyse coûts-bénéfices** : Évaluer l'impact économique des mesures de réduction de la pollution

### 6.4 Conclusion Générale

La qualité de l'air au Canada est influencée par un ensemble complexe de facteurs environnementaux, météorologiques et anthropiques. Cette analyse a permis d'identifier les contributeurs majeurs et de quantifier leurs relations avec la pollution atmosphérique.

Les résultats obtenus fournissent une base scientifique solide pour guider les décisions en matière de santé publique et de politique environnementale. La mise en œuvre des recommandations formulées permettrait de réduire significativement les épisodes de pollution et d'améliorer la qualité de vie des populations.

L'application Streamlit développée dans le cadre de ce projet constitue un outil précieux pour explorer les données de manière interactive et pour communiquer les résultats aux décideurs et au grand public.

---

## Annexes

### Annexe A : Statistiques Descriptives Complètes

| Variable | Moyenne | Médiane | Écart-type | Min | Max | Q1 | Q3 |
|----------|---------|---------|------------|-----|-----|----|----|
| Temperature | 30.041 | 29.000 | 6.799 | -17.892 | 69.084 | 25.100 | 34.000 |
| Humidity | 70.078 | 69.800 | 15.882 | 36.000 | 128.100 | 58.300 | 80.300 |
| PM2.5 | 18.023 | 12.000 | 17.230 | 0.000 | 58.412 | 4.600 | 26.125 |
| PM10 | 28.221 | 21.700 | 20.616 | -0.200 | 76.800 | 12.300 | 38.100 |
| NO2 | 26.491 | 25.300 | 10.725 | 7.400 | 450.520 | 20.100 | 31.900 |
| SO2 | 10.054 | 8.000 | 7.295 | -6.200 | 205.747 | 5.100 | 13.725 |
| CO | 1.510 | 1.410 | 0.863 | 0.650 | 48.723 | 1.030 | 1.840 |
| Proximity_to_Industrial_Areas | 8.568 | 7.900 | 6.901 | 0.000 | 290.849 | 5.400 | 11.100 |
| Population_Density | 541.503 | 494.000 | 1843.873 | 188.000 | 95661.634 | 381.000 | 601.000 |

### Annexe B : Matrice de Corrélation Numérique

|  | Temperature | Humidity | PM2.5 | PM10 | NO2 | SO2 | CO | Proximity | Population | Air_Quality |
|--|-------------|----------|-------|------|-----|-----|----|-----------|-----------| ------------|
| Temperature | 1.000 | 0.458 | 0.326 | 0.448 | 0.478 | 0.517 | 0.428 | -0.294 | 0.015 | 0.743 |
| Humidity | 0.458 | 1.000 | 0.270 | 0.377 | 0.412 | 0.419 | 0.366 | -0.232 | 0.039 | 0.624 |
| PM2.5 | 0.326 | 0.270 | 1.000 | 0.950 | 0.271 | 0.287 | 0.255 | -0.190 | 0.009 | 0.430 |
| PM10 | 0.448 | 0.377 | 0.950 | 1.000 | 0.378 | 0.403 | 0.354 | -0.258 | 0.013 | 0.599 |
| NO2 | 0.478 | 0.412 | 0.271 | 0.378 | 1.000 | 0.434 | 0.365 | -0.251 | 0.029 | 0.651 |
| SO2 | 0.517 | 0.419 | 0.287 | 0.403 | 0.434 | 1.000 | 0.392 | -0.253 | 0.023 | 0.679 |
| CO | 0.428 | 0.366 | 0.255 | 0.354 | 0.365 | 0.392 | 1.000 | -0.220 | 0.015 | 0.577 |
| Proximity | -0.294 | -0.232 | -0.190 | -0.258 | -0.251 | -0.253 | -0.220 | 1.000 | -0.010 | -0.378 |
| Population | 0.015 | 0.039 | 0.009 | 0.013 | 0.029 | 0.023 | 0.015 | -0.010 | 1.000 | 0.030 |
| Air_Quality | 0.743 | 0.624 | 0.430 | 0.599 | 0.651 | 0.679 | 0.577 | -0.378 | 0.030 | 1.000 |


