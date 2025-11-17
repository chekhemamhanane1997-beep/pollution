import os
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# --- Configuration ---
app = Flask(__name__)
DATA_PATH = '../data/pollution.csv'
MODELS_DIR = '../models'
os.makedirs(MODELS_DIR, exist_ok=True)

# Liste des modèles disponibles
MODELS = {
    'KNN': KNeighborsClassifier(),
    'DecisionTree': DecisionTreeClassifier(random_state=42),
    'RandomForest': RandomForestClassifier(random_state=42),
    'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
    'SVM': SVC(random_state=42),
    'NaiveBayes': GaussianNB()
}

# Variables globales pour les données et le scaler
X_train, X_test, y_train, y_test = None, None, None, None
scaler = None
FEATURES = ['Temperature', 'Humidity', 'PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'Proximite_zones_industrielles', 'Densite_population']
TARGET = 'Qualite_air'

# --- Fonctions de Prétraitement ---

def load_and_preprocess_data():
    """Charge, nettoie et prépare les données pour l'entraînement."""
    global X_train, X_test, y_train, y_test, scaler
    
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        return False, "Fichier de données non trouvé."

    # Nettoyage simple: Remplacer les NaN par la médiane
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col].fillna(df[col].median(), inplace=True)
            
    # Supprimer les lignes avec des valeurs aberrantes (simplement pour éviter les erreurs d'entraînement)
    # Dans un vrai projet, on ferait un traitement plus sophistiqué
    df = df[(df[FEATURES] > -1000).all(axis=1)]
    
    X = df[FEATURES]
    y = df[TARGET]
    
    # Séparation des données
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Mise à l'échelle
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_raw)
    X_test = scaler.transform(X_test_raw)
    
    return True, "Données chargées et prétraitées avec succès."

# Charger les données au démarrage de l'API
success, message = load_and_preprocess_data()
if not success:
    print(f"Erreur au chargement des données: {message}")
    exit()

# --- API Endpoints ---

@app.route('/models', methods=['GET'])
def list_models():
    """Liste les modèles disponibles (entraînés et non entraînés)."""
    trained_models = [f.replace('.pkl', '') for f in os.listdir(MODELS_DIR) if f.endswith('.pkl')]
    available_models = list(MODELS.keys())
    
    status = {
        'trained': trained_models,
        'available_for_training': available_models
    }
    return jsonify(status)

@app.route('/train', methods=['POST'])
def train_model():
    """Entraîne un modèle spécifié et le sauvegarde."""
    if X_train is None:
        return jsonify({"error": "Données non chargées. Redémarrez l'API."}), 500
        
    data = request.get_json()
    model_name = data.get('model_name')
    
    if model_name not in MODELS:
        return jsonify({"error": f"Modèle '{model_name}' non supporté."}), 400
        
    try:
        model = MODELS[model_name]
        model.fit(X_train, y_train)
        
        # Évaluation
        y_pred = model.predict(X_test)
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='weighted', zero_division=0),
            'recall': recall_score(y_test, y_pred, average='weighted', zero_division=0),
            'f1_score': f1_score(y_test, y_pred, average='weighted', zero_division=0),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        # Sauvegarde du modèle
        model_path = os.path.join(MODELS_DIR, f'{model_name}.pkl')
        joblib.dump(model, model_path)
        
        return jsonify({
            "message": f"Modèle '{model_name}' entraîné et sauvegardé avec succès.",
            "metrics": metrics
        })
        
    except Exception as e:
        return jsonify({"error": f"Erreur lors de l'entraînement du modèle: {str(e)}"}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Effectue une prédiction avec un modèle sauvegardé."""
    data = request.get_json()
    model_name = data.get('model_name')
    features_data = data.get('features') # Doit être une liste de valeurs
    
    if not model_name or not features_data:
        return jsonify({"error": "Nom du modèle et données de caractéristiques (features) requis."}), 400
        
    model_path = os.path.join(MODELS_DIR, f'{model_name}.pkl')
    if not os.path.exists(model_path):
        return jsonify({"error": f"Modèle '{model_name}' non trouvé. Veuillez l'entraîner d'abord."}), 404
        
    try:
        # Charger le modèle
        model = joblib.load(model_path)
        
        # Préparer les données pour la prédiction
        # features_data doit être une liste de 9 valeurs correspondant à FEATURES
        if len(features_data) != len(FEATURES):
            return jsonify({"error": f"Nombre incorrect de caractéristiques. Attendu: {len(FEATURES)}, Reçu: {len(features_data)}."}), 400
            
        input_df = pd.DataFrame([features_data], columns=FEATURES)
        
        # Mise à l'échelle des données d'entrée
        scaled_input = scaler.transform(input_df)
        
        # Prédiction
        prediction = model.predict(scaled_input)[0]
        
        # Mapping de la prédiction
        quality_map = {0: 'Bonne', 1: 'Modérée', 2: 'Mauvaise', 3: 'Dangereuse'}
        predicted_label = quality_map.get(prediction, "Inconnu")
        
        return jsonify({
            "model_name": model_name,
            "prediction_code": int(prediction),
            "prediction_label": predicted_label,
            "features_used": FEATURES
        })
        
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la prédiction: {str(e)}"}), 500

if __name__ == '__main__':
    # Pour le déploiement, il est préférable d'utiliser un serveur WSGI comme Gunicorn
    # Pour ce projet, nous utilisons le serveur de développement Flask
    app.run(debug=True, host='0.0.0.0', port=5000)
