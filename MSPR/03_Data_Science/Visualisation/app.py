from flask import Flask, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# VRAIES données de votre modèle Machine Learning
# L'accuracy réelle est de 83.3% pour les départements (10/12)
# Les erreurs identifiées dans votre sortie notebook sont :
# DORDOGNE (Gagnant réel NUPES, prédit Ensemble !)
# LOT-ET-GARONNE (Gagnant réel RN, prédit Ensemble !)

RESULTS_DATA = {
    "summary": {
        "region_name": "Nouvelle-Aquitaine",
        "predicted_winner": "Ensemble !",
        "real_winner": "Ensemble !",
        "model_accuracy": 82.4,
        "dept_accuracy": 83.3,
        "target_accuracy": "80%+",
        "total_records": "50 000",
        "noise_applied": "σ=0.45",
        "label_flip": "15%"
    },
    "political_real": [
        {"party": "MACRON - Ensemble !", "count": 7, "color": "#0055A4"},
        {"party": "MÉLENCHON - NUPES", "count": 4, "color": "#E4032E"},
        {"party": "LE PEN - RN", "count": 1, "color": "#000000"}
    ],
    "political_predicted": [
        {"party": "MACRON - Ensemble !", "count": 9, "color": "#176Bc6"}, # Le modèle a surestimé Ensemble (10/12)
        {"party": "MÉLENCHON - NUPES", "count": 3, "color": "#FF4D6A"},
        {"party": "LE PEN - RN", "count": 0, "color": "#333333"}
    ],
    "levels": {
        "region": [
            {"entity": "NOUVELLE-AQUITAINE", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "Ensemble !", "real_cand": "MACRON", "is_correct": True, "conf": "85%"}
        ],
        "departement": [
            {"entity": "CHARENTE", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "Ensemble !", "real_cand": "MACRON", "is_correct": True, "conf": "82%"},
            {"entity": "CHARENTE-MARITIME", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "Ensemble !", "real_cand": "MACRON", "is_correct": True, "conf": "79%"},
            {"entity": "CORRÈZE", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "Ensemble !", "real_cand": "MACRON", "is_correct": True, "conf": "70%"},
            {"entity": "CREUSE", "predicted": "NUPES", "pred_cand": "MÉLENCHON", "real": "NUPES", "real_cand": "MÉLENCHON", "is_correct": True, "conf": "88%"},
            {"entity": "DORDOGNE", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "NUPES", "real_cand": "MÉLENCHON", "is_correct": False, "conf": "45%"},
            {"entity": "GIRONDE", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "Ensemble !", "real_cand": "MACRON", "is_correct": True, "conf": "92%"},
            {"entity": "LANDES", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "Ensemble !", "real_cand": "MACRON", "is_correct": True, "conf": "78%"},
            {"entity": "LOT-ET-GARONNE", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "RN", "real_cand": "LE PEN", "is_correct": False, "conf": "42%"},
            {"entity": "PYRÉNÉES-ATLANTIQUES", "predicted": "NUPES", "pred_cand": "MÉLENCHON", "real": "NUPES", "real_cand": "MÉLENCHON", "is_correct": True, "conf": "84%"},
            {"entity": "DEUX-SÈVRES", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "Ensemble !", "real_cand": "MACRON", "is_correct": True, "conf": "81%"},
            {"entity": "VIENNE", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "Ensemble !", "real_cand": "MACRON", "is_correct": True, "conf": "76%"},
            {"entity": "HAUTE-VIENNE", "predicted": "NUPES", "pred_cand": "MÉLENCHON", "real": "NUPES", "real_cand": "MÉLENCHON", "is_correct": True, "conf": "83%"}
        ],
        "canton": [
            {"entity": "AGEN-1", "predicted": "RN", "pred_cand": "LE PEN", "real": "N/A", "real_cand": "N/A", "is_correct": None, "conf": "72%"},
            {"entity": "ANGOULÊME-1", "predicted": "NUPES", "pred_cand": "MÉLENCHON", "real": "N/A", "real_cand": "N/A", "is_correct": None, "conf": "88%"},
            {"entity": "BORDEAUX-1", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "N/A", "real_cand": "N/A", "is_correct": None, "conf": "91%"},
            {"entity": "LIMOGES-1", "predicted": "NUPES", "pred_cand": "MÉLENCHON", "real": "N/A", "real_cand": "N/A", "is_correct": None, "conf": "85%"},
            {"entity": "PAU-1", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "N/A", "real_cand": "N/A", "is_correct": None, "conf": "80%"}
        ],
        "commune": [
            {"entity": "AGEN", "predicted": "RN", "pred_cand": "LE PEN", "real": "N/A", "real_cand": "N/A", "is_correct": None, "conf": "68%"},
            {"entity": "ANGOULÊME", "predicted": "NUPES", "pred_cand": "MÉLENCHON", "real": "N/A", "real_cand": "N/A", "is_correct": None, "conf": "84%"},
            {"entity": "BORDEAUX", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "N/A", "real_cand": "N/A", "is_correct": None, "conf": "92%"},
            {"entity": "LIMOGES", "predicted": "NUPES", "pred_cand": "MÉLENCHON", "real": "N/A", "real_cand": "N/A", "is_correct": None, "conf": "81%"},
            {"entity": "PAU", "predicted": "Ensemble !", "pred_cand": "MACRON", "real": "N/A", "real_cand": "N/A", "is_correct": None, "conf": "77%"}
        ]
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/results')
def api_results():
    return jsonify(RESULTS_DATA)

if __name__ == '__main__':
    app.run(debug=True, port=5000)