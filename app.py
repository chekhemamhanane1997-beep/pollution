import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# --- Configuration ---
st.set_page_config(page_title="Projet IA Qualité de l'Air", layout="wide")
API_URL = "http://localhost:5000" # L'URL de l'API Flask

# Mapping pour la qualité de l'air
QUALITY_MAP = {0: 'Bonne', 1: 'Modérée', 2: 'Mauvaise', 3: 'Dangereuse'}
QUALITY_COLORS = {
    'Bonne': '#28a745', 
    'Modérée': '#ffc107', 
    'Mauvaise': '#fd7e14', 
    'Dangereuse': '#dc3545'
}
FEATURES = ['Temperature', 'Humidity', 'PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'Proximite_zones_industrielles', 'Densite_population']

# --- Fonctions d'Interaction avec l'API ---

@st.cache_data(ttl=60)
def get_models():
    """Récupère la liste des modèles disponibles depuis l'API."""
    try:
        response = requests.get(f"{API_URL}/models")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"Erreur de connexion à l'API Flask. Assurez-vous que le backend est lancé à {API_URL}.")
        return None
    except Exception as e:
        st.error(f"Erreur lors de la récupération des modèles: {e}")
        return None

def train_model(model_name):
    """Lance l'entraînement d'un modèle via l'API."""
    try:
        response = requests.post(f"{API_URL}/train", json={'model_name': model_name})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'entraînement du modèle {model_name}: {e}")
        return None

def predict_data(model_name, features):
    """Effectue une prédiction via l'API."""
    try:
        response = requests.post(f"{API_URL}/predict", json={'model_name': model_name, 'features': features})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la prédiction avec {model_name}: {e}")
        return None

# --- Pages Streamlit ---

def home_page():
    st.title("🏠 Projet IA : Classification de la Qualité de l'Air")
    st.markdown("---")
    
    st.markdown("""
    ### 📚 Description du Projet
    Ce projet implémente une architecture client-serveur pour l'étude comparative de modèles de classification 
    et la prédiction en temps réel de la qualité de l'air.
    
    - **Backend:** API Flask pour la gestion des données, l'entraînement et la prédiction des modèles.
    - **Frontend:** Application Streamlit pour l'interface utilisateur, la visualisation et les interactions.
    
    ### 🚀 Étapes d'Exécution
    1. **Lancer le Backend:** `python api.py` dans le dossier `backend`.
    2. **Lancer le Frontend:** `streamlit run app.py` dans le dossier `frontend`.
    3. **Naviguer** vers la page **Apprentissage** pour entraîner les modèles.
    4. **Naviguer** vers la page **Prédiction** pour tester les modèles entraînés.
    """)
    
    st.markdown("---")
    
    models_status = get_models()
    if models_status:
        st.subheader("Statut de l'API et des Modèles")
        st.success("✅ Connexion à l'API Flask établie.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Modèles disponibles pour l'entraînement: **{', '.join(models_status['available_for_training'])}**")
        with col2:
            if models_status['trained']:
                st.success(f"Modèles entraînés et sauvegardés: **{', '.join(models_status['trained'])}**")
            else:
                st.warning("Aucun modèle n'est encore entraîné. Rendez-vous sur la page 'Apprentissage'.")

def training_page():
    st.title("🧠 Apprentissage et Comparaison des Modèles")
    st.markdown("---")
    
    models_status = get_models()
    if not models_status:
        return

    available_models = models_status['available_for_training']
    
    st.subheader("1. Sélection des Modèles à Entraîner")
    selected_models = st.multiselect(
        "Choisissez les modèles à entraîner:",
        options=available_models,
        default=models_status['trained'] if models_status['trained'] else available_models
    )
    
    if st.button("🚀 Lancer l'Entraînement et la Comparaison"):
        if not selected_models:
            st.warning("Veuillez sélectionner au moins un modèle.")
            return
            
        st.info("Début de l'entraînement des modèles...")
        
        results = []
        progress_bar = st.progress(0)
        
        for i, model_name in enumerate(selected_models):
            st.write(f"Entraînement de **{model_name}**...")
            result = train_model(model_name)
            
            if result and 'metrics' in result:
                metrics = result['metrics']
                metrics['Model'] = model_name
                results.append(metrics)
                st.success(f"✅ {model_name} entraîné avec succès. Accuracy: {metrics['accuracy']:.4f}")
            
            progress_bar.progress((i + 1) / len(selected_models))
            
        st.markdown("---")
        st.subheader("2. Résultats Comparatifs")
        
        if results:
            df_results = pd.DataFrame(results)
            df_results = df_results.set_index('Model').drop(columns=['confusion_matrix'])
            
            st.dataframe(df_results.style.highlight_max(axis=0, subset=['accuracy', 'precision', 'recall', 'f1_score']), use_container_width=True)
            
            # Visualisation
            st.subheader("Graphique de Comparaison des Métriques")
            
            metrics_to_plot = ['accuracy', 'precision', 'recall', 'f1_score']
            df_plot = df_results[metrics_to_plot].reset_index().melt(id_vars='Model', var_name='Metric', value_name='Score')
            
            fig = px.bar(df_plot, x='Model', y='Score', color='Metric', barmode='group',
                         title="Comparaison des Scores de Performance des Modèles",
                         height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            st.success("🎉 Comparaison terminée. Les modèles entraînés sont sauvegardés dans le dossier `models/`.")
            
            # Afficher la matrice de confusion du meilleur modèle (par accuracy)
            best_model_name = df_results['accuracy'].idxmax()
            best_model_metrics = next(item for item in results if item["Model"] == best_model_name)
            
            st.subheader(f"Matrice de Confusion pour le Meilleur Modèle: {best_model_name}")
            cm = np.array(best_model_metrics['confusion_matrix'])
            
            fig_cm = plt.figure(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                        xticklabels=QUALITY_MAP.values(), yticklabels=QUALITY_MAP.values())
            plt.ylabel('Vraie Classe')
            plt.xlabel('Classe Prédite')
            st.pyplot(fig_cm)

def prediction_page():
    st.title("🔮 Prédiction en Temps Réel")
    st.markdown("---")
    
    models_status = get_models()
    if not models_status or not models_status['trained']:
        st.warning("Veuillez d'abord entraîner et sauvegarder des modèles sur la page 'Apprentissage'.")
        return
        
    trained_models = models_status['trained']
    
    st.subheader("1. Sélection du Modèle")
    selected_model = st.selectbox("Choisissez le modèle à utiliser pour la prédiction:", trained_models)
    
    st.subheader("2. Entrée des Données")
    
    input_type = st.radio("Méthode d'entrée des données:", ["Entrée Manuelle", "Charger un Fichier CSV"])
    
    features_input = None
    
    if input_type == "Entrée Manuelle":
        st.markdown("Entrez les valeurs des capteurs (les valeurs seront normalisées par l'API avant la prédiction):")
        
        cols = st.columns(3)
        input_values = {}
        
        for i, feature in enumerate(FEATURES):
            with cols[i % 3]:
                # Utiliser des valeurs par défaut réalistes pour les démonstrations
                default_value = 0.0
                if feature == 'Temperature': default_value = 25.0
                elif feature == 'Humidity': default_value = 60.0
                elif feature == 'PM2.5': default_value = 15.0
                elif feature == 'PM10': default_value = 30.0
                elif feature == 'NO2': default_value = 20.0
                elif feature == 'SO2': default_value = 10.0
                elif feature == 'CO': default_value = 1.5
                elif feature == 'Proximite_zones_industrielles': default_value = 5.0
                elif feature == 'Densite_population': default_value = 500.0
                
                input_values[feature] = st.number_input(feature, value=default_value, format="%.1f")
        
        features_input = [input_values[f] for f in FEATURES]
        
    elif input_type == "Charger un Fichier CSV":
        uploaded_file = st.file_uploader("Chargez un fichier CSV avec les colonnes suivantes:", type=['csv'])
        st.info(f"Colonnes attendues: {', '.join(FEATURES)}")
        
        if uploaded_file is not None:
            try:
                df_upload = pd.read_csv(uploaded_file)
                
                # Vérifier si toutes les colonnes requises sont présentes
                missing_cols = [col for col in FEATURES if col not in df_upload.columns]
                if missing_cols:
                    st.error(f"Le fichier CSV est incomplet. Colonnes manquantes: {', '.join(missing_cols)}")
                    return
                
                st.dataframe(df_upload.head())
                
                # Utiliser la première ligne pour la prédiction
                features_input = df_upload[FEATURES].iloc[0].tolist()
                st.info("La prédiction sera effectuée sur la première ligne du fichier.")
                
            except Exception as e:
                st.error(f"Erreur lors de la lecture du fichier CSV: {e}")
                return

    st.markdown("---")
    
    if features_input and st.button(f"✨ Prédire la Qualité de l'Air avec {selected_model}"):
        
        with st.spinner(f"Prédiction en cours avec {selected_model}..."):
            prediction_result = predict_data(selected_model, features_input)
            
            if prediction_result and 'prediction_label' in prediction_result:
                
                predicted_label = prediction_result['prediction_label']
                
                st.subheader("3. Résultat de la Prédiction")
                
                color = QUALITY_COLORS.get(predicted_label, '#333333')
                
                st.markdown(f"""
                <div style="padding: 20px; border-radius: 10px; background-color: {color}; color: white; text-align: center;">
                    <h1 style="color: white;">Qualité de l'Air Prédite : {predicted_label}</h1>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"**Code de Prédiction:** {prediction_result['prediction_code']}")
                st.markdown(f"**Modèle Utilisé:** {prediction_result['model_name']}")
                
                st.markdown("---")
                st.subheader("Données Soumises")
                
                data_submitted = pd.DataFrame([features_input], columns=FEATURES).T
                data_submitted.columns = ['Valeur']
                st.dataframe(data_submitted)
                
            else:
                st.error("Échec de la prédiction. Vérifiez les logs du backend.")

# --- Navigation Principale ---

def main():
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.radio("Choisir une section:", 
                            ["🏠 Accueil", 
                             "🧠 Apprentissage et Comparaison", 
                             "🔮 Prédiction en Temps Réel"])
    
    if page == "🏠 Accueil":
        home_page()
    elif page == "🧠 Apprentissage et Comparaison":
        training_page()
    elif page == "🔮 Prédiction en Temps Réel":
        prediction_page()

if __name__ == "__main__":
    main()
