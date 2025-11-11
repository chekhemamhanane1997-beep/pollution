

## 1. Introduction

Ce rapport présente les résultats d'une analyse approfondie des données sur la pollution atmosphérique au Canada. L'objectif principal de ce projet est de comprendre les relations complexes entre divers facteurs environnementaux, démographiques et les niveaux de qualité de l'air. Pour ce faire, une analyse statistique complète a été menée, et les résultats ont été intégrés dans une application web interactive développée avec Streamlit.

La pollution de l'air constitue un enjeu de santé publique majeur. Ce projet vise à identifier les principaux contributeurs à la dégradation de la qualité de l'air et à fournir des informations exploitables pour d'éventuelles stratégies de prévention et de gestion.

Les livrables de ce projet incluent :
- Une **analyse de données complète** incluant le nettoyage, les statistiques descriptives et l'étude des corrélations.
- Une **application Streamlit interactive** pour la visualisation et l'exploration des données.
- Un **dépôt GitHub** contenant le code source et la documentation.
- Le présent **rapport final** qui synthétise les analyses, les résultats et les recommandations.

## 2. Méthodologie

L'analyse a été structurée en plusieurs étapes clés pour garantir la robustesse et la fiabilité des résultats.

1.  **Chargement et Exploration des Données** : Le jeu de données initial (`pollution.csv`) a été chargé en utilisant la bibliothèque Pandas. Une première exploration a permis d'identifier la structure, les types de données et les dimensions du jeu de données (5000 échantillons, 10 variables).

2.  **Nettoyage des Données** : Cette étape cruciale a consisté à traiter les anomalies pour assurer la qualité des données.
    *   **Valeurs Manquantes** : Les quelques valeurs manquantes détectées ont été remplacées par la **médiane** de leur colonne respective. Cette méthode a été choisie pour sa robustesse face aux valeurs aberrantes.
    *   **Valeurs Aberrantes (Outliers)** : Les outliers, notamment dans les concentrations de PM2.5 et PM10, ont été identifiés à l'aide de la méthode de l'intervalle interquartile (IQR). Ils ont ensuite été traités par **winsorisation**, c'est-à-dire qu'ils ont été plafonnés aux limites supérieure et inférieure (Q1 - 1.5*IQR et Q3 + 1.5*IQR) pour réduire leur influence sans les supprimer.

3.  **Analyse Statistique et Visualisation** : Des statistiques descriptives (moyenne, médiane, écart-type, quartiles) ont été calculées pour toutes les variables. Parallèlement, une série de visualisations a été générée pour illustrer les distributions, les dispersions et les relations entre les variables.

4.  **Analyse des Corrélations** : La matrice de corrélation de Pearson a été calculée pour quantifier les relations linéaires entre toutes les paires de variables. Une attention particulière a été portée aux corrélations avec la variable cible, `Air_Quality`.

## 3. Analyse Exploratoire et Résultats

### 3.1. Distribution de la Qualité de l'Air

La variable cible, `Air_Quality`, est répartie en quatre catégories. La distribution des échantillons dans ces catégories est présentée ci-dessous. On observe que les classes ne sont pas parfaitement équilibrées, avec une prédominance des niveaux "Bonne" (0) et "Modérée" (1).

![Distribution de la Qualité de l'Air](images/01_distribution_air_quality.png)

| Catégorie | Label | Nombre d'Échantillons | Pourcentage |
| :--- | :--- | :--- | :--- |
| 0 | Bonne | 1,988 | 39.8% |
| 1 | Modérée | 1,511 | 30.2% |
| 2 | Mauvaise | 1,001 | 20.0% |
| 3 | Dangereuse | 500 | 10.0% |

### 3.2. Analyse des Polluants Principaux (PM2.5 et PM10)

Les particules fines (PM2.5) et grossières (PM10) sont des indicateurs clés de la pollution. Leur analyse statistique révèle les informations suivantes :

- **Moyenne et Médiane** : Pour les deux polluants, la moyenne est légèrement supérieure à la médiane, ce qui suggère une légère asymétrie droite dans leur distribution, causée par des valeurs de pollution plus élevées.
- **Dispersion** : L'écart-type et l'intervalle interquartile montrent une dispersion considérable, indiquant une grande variabilité des niveaux de pollution dans le jeu de données.

![Distribution de PM2.5 et PM10](images/03_histogrammes_pm25_pm10.png)

## 4. Analyse des Facteurs d'Influence

L'étude des corrélations a permis de répondre aux questions clés du projet et d'identifier les facteurs ayant le plus d'impact sur la qualité de l'air.

### 4.1. Matrice de Corrélation

La heatmap ci-dessous visualise la matrice de corrélation de Pearson. Les couleurs chaudes (vertes) indiquent une corrélation positive (les variables évoluent dans le même sens), tandis que les couleurs froides (rouges) indiquent une corrélation négative.

![Heatmap de la Matrice de Corrélation](images/07_heatmap_correlation.png)

### 4.2. Principaux Facteurs Corrélés avec la Qualité de l'Air

L'analyse des corrélations avec la variable `Air_Quality` (où un score plus élevé signifie une moins bonne qualité de l'air) a révélé les facteurs les plus influents.

![Corrélations avec la Qualité de l'Air](images/10_correlations_air_quality.png)

Les **trois principaux contributeurs** à la dégradation de la qualité de l'air sont :

1.  **Température (`Temperature`)** : Corrélation positive forte (r = 0.743). Une augmentation de la température est fortement associée à une mauvaise qualité de l'air. Cela peut être dû à des réactions chimiques favorisées par la chaleur qui produisent des polluants secondaires comme l'ozone.
2.  **Dioxyde de Soufre (`SO2`)** : Corrélation positive modérée (r = 0.679). Ce polluant, souvent émis par les industries et la combustion de fossiles, est un indicateur direct de la pollution.
3.  **Dioxyde d'Azote (`NO2`)** : Corrélation positive modérée (r = 0.651). Principalement issu du trafic routier et de certaines industries, le NO₂ est également un facteur aggravant.

![Top 3 des corrélations](images/11_scatter_top3_correlations.png)

### 4.3. Réponses aux Questions d'Analyse

- **Corrélation Humidité / Qualité de l'Air** : Il existe une corrélation **positive modérée (r = 0.624)**. Une humidité plus élevée est associée à une moins bonne qualité de l'air, potentiellement car elle peut piéger les polluants dans l'atmosphère.

- **Lien Densité de Population / PM2.5** : La corrélation est **positive mais très faible (r = 0.009)**. Cela suggère que la densité de population seule n'est pas un bon prédicteur des niveaux de PM2.5. D'autres facteurs, comme la présence d'industries ou les axes routiers, sont probablement plus déterminants.

- **Quartiles du Monoxyde de Carbone (CO)** : 
    - Q1 (25%) : 1.03 ppm
    - Q2 (Médiane) : 1.41 ppm
    - Q3 (75%) : 1.84 ppm

## 5. Conclusions et Recommandations

Cette analyse a permis de mettre en lumière les principaux facteurs influençant la qualité de l'air dans le jeu de données étudié. Les polluants industriels et liés au trafic (`SO2`, `NO2`, `CO`), ainsi que les conditions météorologiques (`Temperature`, `Humidity`), sont les moteurs les plus significatifs de la pollution.

Sur la base de ces résultats, les recommandations suivantes peuvent être formulées :

1.  **Réglementation des Émissions Industrielles** : Étant donné la forte corrélation des polluants comme le SO₂ et le NO₂ avec la mauvaise qualité de l'air, renforcer les normes d'émission pour les zones industrielles est une priorité. La variable `Proximity_to_Industrial_Areas` montre une corrélation négative (-0.378), confirmant que plus on s'éloigne des industries, meilleure est la qualité de l'air.

2.  **Politiques de Transport Urbain** : Le NO₂, fortement lié au trafic, étant un contributeur majeur, des politiques visant à réduire les émissions des véhicules (promotion des transports en commun, véhicules électriques, zones à faibles émissions) sont recommandées.

3.  **Prise en Compte des Facteurs Météorologiques** : La forte corrélation avec la température suggère que les vagues de chaleur peuvent exacerber les épisodes de pollution. Les systèmes d'alerte à la population devraient intégrer les prévisions météorologiques pour anticiper les pics de pollution.

4.  **Surveillance Ciblée** : Plutôt que de se concentrer uniquement sur la densité de population, les efforts de surveillance devraient cibler les zones situées à proximité des sources d'émission connues (industries, grands axes routiers), car ce sont des facteurs plus directement corrélés à la pollution.

Ce projet démontre la puissance de l'analyse de données et de la visualisation pour extraire des informations pertinentes à partir de données environnementales complexes et pour guider la prise de décision en matière de santé publique.
