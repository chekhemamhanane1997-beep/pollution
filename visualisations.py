"""
Projet 1 - Visualisations pour l'Analyse de la Qualité de l'Air
420-IAA-TT - Intelligence Artificielle 1
Institut Teccart - Automne 2025

Ce script génère toutes les visualisations nécessaires pour l'analyse.
"""

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix
import os

# Configuration des graphiques
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

class VisualisationPollution:
    """Classe pour créer les visualisations des données de pollution"""
    
    def __init__(self, fichier_csv):
        """
        Initialise avec le fichier CSV nettoyé
        
        Args:
            fichier_csv (str): Chemin vers le fichier CSV nettoyé
        """
        self.data = pd.read_csv(fichier_csv)
        self.dossier_images = 'images'
        
        # Créer le dossier images s'il n'existe pas
        if not os.path.exists(self.dossier_images):
            os.makedirs(self.dossier_images)
            print(f"✓ Dossier '{self.dossier_images}' créé")
    
    def distribution_air_quality(self):
        """Graphique de distribution de la qualité de l'air"""
        print("\n1. Création du graphique de distribution de la qualité de l'air...")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Compter les valeurs
        counts = self.data['Air_Quality'].value_counts().sort_index()
        labels = ['Bonne\n(0)', 'Modérée\n(1)', 'Mauvaise\n(2)', 'Dangereuse\n(3)']
        colors = ['#2ecc71', '#f39c12', '#e74c3c', '#8b0000']
        
        # Créer le bar plot
        bars = ax.bar(range(len(counts)), counts.values, color=colors, edgecolor='black', linewidth=1.5)
        
        # Ajouter les valeurs sur les barres
        for i, (bar, count) in enumerate(zip(bars, counts.values)):
            height = bar.get_height()
            pourcentage = (count / len(self.data)) * 100
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{count}\n({pourcentage:.1f}%)',
                   ha='center', va='bottom', fontweight='bold', fontsize=11)
        
        ax.set_xlabel('Niveau de Qualité de l\'Air', fontsize=12, fontweight='bold')
        ax.set_ylabel('Nombre d\'Échantillons', fontsize=12, fontweight='bold')
        ax.set_title('Distribution de la Qualité de l\'Air', fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        fichier = f'{self.dossier_images}/01_distribution_air_quality.png'
        plt.savefig(fichier, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Sauvegardé: {fichier}")
    
    def histogrammes_variables(self):
        """Histogrammes pour toutes les variables"""
        print("\n2. Création des histogrammes pour toutes les variables...")
        
        # Exclure la variable cible
        colonnes = [col for col in self.data.columns if col != 'Air_Quality']
        
        fig, axes = plt.subplots(3, 3, figsize=(15, 12))
        axes = axes.ravel()
        
        for i, col in enumerate(colonnes):
            ax = axes[i]
            ax.hist(self.data[col], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
            ax.set_xlabel(col, fontsize=10, fontweight='bold')
            ax.set_ylabel('Fréquence', fontsize=10)
            ax.set_title(f'Distribution de {col}', fontsize=11, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            
            # Ajouter statistiques
            mean_val = self.data[col].mean()
            median_val = self.data[col].median()
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Moyenne: {mean_val:.2f}')
            ax.axvline(median_val, color='green', linestyle='--', linewidth=2, label=f'Médiane: {median_val:.2f}')
            ax.legend(fontsize=8)
        
        plt.suptitle('Histogrammes des Variables Environnementales', 
                    fontsize=16, fontweight='bold', y=0.995)
        plt.tight_layout()
        
        fichier = f'{self.dossier_images}/02_histogrammes_variables.png'
        plt.savefig(fichier, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Sauvegardé: {fichier}")
    
    def histogrammes_pm25_pm10(self):
        """Histogrammes détaillés pour PM2.5 et PM10"""
        print("\n3. Création des histogrammes détaillés pour PM2.5 et PM10...")
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        for i, col in enumerate(['PM2.5', 'PM10']):
            ax = axes[i]
            
            # Histogramme
            n, bins, patches = ax.hist(self.data[col], bins=40, color='skyblue', 
                                       edgecolor='black', alpha=0.7)
            
            # Statistiques
            mean_val = self.data[col].mean()
            median_val = self.data[col].median()
            std_val = self.data[col].std()
            
            # Lignes verticales
            ax.axvline(mean_val, color='red', linestyle='--', linewidth=2.5, 
                      label=f'Moyenne: {mean_val:.2f}')
            ax.axvline(median_val, color='green', linestyle='--', linewidth=2.5, 
                      label=f'Médiane: {median_val:.2f}')
            ax.axvline(mean_val - std_val, color='orange', linestyle=':', linewidth=2, 
                      label=f'±1 écart-type')
            ax.axvline(mean_val + std_val, color='orange', linestyle=':', linewidth=2)
            
            ax.set_xlabel(f'{col} (µg/m³)', fontsize=11, fontweight='bold')
            ax.set_ylabel('Fréquence', fontsize=11, fontweight='bold')
            ax.set_title(f'Distribution de {col}', fontsize=12, fontweight='bold')
            ax.legend(fontsize=9)
            ax.grid(axis='y', alpha=0.3)
        
        plt.suptitle('Analyse Détaillée des Particules Fines (PM2.5) et Grossières (PM10)', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        fichier = f'{self.dossier_images}/03_histogrammes_pm25_pm10.png'
        plt.savefig(fichier, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Sauvegardé: {fichier}")
    
    def boxplots_variables(self):
        """Boîtes à moustaches pour toutes les variables"""
        print("\n4. Création des boxplots pour toutes les variables...")
        
        colonnes = [col for col in self.data.columns if col != 'Air_Quality']
        
        fig, axes = plt.subplots(3, 3, figsize=(15, 12))
        axes = axes.ravel()
        
        for i, col in enumerate(colonnes):
            ax = axes[i]
            bp = ax.boxplot(self.data[col], vert=True, patch_artist=True,
                           boxprops=dict(facecolor='lightblue', color='navy'),
                           whiskerprops=dict(color='navy', linewidth=1.5),
                           capprops=dict(color='navy', linewidth=1.5),
                           medianprops=dict(color='red', linewidth=2),
                           flierprops=dict(marker='o', markerfacecolor='red', 
                                         markersize=5, alpha=0.5))
            
            ax.set_ylabel(col, fontsize=10, fontweight='bold')
            ax.set_title(f'Boxplot de {col}', fontsize=11, fontweight='bold')
            ax.grid(axis='y', alpha=0.3)
            
            # Ajouter statistiques
            Q1 = self.data[col].quantile(0.25)
            Q2 = self.data[col].quantile(0.50)
            Q3 = self.data[col].quantile(0.75)
            ax.text(1.15, Q1, f'Q1: {Q1:.2f}', fontsize=8, va='center')
            ax.text(1.15, Q2, f'Q2: {Q2:.2f}', fontsize=8, va='center', color='red', fontweight='bold')
            ax.text(1.15, Q3, f'Q3: {Q3:.2f}', fontsize=8, va='center')
        
        plt.suptitle('Boîtes à Moustaches des Variables Environnementales', 
                    fontsize=16, fontweight='bold', y=0.995)
        plt.tight_layout()
        
        fichier = f'{self.dossier_images}/04_boxplots_variables.png'
        plt.savefig(fichier, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Sauvegardé: {fichier}")
    
    def boxplots_pm25_pm10(self):
        """Boxplots détaillés pour PM2.5 et PM10"""
        print("\n5. Création des boxplots détaillés pour PM2.5 et PM10...")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        data_to_plot = [self.data['PM2.5'], self.data['PM10']]
        bp = ax.boxplot(data_to_plot, labels=['PM2.5', 'PM10'], patch_artist=True,
                       boxprops=dict(facecolor='lightcoral', color='darkred', linewidth=2),
                       whiskerprops=dict(color='darkred', linewidth=2),
                       capprops=dict(color='darkred', linewidth=2),
                       medianprops=dict(color='blue', linewidth=3),
                       flierprops=dict(marker='D', markerfacecolor='red', 
                                     markersize=6, alpha=0.6))
        
        ax.set_ylabel('Concentration (µg/m³)', fontsize=12, fontweight='bold')
        ax.set_title('Comparaison des Distributions de PM2.5 et PM10\n(Détection des Valeurs Aberrantes)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.grid(axis='y', alpha=0.3)
        
        # Ajouter les statistiques
        for i, col in enumerate(['PM2.5', 'PM10'], 1):
            Q1 = self.data[col].quantile(0.25)
            Q2 = self.data[col].quantile(0.50)
            Q3 = self.data[col].quantile(0.75)
            IQR = Q3 - Q1
            
            stats_text = f'{col}:\nQ1={Q1:.2f}\nQ2={Q2:.2f}\nQ3={Q3:.2f}\nIQR={IQR:.2f}'
            ax.text(i + 0.25, ax.get_ylim()[1] * 0.7, stats_text, 
                   fontsize=9, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        fichier = f'{self.dossier_images}/05_boxplots_pm25_pm10.png'
        plt.savefig(fichier, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Sauvegardé: {fichier}")
    
    def graphes_densite(self):
        """Graphes de densité pour les variables principales"""
        print("\n6. Création des graphes de densité...")
        
        colonnes = ['Temperature', 'Humidity', 'PM2.5', 'PM10', 'NO2', 'SO2', 'CO']
        
        fig, axes = plt.subplots(3, 3, figsize=(15, 12))
        axes = axes.ravel()
        
        for i, col in enumerate(colonnes):
            ax = axes[i]
            self.data[col].plot(kind='density', ax=ax, color='darkblue', linewidth=2)
            ax.set_xlabel(col, fontsize=10, fontweight='bold')
            ax.set_ylabel('Densité', fontsize=10)
            ax.set_title(f'Densité de {col}', fontsize=11, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.fill_between(ax.get_xlim(), 0, ax.get_ylim()[1], alpha=0.2, color='skyblue')
        
        # Supprimer les axes vides
        for j in range(len(colonnes), len(axes)):
            fig.delaxes(axes[j])
        
        plt.suptitle('Graphes de Densité des Variables Environnementales', 
                    fontsize=16, fontweight='bold', y=0.995)
        plt.tight_layout()
        
        fichier = f'{self.dossier_images}/06_graphes_densite.png'
        plt.savefig(fichier, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Sauvegardé: {fichier}")
    
    def heatmap_correlation(self):
        """Heatmap de la matrice de corrélation"""
        print("\n7. Création de la heatmap de corrélation...")
        
        # Calculer la matrice de corrélation
        corr_matrix = self.data.corr()
        
        fig, ax = plt.subplots(figsize=(14, 12))
        
        # Créer la heatmap
        sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdYlGn', 
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
                   ax=ax, vmin=-1, vmax=1)
        
        ax.set_title('Matrice de Corrélation des Variables Environnementales', 
                    fontsize=16, fontweight='bold', pad=20)
        
        # Rotation des labels
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        
        fichier = f'{self.dossier_images}/07_heatmap_correlation.png'
        plt.savefig(fichier, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Sauvegardé: {fichier}")
    
    def scatter_matrix_plot(self):
        """Matrice de diagrammes de dispersion"""
        print("\n8. Création de la matrice de dispersion...")
        
        # Sélectionner les variables principales
        colonnes = ['Temperature', 'Humidity', 'PM2.5', 'PM10', 'NO2', 'SO2', 'Air_Quality']
        data_subset = self.data[colonnes]
        
        fig = plt.figure(figsize=(16, 16))
        
        # Créer la scatter matrix avec couleurs selon Air_Quality
        colors = self.data['Air_Quality'].map({0: 'green', 1: 'yellow', 2: 'orange', 3: 'red'})
        scatter_matrix(data_subset, alpha=0.6, figsize=(16, 16), 
                      diagonal='hist', c=colors, s=20)
        
        plt.suptitle('Matrice de Dispersion des Variables Principales\n(Couleurs: Vert=Bonne, Jaune=Modérée, Orange=Mauvaise, Rouge=Dangereuse)', 
                    fontsize=16, fontweight='bold', y=0.995)
        
        fichier = f'{self.dossier_images}/08_scatter_matrix.png'
        plt.savefig(fichier, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Sauvegardé: {fichier}")
    
    def pairplot_complet(self):
        """Pairplot avec seaborn"""
        print("\n9. Création du pairplot complet...")
        
        # Sélectionner les variables principales
        colonnes = ['Temperature', 'Humidity', 'PM2.5', 'PM10', 'NO2', 'SO2', 'Air_Quality']
        data_subset = self.data[colonnes]
        
        # Créer le pairplot
        g = sns.pairplot(data_subset, hue='Air_Quality', 
                        palette={0: 'green', 1: 'yellow', 2: 'orange', 3: 'red'},
                        diag_kind='kde', plot_kws={'alpha': 0.6, 's': 30},
                        height=2.5)
        
        g.fig.suptitle('Pairplot des Variables Environnementales par Qualité de l\'Air', 
                      fontsize=16, fontweight='bold', y=1.001)
        
        # Légende personnalisée
        handles = g._legend_data.values()
        labels = ['Bonne (0)', 'Modérée (1)', 'Mauvaise (2)', 'Dangereuse (3)']
        g._legend.remove()
        g.fig.legend(handles=handles, labels=labels, loc='upper right', 
                    bbox_to_anchor=(0.98, 0.98), fontsize=10)
        
        fichier = f'{self.dossier_images}/09_pairplot_complet.png'
        plt.savefig(fichier, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Sauvegardé: {fichier}")
    
    def correlations_air_quality(self):
        """Graphique des corrélations avec Air_Quality"""
        print("\n10. Création du graphique des corrélations avec Air_Quality...")
        
        # Calculer les corrélations
        corr_with_target = self.data.corr()['Air_Quality'].drop('Air_Quality').sort_values(ascending=True)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Créer le bar plot horizontal
        colors = ['red' if x < 0 else 'green' for x in corr_with_target.values]
        bars = ax.barh(range(len(corr_with_target)), corr_with_target.values, color=colors, alpha=0.7, edgecolor='black')
        
        # Ajouter les valeurs
        for i, (bar, val) in enumerate(zip(bars, corr_with_target.values)):
            ax.text(val + 0.02 if val > 0 else val - 0.02, i, f'{val:.3f}',
                   va='center', ha='left' if val > 0 else 'right', fontweight='bold', fontsize=10)
        
        ax.set_yticks(range(len(corr_with_target)))
        ax.set_yticklabels(corr_with_target.index, fontsize=11)
        ax.set_xlabel('Coefficient de Corrélation de Pearson', fontsize=12, fontweight='bold')
        ax.set_title('Corrélations des Variables avec la Qualité de l\'Air', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.axvline(0, color='black', linewidth=1)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        fichier = f'{self.dossier_images}/10_correlations_air_quality.png'
        plt.savefig(fichier, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Sauvegardé: {fichier}")
    
    def scatter_top_correlations(self):
        """Diagrammes de dispersion pour les 3 principales corrélations"""
        print("\n11. Création des scatter plots pour les top 3 corrélations...")
        
        # Top 3 corrélations
        corr_with_target = self.data.corr()['Air_Quality'].drop('Air_Quality').sort_values(ascending=False)
        top_3 = corr_with_target.head(3)
        
        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        
        colors_map = {0: 'green', 1: 'yellow', 2: 'orange', 3: 'red'}
        colors = self.data['Air_Quality'].map(colors_map)
        
        for i, (var, corr) in enumerate(top_3.items()):
            ax = axes[i]
            scatter = ax.scatter(self.data[var], self.data['Air_Quality'], 
                               c=colors, alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
            
            # Ligne de tendance
            z = np.polyfit(self.data[var], self.data['Air_Quality'], 1)
            p = np.poly1d(z)
            ax.plot(self.data[var].sort_values(), p(self.data[var].sort_values()), 
                   "r--", linewidth=2, label=f'Tendance (r={corr:.3f})')
            
            ax.set_xlabel(var, fontsize=11, fontweight='bold')
            ax.set_ylabel('Air Quality', fontsize=11, fontweight='bold')
            ax.set_title(f'{var} vs Air Quality\n(Corrélation: {corr:.3f})', 
                        fontsize=12, fontweight='bold')
            ax.legend(fontsize=9)
            ax.grid(True, alpha=0.3)
        
        plt.suptitle('Top 3 Variables Corrélées avec la Qualité de l\'Air', 
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        fichier = f'{self.dossier_images}/11_scatter_top3_correlations.png'
        plt.savefig(fichier, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"  ✓ Sauvegardé: {fichier}")
    
    def generer_toutes_visualisations(self):
        """Génère toutes les visualisations"""
        print("\n" + "="*70)
        print("GÉNÉRATION DES VISUALISATIONS")
        print("="*70)
        
        self.distribution_air_quality()
        self.histogrammes_variables()
        self.histogrammes_pm25_pm10()
        self.boxplots_variables()
        self.boxplots_pm25_pm10()
        self.graphes_densite()
        self.heatmap_correlation()
        self.scatter_matrix_plot()
        self.pairplot_complet()
        self.correlations_air_quality()
        self.scatter_top_correlations()
        
        print("\n" + "="*70)
        print("✓ TOUTES LES VISUALISATIONS ONT ÉTÉ GÉNÉRÉES AVEC SUCCÈS!")
        print(f"✓ Les images sont sauvegardées dans le dossier: {self.dossier_images}/")
        print("="*70)


def main():
    """Fonction principale"""
    print("\n" + "="*70)
    print("PROJET 1 - VISUALISATIONS DE LA QUALITÉ DE L'AIR")
    print("420-IAA-TT - Intelligence Artificielle 1")
    print("Institut Teccart - Automne 2025")
    print("="*70)
    
    # Créer les visualisations
    viz = VisualisationPollution('pollution_clean.csv')
    viz.generer_toutes_visualisations()


if __name__ == "__main__":
    main()
