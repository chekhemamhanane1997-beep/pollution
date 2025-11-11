"""
Projet 1 - Application Streamlit pour l'Analyse de la Qualité de l'Air
420-IAA-TT - Intelligence Artificielle 1
Institut Teccart - Automne 2025
Par: Benfriha Hichem

Application interactive pour explorer et analyser les données de pollution atmosphérique.
"""

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
import os

# Configuration de la page
st.set_page_config(
    page_title="Analyse Qualité de l'Air",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration des graphiques
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Chargement des données
@st.cache_data
def charger_donnees():
    """Charge les données nettoyées"""
    try:
        data = pd.read_csv('pollution_clean.csv')
        return data
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        return None

# Fonction pour afficher les statistiques
def afficher_statistiques(data, colonne):
    """Affiche les statistiques descriptives pour une colonne"""
    stats = {
        'Moyenne': data[colonne].mean(),
        'Médiane': data[colonne].median(),
        'Écart-type': data[colonne].std(),
        'Variance': data[colonne].var(),
        'Minimum': data[colonne].min(),
        'Maximum': data[colonne].max(),
        'Q1 (25%)': data[colonne].quantile(0.25),
        'Q3 (75%)': data[colonne].quantile(0.75),
        'IQR': data[colonne].quantile(0.75) - data[colonne].quantile(0.25)
    }
    return pd.DataFrame(stats, index=[0]).T

# Chargement des données
data = charger_donnees()

if data is not None:
    # Sidebar - Navigation
    st.sidebar.title('🌍 Navigation')
    st.sidebar.markdown('---')
    
    menu = st.sidebar.selectbox(
        'Choisir une section',
        ['🏠 Accueil', 
         '🔍 Exploration des Données', 
         '📊 Visualisations', 
         '🔗 Étude de Corrélation',
         '📈 Analyse Approfondie']
    )
    
    st.sidebar.markdown('---')
    st.sidebar.info("""
    **Projet 1 - 420-IAA-TT**  
    Intelligence Artificielle 1  
    Institut Teccart  
    Automne 2025
    """)
    
    # ============================================================
    # SECTION 1: ACCUEIL
    # ============================================================
    if menu == '🏠 Accueil':
        st.markdown("""
        <div style='text-align:center; padding: 20px;'>
            <h1 style='color:#2E86AB; font-size:48px;'>🌍 Analyse de la Qualité de l'Air et de la Pollution</h1>
            <h3 style='color:#555;'>Étude des Facteurs Environnementaux au Canada</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Introduction
        st.header("📋 Introduction")
        st.write("""
        Cette application interactive présente une analyse complète des données de qualité de l'air au Canada. 
        En tant que Data Scientist environnemental, nous analysons comment différents facteurs environnementaux 
        et démographiques influencent les niveaux de pollution atmosphérique.
        
        La pollution atmosphérique est un enjeu de santé publique majeur, influencée par plusieurs facteurs 
        tels que la concentration de polluants chimiques (PM2.5, PM10, NO₂, SO₂, CO), les conditions 
        météorologiques (température, humidité), la densité de population et la proximité des zones industrielles.
        """)
        
        # Objectifs
        st.header("🎯 Objectifs du Projet")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            - ✅ Explorer et comprendre la structure des données
            - ✅ Identifier les relations entre facteurs environnementaux
            - ✅ Déterminer les variables corrélées avec la pollution
            """)
        
        with col2:
            st.markdown("""
            - ✅ Créer des visualisations dynamiques et interactives
            - ✅ Analyser les statistiques descriptives
            - ✅ Formuler des recommandations pour la gestion de la pollution
            """)
        
        st.markdown("---")
        
        # Aperçu des données
        st.header("📊 Aperçu des Données")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Échantillons", f"{len(data):,}")
        with col2:
            st.metric("Variables", len(data.columns))
        with col3:
            st.metric("Variables Prédictives", len(data.columns) - 1)
        with col4:
            st.metric("Variable Cible", "Air_Quality")
        
        st.subheader("🔍 Données Brutes (10 premières lignes)")
        st.dataframe(data.head(10), use_container_width=True)
        
        # Description des variables
        st.markdown("---")
        st.header("📖 Description des Variables")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Variables Environnementales")
            st.markdown("""
            - **Temperature (°C)**: Température moyenne de la région
            - **Humidity (%)**: Humidité relative enregistrée
            - **PM2.5 (µg/m³)**: Particules fines en suspension
            - **PM10 (µg/m³)**: Particules grossières en suspension
            - **NO₂ (ppb)**: Dioxyde d'azote
            """)
        
        with col2:
            st.subheader("Variables Démographiques")
            st.markdown("""
            - **SO₂ (ppb)**: Dioxyde de soufre
            - **CO (ppm)**: Monoxyde de carbone
            - **Proximity_to_Industrial_Areas (km)**: Distance à la zone industrielle
            - **Population_Density (hab/km²)**: Densité de population
            """)
        
        st.subheader("🎯 Variable Cible: Air_Quality")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.success("**0 - Bonne**  \nAir propre")
        with col2:
            st.info("**1 - Modérée**  \nAcceptable")
        with col3:
            st.warning("**2 - Mauvaise**  \nProblèmes pour groupes sensibles")
        with col4:
            st.error("**3 - Dangereuse**  \nGraves risques")
    
    # ============================================================
    # SECTION 2: EXPLORATION DES DONNÉES
    # ============================================================
    elif menu == '🔍 Exploration des Données':
        st.title("🔍 Exploration des Données")
        st.markdown("---")
        
        # Question 1: Types de données
        st.header("1️⃣ Types de Données")
        st.write("**Question**: Quels sont les types de données présents dans le jeu de données ?")
        
        types_df = pd.DataFrame({
            'Variable': data.columns,
            'Type Python': data.dtypes.values,
            'Type Statistique': ['Quantitative Continue' if dt in ['float64', 'int64'] else 'Qualitative' 
                                for dt in data.dtypes.values]
        })
        st.dataframe(types_df, use_container_width=True)
        
        st.info("**Réponse**: Toutes les variables sont quantitatives continues (numériques), ce qui permet d'effectuer des analyses statistiques complètes.")
        
        st.markdown("---")
        
        # Question 2: Dimensions
        st.header("2️⃣ Dimensions du Jeu de Données")
        st.write("**Question**: Combien d'échantillons et de colonnes contient le jeu de données ?")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Nombre de lignes (échantillons)", f"{data.shape[0]:,}")
        with col2:
            st.metric("📋 Nombre de colonnes", data.shape[1])
        with col3:
            st.metric("📈 Total de données", f"{data.shape[0] * data.shape[1]:,}")
        
        st.info(f"**Réponse**: Le jeu de données contient **{data.shape[0]:,} échantillons** (lignes) et **{data.shape[1]} colonnes** (9 variables prédictives + 1 variable cible).")
        
        st.markdown("---")
        
        # Question 3: Valeurs manquantes
        st.header("3️⃣ Valeurs Manquantes")
        st.write("**Question**: Y a-t-il des valeurs manquantes dans le jeu de données ? Si oui, dans quelles colonnes ?")
        
        valeurs_manquantes = data.isnull().sum()
        if valeurs_manquantes.sum() == 0:
            st.success("✅ **Réponse**: Aucune valeur manquante détectée dans le jeu de données nettoyé !")
        else:
            st.warning(f"⚠️ **Réponse**: {valeurs_manquantes.sum()} valeurs manquantes détectées")
            st.dataframe(valeurs_manquantes[valeurs_manquantes > 0])
        
        st.markdown("---")
        
        # Question 4: Traitement des valeurs manquantes
        st.header("4️⃣ Traitement des Valeurs Manquantes")
        st.write("**Question**: Quelle technique a été appliquée pour remplacer les valeurs manquantes ?")
        
        st.info("""
        **Réponse**: La technique d'**imputation par la médiane** a été utilisée.
        
        **Justification**:
        - La médiane est robuste aux valeurs aberrantes (outliers)
        - Elle préserve la distribution centrale des données
        - Elle est appropriée pour les données environnementales qui peuvent contenir des valeurs extrêmes
        
        **Processus**:
        1. Détection des valeurs manquantes dans chaque colonne
        2. Calcul de la médiane pour chaque variable
        3. Remplacement des valeurs manquantes par la médiane correspondante
        """)
        
        st.markdown("---")
        
        # Statistiques descriptives complètes
        st.header("📊 Statistiques Descriptives Complètes")
        st.dataframe(data.describe(), use_container_width=True)
        
        st.markdown("---")
        
        # Distribution de la variable cible
        st.header("🎯 Distribution de la Variable Cible (Air_Quality)")
        
        distribution = data['Air_Quality'].value_counts().sort_index()
        labels_map = {0: 'Bonne', 1: 'Modérée', 2: 'Mauvaise', 3: 'Dangereuse'}
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Répartition")
            for niveau, count in distribution.items():
                pourcentage = (count / len(data)) * 100
                st.metric(
                    f"{labels_map[niveau]} ({niveau})",
                    f"{count} échantillons",
                    f"{pourcentage:.1f}%"
                )
        
        with col2:
            st.subheader("Graphique")
            if os.path.exists('images/01_distribution_air_quality.png'):
                st.image('images/01_distribution_air_quality.png', use_container_width=True)
    
    # ============================================================
    # SECTION 3: VISUALISATIONS
    # ============================================================
    elif menu == '📊 Visualisations':
        st.title("📊 Visualisations Dynamiques")
        st.markdown("---")
        
        # Sous-menu de visualisations
        viz_type = st.selectbox(
            "Choisir le type de visualisation",
            ["Histogrammes", "Boîtes à Moustaches (Boxplots)", "Graphes de Densité", 
             "Diagrammes de Dispersion", "Pairplot"]
        )
        
        if viz_type == "Histogrammes":
            st.header("📊 Histogrammes des Variables")
            st.write("Les histogrammes montrent la distribution de fréquence de chaque variable.")
            
            tab1, tab2 = st.tabs(["Toutes les Variables", "PM2.5 et PM10 Détaillés"])
            
            with tab1:
                if os.path.exists('images/02_histogrammes_variables.png'):
                    st.image('images/02_histogrammes_variables.png', use_container_width=True)
                
                st.info("""
                **Observations**:
                - Les distributions montrent les moyennes (ligne rouge) et médianes (ligne verte)
                - La plupart des variables suivent des distributions approximativement normales
                - Certaines variables présentent des asymétries (skewness)
                """)
            
            with tab2:
                if os.path.exists('images/03_histogrammes_pm25_pm10.png'):
                    st.image('images/03_histogrammes_pm25_pm10.png', use_container_width=True)
                
                # Question 8: Statistiques PM2.5 et PM10
                st.subheader("8️⃣ Statistiques pour PM2.5 et PM10")
                st.write("**Question**: Quelle est la moyenne, la médiane et l'écart-type des concentrations de PM2.5 et PM10 ?")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**PM2.5 (µg/m³)**")
                    st.metric("Moyenne", f"{data['PM2.5'].mean():.3f}")
                    st.metric("Médiane", f"{data['PM2.5'].median():.3f}")
                    st.metric("Écart-type", f"{data['PM2.5'].std():.3f}")
                
                with col2:
                    st.markdown("**PM10 (µg/m³)**")
                    st.metric("Moyenne", f"{data['PM10'].mean():.3f}")
                    st.metric("Médiane", f"{data['PM10'].median():.3f}")
                    st.metric("Écart-type", f"{data['PM10'].std():.3f}")
        
        elif viz_type == "Boîtes à Moustaches (Boxplots)":
            st.header("📦 Boîtes à Moustaches (Boxplots)")
            st.write("Les boxplots permettent d'identifier les valeurs aberrantes et la dispersion des données.")
            
            tab1, tab2 = st.tabs(["Toutes les Variables", "PM2.5 et PM10 Détaillés"])
            
            with tab1:
                if os.path.exists('images/04_boxplots_variables.png'):
                    st.image('images/04_boxplots_variables.png', use_container_width=True)
            
            with tab2:
                if os.path.exists('images/05_boxplots_pm25_pm10.png'):
                    st.image('images/05_boxplots_pm25_pm10.png', use_container_width=True)
                
                # Question 7: Valeurs aberrantes
                st.subheader("7️⃣ Valeurs Aberrantes dans PM2.5 et PM10")
                st.write("**Question**: Existe-t-il des valeurs aberrantes dans les concentrations de PM2.5 ou PM10 ?")
                
                for col in ['PM2.5', 'PM10']:
                    Q1 = data[col].quantile(0.25)
                    Q3 = data[col].quantile(0.75)
                    IQR = Q3 - Q1
                    limite_inf = Q1 - 1.5 * IQR
                    limite_sup = Q3 + 1.5 * IQR
                    
                    outliers = data[(data[col] < limite_inf) | (data[col] > limite_sup)]
                    
                    with st.expander(f"📊 Analyse de {col}"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Q1", f"{Q1:.2f}")
                        with col2:
                            st.metric("Q3", f"{Q3:.2f}")
                        with col3:
                            st.metric("IQR", f"{IQR:.2f}")
                        
                        if len(outliers) > 0:
                            st.warning(f"⚠️ {len(outliers)} valeurs aberrantes détectées (traitées par winsorisation)")
                        else:
                            st.success("✅ Aucune valeur aberrante détectée")
        
        elif viz_type == "Graphes de Densité":
            st.header("📈 Graphes de Densité")
            st.write("Les graphes de densité montrent la distribution de probabilité des variables.")
            
            if os.path.exists('images/06_graphes_densite.png'):
                st.image('images/06_graphes_densite.png', use_container_width=True)
            
            st.info("""
            **Interprétation**:
            - Les pics indiquent les valeurs les plus fréquentes
            - La forme de la courbe révèle la distribution (normale, asymétrique, bimodale, etc.)
            - Les queues de distribution montrent les valeurs extrêmes
            """)
        
        elif viz_type == "Diagrammes de Dispersion":
            st.header("🔵 Diagrammes de Dispersion")
            st.write("Les scatter plots montrent les relations entre variables.")
            
            tab1, tab2 = st.tabs(["Matrice Complète", "Top 3 Corrélations"])
            
            with tab1:
                if os.path.exists('images/08_scatter_matrix.png'):
                    st.image('images/08_scatter_matrix.png', use_container_width=True)
                
                st.info("Les couleurs représentent la qualité de l'air: Vert=Bonne, Jaune=Modérée, Orange=Mauvaise, Rouge=Dangereuse")
            
            with tab2:
                if os.path.exists('images/11_scatter_top3_correlations.png'):
                    st.image('images/11_scatter_top3_correlations.png', use_container_width=True)
        
        elif viz_type == "Pairplot":
            st.header("🎨 Pairplot des Variables")
            st.write("Le pairplot combine histogrammes et scatter plots pour une vue d'ensemble complète.")
            
            if os.path.exists('images/09_pairplot_complet.png'):
                st.image('images/09_pairplot_complet.png', use_container_width=True)
            
            st.info("""
            **Légende des couleurs**:
            - 🟢 Vert: Bonne qualité de l'air (0)
            - 🟡 Jaune: Qualité modérée (1)
            - 🟠 Orange: Mauvaise qualité (2)
            - 🔴 Rouge: Qualité dangereuse (3)
            """)
    
    # ============================================================
    # SECTION 4: ÉTUDE DE CORRÉLATION
    # ============================================================
    elif menu == '🔗 Étude de Corrélation':
        st.title("🔗 Étude de Corrélation")
        st.markdown("---")
        
        # Calculer la matrice de corrélation
        corr_matrix = data.corr()
        
        # Question 5 et 6
        st.header("5️⃣ Facteurs Environnementaux Corrélés avec la Qualité de l'Air")
        st.write("**Question**: Quels sont les facteurs environnementaux les plus corrélés avec la qualité de l'air ?")
        
        correlations_air_quality = corr_matrix['Air_Quality'].drop('Air_Quality').sort_values(ascending=False)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Classement")
            for i, (var, corr) in enumerate(correlations_air_quality.items(), 1):
                force = "🔴 Forte" if abs(corr) > 0.7 else "🟡 Modérée" if abs(corr) > 0.4 else "🟢 Faible"
                st.write(f"**{i}. {var}**")
                st.write(f"   Corrélation: {corr:.3f} ({force})")
        
        with col2:
            st.subheader("Visualisation")
            if os.path.exists('images/10_correlations_air_quality.png'):
                st.image('images/10_correlations_air_quality.png', use_container_width=True)
        
        st.markdown("---")
        
        # Question 6
        st.header("6️⃣ Trois Principaux Contributeurs à la Pollution")
        st.write("**Question**: Quels sont les trois principaux contributeurs aux niveaux de pollution dans le dataset ?")
        
        top_3 = correlations_air_quality.head(3)
        
        col1, col2, col3 = st.columns(3)
        
        for i, ((var, corr), col) in enumerate(zip(top_3.items(), [col1, col2, col3]), 1):
            with col:
                st.metric(
                    f"🥇 #{i}: {var}" if i == 1 else f"🥈 #{i}: {var}" if i == 2 else f"🥉 #{i}: {var}",
                    f"r = {corr:.3f}",
                    "Corrélation forte" if abs(corr) > 0.7 else "Corrélation modérée"
                )
        
        st.success(f"""
        **Réponse**: Les trois principaux contributeurs sont:
        1. **{top_3.index[0]}** (r = {top_3.iloc[0]:.3f})
        2. **{top_3.index[1]}** (r = {top_3.iloc[1]:.3f})
        3. **{top_3.index[2]}** (r = {top_3.iloc[2]:.3f})
        """)
        
        st.markdown("---")
        
        # Heatmap de corrélation
        st.header("🔥 Matrice de Corrélation Complète (Heatmap)")
        
        if os.path.exists('images/07_heatmap_correlation.png'):
            st.image('images/07_heatmap_correlation.png', use_container_width=True)
        
        st.info("""
        **Interprétation des couleurs**:
        - 🟢 Vert: Corrélation positive (les deux variables augmentent ensemble)
        - 🔴 Rouge: Corrélation négative (quand l'une augmente, l'autre diminue)
        - 🟡 Jaune: Corrélation proche de zéro (pas de relation linéaire)
        
        **Valeurs**:
        - Proche de +1: Corrélation positive très forte
        - Proche de -1: Corrélation négative très forte
        - Proche de 0: Pas de corrélation linéaire
        """)
        
        st.markdown("---")
        
        # Afficher la matrice numérique
        with st.expander("📊 Voir la matrice de corrélation numérique"):
            st.dataframe(corr_matrix.style.background_gradient(cmap='RdYlGn', vmin=-1, vmax=1), 
                        use_container_width=True)
    
    # ============================================================
    # SECTION 5: ANALYSE APPROFONDIE
    # ============================================================
    elif menu == '📈 Analyse Approfondie':
        st.title("📈 Analyse Approfondie")
        st.markdown("---")
        
        # Question 9: Humidité et Air Quality
        st.header("9️⃣ Corrélation entre Humidité et Qualité de l'Air")
        st.write("**Question**: Quelle est la corrélation entre l'humidité et la qualité de l'air ?")
        
        corr_humidity = data['Humidity'].corr(data['Air_Quality'])
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Coefficient de Pearson", f"{corr_humidity:.3f}")
            
            if abs(corr_humidity) > 0.7:
                interpretation = "Très forte"
                color = "🔴"
            elif abs(corr_humidity) > 0.4:
                interpretation = "Modérée"
                color = "🟡"
            else:
                interpretation = "Faible"
                color = "🟢"
            
            st.metric("Force de la corrélation", f"{color} {interpretation}")
            st.metric("Direction", "Positive ↗️" if corr_humidity > 0 else "Négative ↘️")
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 5))
            colors_map = {0: 'green', 1: 'yellow', 2: 'orange', 3: 'red'}
            colors = data['Air_Quality'].map(colors_map)
            
            ax.scatter(data['Humidity'], data['Air_Quality'], c=colors, alpha=0.6, s=30, edgecolors='black', linewidth=0.5)
            
            # Ligne de tendance
            z = np.polyfit(data['Humidity'], data['Air_Quality'], 1)
            p = np.poly1d(z)
            ax.plot(data['Humidity'].sort_values(), p(data['Humidity'].sort_values()), 
                   "r--", linewidth=2, label=f'Tendance (r={corr_humidity:.3f})')
            
            ax.set_xlabel('Humidité (%)', fontsize=11, fontweight='bold')
            ax.set_ylabel('Air Quality', fontsize=11, fontweight='bold')
            ax.set_title('Humidité vs Qualité de l\'Air', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
        
        st.info(f"""
        **Réponse**: La corrélation entre l'humidité et la qualité de l'air est **{interpretation.lower()}** et **{'positive' if corr_humidity > 0 else 'négative'}** (r = {corr_humidity:.3f}).
        
        **Signification**: {'L\'augmentation de l\'humidité est associée à une dégradation de la qualité de l\'air.' if corr_humidity > 0 else 'L\'augmentation de l\'humidité est associée à une amélioration de la qualité de l\'air.'}
        """)
        
        st.markdown("---")
        
        # Question 10: Population Density et PM2.5
        st.header("🔟 Lien entre Densité de Population et PM2.5")
        st.write("**Question**: Quel est le lien entre la densité de population et les niveaux de PM2.5 ?")
        
        corr_pop_pm25 = data['Population_Density'].corr(data['PM2.5'])
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Coefficient de Pearson", f"{corr_pop_pm25:.3f}")
            
            if abs(corr_pop_pm25) > 0.7:
                interpretation = "Très forte"
                color = "🔴"
            elif abs(corr_pop_pm25) > 0.4:
                interpretation = "Modérée"
                color = "🟡"
            else:
                interpretation = "Faible"
                color = "🟢"
            
            st.metric("Force de la corrélation", f"{color} {interpretation}")
            st.metric("Direction", "Positive ↗️" if corr_pop_pm25 > 0 else "Négative ↘️")
        
        with col2:
            fig, ax = plt.subplots(figsize=(8, 5))
            
            ax.scatter(data['Population_Density'], data['PM2.5'], alpha=0.6, s=30, 
                      c='steelblue', edgecolors='black', linewidth=0.5)
            
            # Ligne de tendance
            z = np.polyfit(data['Population_Density'], data['PM2.5'], 1)
            p = np.poly1d(z)
            ax.plot(data['Population_Density'].sort_values(), p(data['Population_Density'].sort_values()), 
                   "r--", linewidth=2, label=f'Tendance (r={corr_pop_pm25:.3f})')
            
            ax.set_xlabel('Densité de Population (hab/km²)', fontsize=11, fontweight='bold')
            ax.set_ylabel('PM2.5 (µg/m³)', fontsize=11, fontweight='bold')
            ax.set_title('Densité de Population vs PM2.5', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            st.pyplot(fig)
        
        st.info(f"""
        **Réponse**: La corrélation entre la densité de population et les niveaux de PM2.5 est **{interpretation.lower()}** (r = {corr_pop_pm25:.3f}).
        
        **Signification**: {'Les zones à forte densité de population ont tendance à avoir des niveaux plus élevés de PM2.5.' if corr_pop_pm25 > 0 else 'Les zones à forte densité de population ont tendance à avoir des niveaux plus faibles de PM2.5.'}
        
        **Remarque**: La corrélation très faible suggère que d'autres facteurs (comme la proximité industrielle, les conditions météorologiques) ont une influence plus importante sur les niveaux de PM2.5.
        """)
        
        st.markdown("---")
        
        # Question 11: Quartiles CO
        st.header("1️⃣1️⃣ Quartiles du Monoxyde de Carbone (CO)")
        st.write("**Question**: Quels sont les quartiles des concentrations de monoxyde de carbone (CO) ?")
        
        Q1 = data['CO'].quantile(0.25)
        Q2 = data['CO'].quantile(0.50)
        Q3 = data['CO'].quantile(0.75)
        IQR = Q3 - Q1
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Q1 (25%)", f"{Q1:.3f} ppm")
        with col2:
            st.metric("Q2 (50% - Médiane)", f"{Q2:.3f} ppm")
        with col3:
            st.metric("Q3 (75%)", f"{Q3:.3f} ppm")
        with col4:
            st.metric("IQR", f"{IQR:.3f} ppm")
        
        # Visualisation
        fig, ax = plt.subplots(figsize=(10, 5))
        
        ax.hist(data['CO'], bins=40, color='lightcoral', edgecolor='black', alpha=0.7)
        ax.axvline(Q1, color='blue', linestyle='--', linewidth=2, label=f'Q1 = {Q1:.3f}')
        ax.axvline(Q2, color='green', linestyle='--', linewidth=2, label=f'Q2 = {Q2:.3f}')
        ax.axvline(Q3, color='red', linestyle='--', linewidth=2, label=f'Q3 = {Q3:.3f}')
        
        ax.set_xlabel('CO (ppm)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Fréquence', fontsize=11, fontweight='bold')
        ax.set_title('Distribution du Monoxyde de Carbone (CO) avec Quartiles', fontsize=12, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        
        st.pyplot(fig)
        
        st.success(f"""
        **Réponse**: Les quartiles du CO sont:
        - **Q1 (25e percentile)**: {Q1:.3f} ppm - 25% des valeurs sont inférieures
        - **Q2 (50e percentile - Médiane)**: {Q2:.3f} ppm - Valeur centrale
        - **Q3 (75e percentile)**: {Q3:.3f} ppm - 75% des valeurs sont inférieures
        - **IQR (Intervalle interquartile)**: {IQR:.3f} ppm - Mesure de dispersion
        """)
        
        st.markdown("---")
        
        # Statistiques interactives
        st.header("🔍 Explorateur de Statistiques Interactif")
        
        variable_selectionnee = st.selectbox(
            "Choisir une variable à analyser",
            [col for col in data.columns if col != 'Air_Quality']
        )
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader(f"Statistiques de {variable_selectionnee}")
            stats_df = afficher_statistiques(data, variable_selectionnee)
            st.dataframe(stats_df, use_container_width=True)
        
        with col2:
            st.subheader("Distribution")
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.hist(data[variable_selectionnee], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
            mean_val = data[variable_selectionnee].mean()
            median_val = data[variable_selectionnee].median()
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Moyenne: {mean_val:.2f}')
            ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Médiane: {median_val:.2f}')
            ax.set_xlabel(variable_selectionnee, fontsize=11, fontweight='bold')
            ax.set_ylabel('Fréquence', fontsize=11)
            ax.set_title(f'Distribution de {variable_selectionnee}', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)

else:
    st.error("❌ Impossible de charger les données. Veuillez vérifier que le fichier 'pollution_clean.csv' existe.")
