import os
import json
import numpy as np
from flask import Flask, render_template, jsonify, abort, request

app = Flask(__name__)
TOKEN = "123"

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")

# ------------------ Proteção ------------------
@app.before_request
def proteger():
    if request.path.startswith("/static/") or request.path == "/favicon.ico":
        return

    token = request.headers.get("X-Token") or request.args.get("token")
    if token != TOKEN:
        abort(403)

# ------------------ Rota raiz ------------------
@app.route("/")
def index_root():
    return "Use /plot/nome_json?token=123"

# ------------------ Página ------------------
@app.route("/plot/<nome_json>")
def plot_index(nome_json):
    caminho = os.path.join(DATA_FOLDER, f"{nome_json}.json")

    if not os.path.exists(caminho):
        abort(404, description="Arquivo não encontrado")

    return render_template(
        "index.html",
        arquivo_json=f"/data/{nome_json}.json?token={TOKEN}"
    )

# ------------------ JSON ------------------
@app.route("/data/<nome_json>.json")
def get_json(nome_json):
    caminho = os.path.join(DATA_FOLDER, f"{nome_json}.json")

    if not os.path.exists(caminho):
        abort(404)

    with open(caminho) as f:
        dados = json.load(f)

    x = np.array(dados["x"])
    y = np.array(dados["y"])

    # ajuste quadrático (mantido, caso queira usar depois)
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

# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
