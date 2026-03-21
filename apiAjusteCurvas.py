import os
import json
import numpy as np
from flask import Flask, render_template, jsonify, abort, request

app = Flask(__name__)
TOKEN = "123"

# Pasta onde os JSONs estão armazenados
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")

# ------------------ Proteção com token ------------------
@app.before_request
def proteger():
    # Libera favicon e arquivos estáticos
    if request.path.startswith("/static/") or request.path == "/favicon.ico":
        return

    # Pega token da URL ou do header
    token = request.headers.get("X-Token") or request.args.get("token")
    if token != TOKEN:
        abort(403)

# ------------------ Rota raiz (opcional) ------------------
@app.route("/")
def index_root():
    return "Use /plot/nome_json?token=123 para ver a animação"
    
    # Ajuste quadrático (grau 2)
    coef = np.polyfit(x, y, 2)

    a, b, c = coef

    return jsonify({
        "coeficientes": {
            "a": float(a),
            "b": float(b),
            "c": float(c)
        },
        "animacao": {
            "x_min": float(min(x)),
            "x_max": float(max(x))
        },
        "pontos": list(zip(x.tolist(), y.tolist()))
    })

# ------------------ Rota de plotagem ------------------
@app.route("/plot/<nome_json>")
def plot_index(nome_json):
    # Verifica se o arquivo JSON existe
    caminho = os.path.join(DATA_FOLDER, f"{nome_json}.json")
    if not os.path.exists(caminho):
        abort(404, description="Arquivo de dados não encontrado")

    # Passa o caminho do JSON para o template
    return render_template("index.html", arquivo_json=f"/data/{nome_json}.json?token={TOKEN}")

# ------------------ Rota para retornar os dados JSON ------------------
@app.route("/data/<nome_json>.json")
def get_json(nome_json):
    caminho = os.path.join(DATA_FOLDER, f"{nome_json}.json")

    if not os.path.exists(caminho):
        abort(404)

    with open(caminho) as f:
        dados = json.load(f)

    x = np.array(dados["x"])
    y = np.array(dados["y"])

    # ajuste quadrático
    coef = np.polyfit(x, y, 2)
    a, b, c = coef

    return jsonify({
        "x": dados["x"],
        "y": dados["y"],
        "coeficientes": {
            "a": float(a),
            "b": float(b),
            "c": float(c)
        },
        "animacao": {
            "x_min": float(min(x)),
            "x_max": float(max(x))
        }
    })
# ------------------ Roda o Flask ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
