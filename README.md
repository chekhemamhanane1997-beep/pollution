# Projet 2 : Étude comparative de classification et prédiction en temps réel de la qualité de l’air

## 420-IAA-TT - Automne-2025

### Description
Ce projet vise à développer une application client-serveur pour la modélisation prédictive et la classification automatique de la qualité de l'air à partir d'un jeu de données sur la pollution. L'objectif est de concevoir, comparer et déployer plusieurs modèles de classification capables de prédire le niveau de qualité de l'air (Bonne, Modérée, Mauvaise, Dangereuse).

### Architecture
- **Backend (API):** Flask (pour la gestion des modèles, des prédictions et des fichiers).
- **Frontend (Interface Utilisateur):** Streamlit (pour la visualisation et les interactions).

### Structure du Projet

```
projet_ia_qualite_air/
├── data/
│   └── pollution.csv             # Jeu de données de pollution
├── models/
│   └── (modèles .pkl sauvegardés) # Dossier pour les modèles entraînés
├── backend/
│   └── api.py                    # Application Flask pour l'API REST
├── frontend/
│   └── app.py                    # Application Streamlit pour l'interface utilisateur
├── README.md                     # Ce fichier
└── requirements.txt              # Liste des dépendances Python
```

### Installation et Exécution

#### 1. Prérequis
Assurez-vous d'avoir Python 3.x installé.

#### 2. Installation des dépendances
```bash
pip install -r requirements.txt
```

#### 3. Lancement du Backend (API Flask)
Le backend doit être lancé en premier pour que le frontend puisse y accéder.
```bash
cd projet_ia_qualite_air/backend
python api.py
```
L'API sera disponible à l'adresse `http://127.0.0.1:5000`.

#### 4. Lancement du Frontend (Application Streamlit)
Dans un nouveau terminal, lancez l'application Streamlit.
```bash
cd projet_ia_qualite_air/frontend
streamlit run app.py
```
L'interface utilisateur sera accessible dans votre navigateur à l'adresse indiquée par Streamlit (généralement `http://localhost:8501`).

### API Endpoints

| Endpoint | Méthode | Description |
| :--- | :--- | :--- |
| `/models` | `GET` | Liste les modèles disponibles dans le dossier `models/`. |
| `/train` | `POST` | Entraîne un modèle spécifié et le sauvegarde. |
| `/predict` | `POST` | Renvoie la prédiction pour une entrée de données donnée. |

---
*Ce projet a été généré pour le cours 420-IAA-TT - Automne-2025.*
