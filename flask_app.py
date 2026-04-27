from flask import Flask, render_template_string
import requests
import time

app = Flask(__name__)

# --- CONFIGURATION ---
# Remplacez par l'URL de l'API que vous avez choisie
API_URL = "https://api.zippopotam.us/fr/75001" 

@app.route('/')
def dashboard():
    start_time = time.time()
    status = "🔴 HORS LIGNE"
    latency = 0
    test_result = "ÉCHEC"
    
    try:
        # 1. Test de l'API
        response = requests.get(API_URL, timeout=5)
        latency = round((time.time() - start_time) * 1000, 2) # en millisecondes
        
        if response.status_code == 200:
            status = "🟢 OPÉRATIONNEL"
            # 2. Vérification de la qualité des données
            data = response.json()
            if "places" in data: # Exemple de test de structure
                test_result = "PASSÉ ✅"
            else:
                test_result = "DONNÉES INVALIDES ⚠️"
    except Exception as e:
        test_result = f"ERREUR : {str(e)}"

    # 3. Affichage (HTML simple pour le dashboard)
    html_content = f"""
    <html>
        <body style="font-family: sans-serif; text-align: center; padding: 50px;">
            <h1>Dashboard Qualité API</h1>
            <hr>
            <p><strong>Statut du service :</strong> {status}</p>
            <p><strong>Latence :</strong> {latency} ms</p>
            <p><strong>Test de conformité :</strong> {test_result}</p>
            <hr>
            <small>Dernière vérification : {time.ctime()}</small>
        </body>
    </html>
    """
    return render_template_string(html_content)
