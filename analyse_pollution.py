"""
Projet 1 - Analyse de la Qualité de l'Air et de la Pollution
420-IAA-TT - Intelligence Artificielle 1
Institut Teccart - Automne 2025
Par: Benfriha Hichem

Ce script effectue une analyse complète des données de pollution atmosphérique.
"""

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pandas.plotting import scatter_matrix

# Configuration de l'affichage
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.precision', 3)

# Configuration des graphiques
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class AnalysePollution:
    """Classe pour l'analyse des données de pollution atmosphérique"""
    
    def __init__(self, fichier_csv):
        """
        Initialise l'analyse avec le fichier CSV
        
        Args:
            fichier_csv (str): Chemin vers le fichier CSV
        """
        self.fichier = fichier_csv
        self.data = None
        self.data_clean = None
        self.colonnes = [
            'Temperature', 'Humidity', 'PM2.5', 'PM10', 
            'NO2', 'SO2', 'CO', 'Proximity_to_Industrial_Areas',
            'Population_Density', 'Air_Quality'
        ]
        
    def charger_donnees(self):
        """Charge les données depuis le fichier CSV"""
        try:
            self.data = pd.read_csv(self.fichier, names=self.colonnes, header=0)
            print("✓ Données chargées avec succès!")
            print(f"  Dimensions: {self.data.shape[0]} lignes × {self.data.shape[1]} colonnes")
            return True
        except Exception as e:
            print(f"✗ Erreur lors du chargement: {e}")
            return False
    
    def explorer_donnees(self):
        """Explore la structure des données"""
        print("\n" + "="*70)
        print("EXPLORATION DES DONNÉES")
        print("="*70)
        
        # Question 1: Types de données
        print("\n1. TYPES DE DONNÉES:")
        print("-" * 70)
        types_info = self.data.dtypes
        for col, dtype in types_info.items():
            if dtype in ['int64', 'float64']:
                print(f"  • {col}: {dtype} (Quantitative)")
            else:
                print(f"  • {col}: {dtype} (Qualitative)")
        
        # Question 2: Dimensions
        print(f"\n2. DIMENSIONS DU JEU DE DONNÉES:")
        print("-" * 70)
        print(f"  • Nombre d'échantillons (lignes): {self.data.shape[0]}")
        print(f"  • Nombre de colonnes: {self.data.shape[1]}")
        print(f"  • Variables prédictives: {self.data.shape[1] - 1}")
        print(f"  • Variable cible: 1 (Air_Quality)")
        
        # Question 3: Valeurs manquantes
        print(f"\n3. VALEURS MANQUANTES:")
        print("-" * 70)
        valeurs_manquantes = self.data.isnull().sum()
        total_manquantes = valeurs_manquantes.sum()
        
        if total_manquantes > 0:
            print(f"  ⚠ Total de valeurs manquantes: {total_manquantes}")
            for col, count in valeurs_manquantes.items():
                if count > 0:
                    pourcentage = (count / len(self.data)) * 100
                    print(f"    • {col}: {count} valeurs ({pourcentage:.2f}%)")
        else:
            print("  ✓ Aucune valeur manquante détectée")
        
        # Afficher un aperçu des données
        print(f"\n4. APERÇU DES DONNÉES (5 premières lignes):")
        print("-" * 70)
        print(self.data.head())
        
        # Distribution de la variable cible
        print(f"\n5. DISTRIBUTION DE LA VARIABLE CIBLE (Air_Quality):")
        print("-" * 70)
        distribution = self.data['Air_Quality'].value_counts().sort_index()
        labels = {0: 'Bonne', 1: 'Modérée', 2: 'Mauvaise', 3: 'Dangereuse'}
        for niveau, count in distribution.items():
            pourcentage = (count / len(self.data)) * 100
            print(f"  • Niveau {niveau} ({labels[niveau]}): {count} échantillons ({pourcentage:.2f}%)")
    
    def nettoyer_donnees(self):
        """Nettoie les données (valeurs manquantes et aberrantes)"""
        print("\n" + "="*70)
        print("NETTOYAGE DES DONNÉES")
        print("="*70)
        
        # Copie des données originales
        self.data_clean = self.data.copy()
        
        # Question 4: Traitement des valeurs manquantes
        print("\n4. TRAITEMENT DES VALEURS MANQUANTES:")
        print("-" * 70)
        
        valeurs_manquantes = self.data_clean.isnull().sum()
        if valeurs_manquantes.sum() > 0:
            print("  Méthode: Imputation par la médiane (robuste aux outliers)")
            for col in self.data_clean.columns:
                if self.data_clean[col].isnull().sum() > 0:
                    mediane = self.data_clean[col].median()
                    nb_remplaces = self.data_clean[col].isnull().sum()
                    self.data_clean[col].fillna(mediane, inplace=True)
                    print(f"    • {col}: {nb_remplaces} valeurs remplacées par {mediane:.2f}")
            print("  ✓ Toutes les valeurs manquantes ont été traitées")
        else:
            print("  ✓ Aucune valeur manquante à traiter")
        
        # Question 7: Détection des valeurs aberrantes
        print("\n7. DÉTECTION DES VALEURS ABERRANTES (PM2.5 et PM10):")
        print("-" * 70)
        print("  Méthode: IQR (Interquartile Range)")
        
        for col in ['PM2.5', 'PM10']:
            Q1 = self.data_clean[col].quantile(0.25)
            Q3 = self.data_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            limite_inf = Q1 - 1.5 * IQR
            limite_sup = Q3 + 1.5 * IQR
            
            outliers = self.data_clean[(self.data_clean[col] < limite_inf) | 
                                       (self.data_clean[col] > limite_sup)]
            
            print(f"\n  {col}:")
            print(f"    • Q1 = {Q1:.2f}, Q3 = {Q3:.2f}, IQR = {IQR:.2f}")
            print(f"    • Limites: [{limite_inf:.2f}, {limite_sup:.2f}]")
            print(f"    • Nombre d'outliers: {len(outliers)}")
            
            if len(outliers) > 0:
                print(f"    • Valeurs aberrantes détectées:")
                print(f"      Min outlier: {outliers[col].min():.2f}")
                print(f"      Max outlier: {outliers[col].max():.2f}")
                
                # Traitement: winsorisation (cap aux limites)
                self.data_clean.loc[self.data_clean[col] < limite_inf, col] = limite_inf
                self.data_clean.loc[self.data_clean[col] > limite_sup, col] = limite_sup
                print(f"    ✓ Outliers traités par winsorisation")
            else:
                print(f"    ✓ Aucune valeur aberrante détectée")
        
        print(f"\n✓ Nettoyage terminé!")
        print(f"  Données nettoyées: {self.data_clean.shape[0]} lignes × {self.data_clean.shape[1]} colonnes")
    
    def statistiques_descriptives(self):
        """Calcule les statistiques descriptives complètes"""
        print("\n" + "="*70)
        print("STATISTIQUES DESCRIPTIVES")
        print("="*70)
        
        # Question 8: Statistiques pour PM2.5 et PM10
        print("\n8. STATISTIQUES POUR PM2.5 ET PM10:")
        print("-" * 70)
        
        for col in ['PM2.5', 'PM10']:
            print(f"\n  {col}:")
            moyenne = self.data_clean[col].mean()
            mediane = self.data_clean[col].median()
            ecart_type = self.data_clean[col].std()
            variance = self.data_clean[col].var()
            minimum = self.data_clean[col].min()
            maximum = self.data_clean[col].max()
            
            print(f"    • Moyenne: {moyenne:.3f} µg/m³")
            print(f"    • Médiane: {mediane:.3f} µg/m³")
            print(f"    • Écart-type: {ecart_type:.3f} µg/m³")
            print(f"    • Variance: {variance:.3f}")
            print(f"    • Minimum: {minimum:.3f} µg/m³")
            print(f"    • Maximum: {maximum:.3f} µg/m³")
        
        # Question 11: Quartiles pour CO
        print("\n11. QUARTILES POUR LE MONOXYDE DE CARBONE (CO):")
        print("-" * 70)
        Q1 = self.data_clean['CO'].quantile(0.25)
        Q2 = self.data_clean['CO'].quantile(0.50)  # Médiane
        Q3 = self.data_clean['CO'].quantile(0.75)
        
        print(f"  • Q1 (25e percentile): {Q1:.3f} ppm")
        print(f"  • Q2 (50e percentile - Médiane): {Q2:.3f} ppm")
        print(f"  • Q3 (75e percentile): {Q3:.3f} ppm")
        print(f"  • Intervalle interquartile (IQR): {Q3 - Q1:.3f} ppm")
        
        # Statistiques complètes pour toutes les variables
        print("\nSTATISTIQUES COMPLÈTES POUR TOUTES LES VARIABLES:")
        print("-" * 70)
        print(self.data_clean.describe())
    
    def analyser_correlations(self):
        """Analyse les corrélations entre variables"""
        print("\n" + "="*70)
        print("ANALYSE DES CORRÉLATIONS")
        print("="*70)
        
        # Matrice de corrélation
        corr_matrix = self.data_clean.corr()
        
        # Question 5 et 6: Corrélations avec Air_Quality
        print("\n5. FACTEURS ENVIRONNEMENTAUX CORRÉLÉS AVEC LA QUALITÉ DE L'AIR:")
        print("-" * 70)
        
        correlations_air_quality = corr_matrix['Air_Quality'].drop('Air_Quality').sort_values(ascending=False)
        
        print("\n  Corrélations (de la plus forte à la plus faible):")
        for variable, corr in correlations_air_quality.items():
            force = "forte" if abs(corr) > 0.7 else "modérée" if abs(corr) > 0.4 else "faible"
            signe = "positive" if corr > 0 else "négative"
            print(f"    • {variable}: {corr:.3f} ({force}, {signe})")
        
        print("\n6. TROIS PRINCIPAUX CONTRIBUTEURS À LA POLLUTION:")
        print("-" * 70)
        top_3 = correlations_air_quality.head(3)
        for i, (variable, corr) in enumerate(top_3.items(), 1):
            print(f"  {i}. {variable}: corrélation = {corr:.3f}")
        
        # Question 9: Corrélation Humidité - Air_Quality
        print("\n9. CORRÉLATION ENTRE HUMIDITÉ ET QUALITÉ DE L'AIR:")
        print("-" * 70)
        corr_humidity = corr_matrix.loc['Humidity', 'Air_Quality']
        print(f"  • Coefficient de corrélation de Pearson: {corr_humidity:.3f}")
        
        if abs(corr_humidity) > 0.7:
            interpretation = "très forte"
        elif abs(corr_humidity) > 0.4:
            interpretation = "modérée"
        else:
            interpretation = "faible"
        
        signe = "positive" if corr_humidity > 0 else "négative"
        print(f"  • Interprétation: Corrélation {interpretation} et {signe}")
        
        if corr_humidity > 0:
            print(f"  • Signification: L'augmentation de l'humidité est associée")
            print(f"    à une dégradation de la qualité de l'air")
        else:
            print(f"  • Signification: L'augmentation de l'humidité est associée")
            print(f"    à une amélioration de la qualité de l'air")
        
        # Question 10: Corrélation Population_Density - PM2.5
        print("\n10. LIEN ENTRE DENSITÉ DE POPULATION ET PM2.5:")
        print("-" * 70)
        corr_pop_pm25 = corr_matrix.loc['Population_Density', 'PM2.5']
        print(f"  • Coefficient de corrélation de Pearson: {corr_pop_pm25:.3f}")
        
        if abs(corr_pop_pm25) > 0.7:
            interpretation = "très forte"
        elif abs(corr_pop_pm25) > 0.4:
            interpretation = "modérée"
        else:
            interpretation = "faible"
        
        signe = "positive" if corr_pop_pm25 > 0 else "négative"
        print(f"  • Interprétation: Corrélation {interpretation} et {signe}")
        
        if corr_pop_pm25 > 0:
            print(f"  • Signification: Les zones à forte densité de population")
            print(f"    ont tendance à avoir des niveaux plus élevés de PM2.5")
        else:
            print(f"  • Signification: Les zones à forte densité de population")
            print(f"    ont tendance à avoir des niveaux plus faibles de PM2.5")
        
        # Afficher la matrice complète
        print("\nMATRICE DE CORRÉLATION COMPLÈTE:")
        print("-" * 70)
        print(corr_matrix)
        
        return corr_matrix
    
    def sauvegarder_resultats(self):
        """Sauvegarde les données nettoyées"""
        fichier_sortie = 'pollution_clean.csv'
        self.data_clean.to_csv(fichier_sortie, index=False)
        print(f"\n✓ Données nettoyées sauvegardées dans: {fichier_sortie}")
        return fichier_sortie


def main():
    """Fonction principale"""
    print("\n" + "="*70)
    print("PROJET 1 - ANALYSE DE LA QUALITÉ DE L'AIR ET DE LA POLLUTION")
    print("420-IAA-TT - Intelligence Artificielle 1")
    print("Institut Teccart - Automne 2025")
    print("="*70)
    
    # Initialisation
    analyse = AnalysePollution('pollution.csv')
    
    # Étape 1: Charger les données
    if not analyse.charger_donnees():
        return
    
    # Étape 2: Explorer les données
    analyse.explorer_donnees()
    
    # Étape 3: Nettoyer les données
    analyse.nettoyer_donnees()
    
    # Étape 4: Statistiques descriptives
    analyse.statistiques_descriptives()
    
    # Étape 5: Analyser les corrélations
    analyse.analyser_correlations()
    
    # Étape 6: Sauvegarder les résultats
    analyse.sauvegarder_resultats()
    
    print("\n" + "="*70)
    print("✓ ANALYSE TERMINÉE AVEC SUCCÈS!")
    print("="*70)


if __name__ == "__main__":
    main()
