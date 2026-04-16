import os
import json
import numpy as np
from flask import Flask, render_template, jsonify, request, abort

app = Flask(__name__)
TOKEN = "123"

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")

@app.route("/")
def index():
    return render_template("index.html", arquivo_json=None)

@app.route("/plot/<nome_json>")
def plot(nome_json):
    return render_template(
        "index.html",
        arquivo_json=f"/data/{nome_json}.json?token={TOKEN}"
    )

@app.route("/lista_json")
def lista_json():
    if not os.path.exists(DATA_FOLDER):
        return jsonify([])

    arquivos = [
        f.replace(".json", "")
        for f in os.listdir(DATA_FOLDER)
        if f.endswith(".json")
    ]

    return jsonify(arquivos)

#@app.before_request
#def proteger():
#    if request.path.startswith("/static") or request.path in ["/lista_json"]:
#        return
#
#    token = request.args.get("token")
#    if token != TOKEN:
#        abort(403)


@app.route("/data/<nome_json>.json")
def get_json(nome_json):
    caminho = os.path.join(DATA_FOLDER, f"{nome_json}.json")

    with open(caminho) as f:
        dados = json.load(f)

    return calcular(dados)

@app.route("/data_temp", methods=["POST"])
def data_temp():
    dados = request.json
    return calcular(dados)

def calcular(dados):
    x = np.array(dados["x"])
    y = np.array(dados["y"])

    coef = np.polyfit(x, y, 2)

    return jsonify({
        "x": dados["x"],
        "y": dados["y"],
        "coeficientes": {
            "a": float(coef[0]),
            "b": float(coef[1]),
            "c": float(coef[2])
        }
    })

# ==========================================
# NOVA ROTA ADICIONADA: AJUSTE PURO
# ==========================================
@app.route("/api/ajuste-puro/<nome_json>")
def api_ajuste_puro(nome_json):
    caminho = os.path.join(DATA_FOLDER, f"{nome_json}.json")
    
    if not os.path.exists(caminho):
        return jsonify({"error": "Arquivo não encontrado"}), 404
        
    with open(caminho) as f:
        dados = json.load(f)
        
    # Reutiliza a função calcular original para manter a padronização
    return calcular(dados)

if __name__ == "__main__":
    app.run(debug=True)
