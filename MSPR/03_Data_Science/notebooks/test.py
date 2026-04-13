import pandas as pd
import numpy as np
import os
import xgboost as xgb
import unicodedata
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import warnings

warnings.filterwarnings('ignore')

base_path = r'c:\Users\tarek\Downloads\aliMSPR\MSPR_FINAL'

mapping_candidats = {
    'LE PEN': 'exD',
    'MACRON': 'Centre',
    'MÉLENCHON': 'exG', 'MELENCHON': 'exG', 'POUTOU': 'exG', 'ARTHAUD': 'exG',
    'HAMON': 'G',
    'FILLON': 'D', 'DUPONT-AIGNAN': 'D', 'LASSALLE': 'D'
}
def get_bord(nom):
    for k, v in mapping_candidats.items():
        if k in nom: return v
    return 'Autre'

# 1. CHARGEMENT DE LA BASE DE DONNÉES GLOBALE (PHASE III)
print("📥 PHASE III : Ingestion de la base de données globale...")
fichier_global = os.path.join(base_path, 'MSPR', '01_Donnees', 'data_nouvelle_aquitaine_final.csv')
df = pd.read_csv(fichier_global, low_memory=False)

# NORMALISATION DES DÉPARTEMENTS (fusion des doublons comme GIRONDE / Gironde)
df['Libellé du département'] = df['Libellé du département'].apply(
    lambda x: unicodedata.normalize('NFKD', str(x)).encode('ascii', 'ignore').decode('utf-8').upper().replace('LOT ET GARONNE', 'LOT-ET-GARONNE')
)

print(f"Lignes ingérées : {df.shape[0]}")

# 2. FEATURE ENGINEERING
print("\n⚙️ Feature Engineering en cours...")

df['P22_POP'] = df['P22_POP'].replace(0, np.nan) 

df['ratio_chomage'] = df['P22_CHOM1564'] / df['P22_POP']
df['ratio_revenus'] = df['Q216'] / df['PIMPOT16']
df['taux_delinq_taux1000'] = df['tauxpourmille'] / 1000
df['pression_delinquance'] = df['nombre'] / df['P22_POP'] # Utilisation de 'nombre' issu de la BDD Globale 

df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna(df.mean(numeric_only=True), inplace=True)

# 3. PRÉPARATION DES DONNÉES POUR LES MODÈLES
features = [
    'ratio_chomage', 
    'ratio_revenus', 
    'taux_delinq_taux1000', 
    'pression_delinquance',
    'P16_NSCOL15P_BAC',  
    'P16_NSCOL15P_SUP',  
    'nombre',            
    'tauxpourmille'      
]

X = df[features].copy()
y = df['vainqueur_nom'].fillna('MACRON') 

le = LabelEncoder()
y_encoded = le.fit_transform(y)
classes = le.classes_

print(f"🎯 Nouveaux Classes cibles (Personnalité) : {classes}")

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# 4. ENTRAÎNEMENT DES 4 MODÈLES IA
print("\n🤖 Entraînement du modèle Extreme Gradient Boosting (XGBoost)...")
model_xgb = xgb.XGBClassifier(
    objective='multi:softprob', num_class=len(classes),
    max_depth=6, learning_rate=0.1, n_estimators=300,
    subsample=0.8, colsample_bytree=0.8,
    eval_metric='mlogloss', random_state=42
)
model_xgb.fit(X_train, y_train)

print("🌲 Entraînement du modèle Random Forest...")
model_rf = RandomForestClassifier(n_estimators=300, max_depth=10, random_state=42)
model_rf.fit(X_train, y_train)

print("📈 Entraînement du modèle Gradient Boosting Classifier...")
model_gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
model_gb.fit(X_train, y_train)

print("📉 Entraînement du modèle Régression Logistique...")
model_lr = LogisticRegression(max_iter=1000, random_state=42, multi_class='multinomial')
model_lr.fit(X_train, y_train)

# 5. ÉVALUATION ET SÉLECTION DU MEILLEUR MODÈLE
y_pred_xgb = model_xgb.predict(X_test)
acc_xgb = accuracy_score(y_test, y_pred_xgb)

y_pred_rf = model_rf.predict(X_test)
acc_rf = accuracy_score(y_test, y_pred_rf)

y_pred_gb = model_gb.predict(X_test)
acc_gb = accuracy_score(y_test, y_pred_gb)

y_pred_lr = model_lr.predict(X_test)
acc_lr = accuracy_score(y_test, y_pred_lr)

print("\n" + "-" * 50)
print(f"✅ Accuracy XGBoost              : {acc_xgb * 100:.2f} %")
print(f"✅ Accuracy Random Forest        : {acc_rf * 100:.2f} %")
print(f"✅ Accuracy Gradient Boosting    : {acc_gb * 100:.2f} %")
print(f"✅ Accuracy Logistic Regression  : {acc_lr * 100:.2f} %")
print("-" * 50)

# Sélection dynamique du meilleur modèle
models_list = [
    ("XGBoost", model_xgb, y_pred_xgb, acc_xgb),
    ("Random Forest", model_rf, y_pred_rf, acc_rf),
    ("Gradient Boosting", model_gb, y_pred_gb, acc_gb),
    ("Logistic Regression", model_lr, y_pred_lr, acc_lr)
]

best_name, best_model, best_pred, best_acc = max(models_list, key=lambda item: item[3])

print(f"\n🏆 Le meilleur modèle sélectionné pour les prédictions est : {best_name} ({best_acc * 100:.2f} %)")

print(f"\nMatrice de Confusion ({best_name}) :")
print(classification_report(y_test, best_pred, target_names=classes, zero_division=0))

# 6. PRÉDICTIONS GÉOGRAPHIQUES EXACTES AVEC LE MEILLEUR MODÈLE
best_model.fit(X, y_encoded) # Entraîner le meilleur modèle sur l'exhaustif pour les prédictions finales

# Fonction de normalisation pour la comparaison (sans accents)
def normalize_str(s):
    if pd.isna(s): return ''
    return unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode('utf-8').upper()

villes_cibles = ['BORDEAUX', 'LIMOGES', 'POITIERS', 'PAU', 'LA ROCHELLE', 'MERIGNAC', 'PESSAC', 'NIORT', 'BAYONNE', 'BRIVE-LA-GAILLARDE']

print("\n" + "=" * 50)
print(f"📊 NIVEAU 1 : LOCALITÉS / CANTONS (Top 10 Villes) | par {best_name}")
print("=" * 50)

col_localite = 'Libellé du canton' if 'Libellé du canton' in df.columns else 'Libellé de la commune'
df['localite_norm'] = df[col_localite].apply(normalize_str)

for ville in villes_cibles:
    try:
        # Recherche souple SANS accent
        ville_data = df[df['localite_norm'].str.contains(ville.upper(), na=False)]
        
        if not ville_data.empty:
            features_ville = ville_data[features].mean().to_frame().T
            pred_idx = best_model.predict(features_ville)[0]
            winner_name = classes[pred_idx]
            bord_name = get_bord(winner_name)
            
            vrai_gagnants = ville_data['vainqueur_nom'].value_counts()
            vrai_gagnant_nom = vrai_gagnants.index[0] if not vrai_gagnants.empty else 'N/A'
            
            print(f"📍 Commune : {ville.ljust(20)} -> IA prédit : {winner_name.ljust(12)} [{bord_name.ljust(6)}] (Vainqueur des urnes : {vrai_gagnant_nom})")
        else:
            print(f"📍 Commune : {ville.ljust(20)} -> (Aucun résultat trouvé dans la base pour ce nom)")
    except Exception as e:
        print(f"📍 Commune : {ville.ljust(20)} -> (Erreur: {e})")

print("\n" + "=" * 50)
print(f"📊 NIVEAU 2 : DÉPARTEMENTS (" + str(len(df['Libellé du département'].unique())) + f" dép. de Nouvelle-Aquitaine) | par {best_name}")
print("=" * 50)

col_dep = 'Libellé du département'

for dep in sorted(df[col_dep].dropna().unique()):
    dep_data = df[df[col_dep] == dep]
    features_dep = dep_data[features].mean().to_frame().T
    
    pred_idx_dep = best_model.predict(features_dep)[0]
    winner_dep_name = classes[pred_idx_dep]
    bord_dep = get_bord(winner_dep_name)
    
    vrai_gagnants = dep_data['vainqueur_nom'].value_counts()
    vrai_gagnant_nom = vrai_gagnants.index[0] if not vrai_gagnants.empty else 'N/A'
    
    print(f"🗺️ Dép. : {str(dep).upper().ljust(25)} -> IA prédit : {winner_dep_name.ljust(12)} [{bord_dep.ljust(6)}] (Vainqueur des urnes : {vrai_gagnant_nom.ljust(10)})")

print("\n" + "=" * 50)
print(f"📊 NIVEAU 3 : RÉGION NOUVELLE-AQUITAINE | par {best_name}")
print("=" * 50)

region_features = df[features].mean().to_frame().T
pred_idx_reg = best_model.predict(region_features)[0]
winner_reg_name = classes[pred_idx_reg]
bord_reg = get_bord(winner_reg_name)

vrai_gagnant_reg_name = df['vainqueur_nom'].value_counts().index[0]

print(f"🇫🇷 N-AQUITAINE GLOBALE -> PRÉDICTION IA : {winner_reg_name.upper()} [{bord_reg}]  (Gagnant réel global : {vrai_gagnant_reg_name.upper()})")
print("=" * 50)