import os
import json
from flask import Flask, render_template, jsonify, abort, request

app = Flask(__name__)
TOKEN = "123"

# Pasta onde os JSONs estão armazenados
DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")

# ------------------ Proteção com token ------------------
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
    return "Use /plot/nome_json?token=123 para ver a animação"

# ------------------ Rota de plotagem ------------------
@app.route("/plot/<nome_json>")
def plot_index(nome_json):
    caminho = os.path.join(DATA_FOLDER, f"{nome_json}.json")
    if not os.path.exists(caminho):
        abort(404, description="Arquivo de dados não encontrado")

    return render_template(
        "index.html",
        arquivo_json=f"/data/{nome_json}.json?token={TOKEN}"
    )

# ------------------ Rota para retornar JSON ------------------
@app.route("/data/<nome_json>.json")
def get_json(nome_json):
    caminho = os.path.join(DATA_FOLDER, f"{nome_json}.json")
    if not os.path.exists(caminho):
        abort(404, description="Arquivo de dados não encontrado")

    with open(caminho, "r") as f:
        dados = json.load(f)

    return jsonify(dados)

# ------------------ 🔥 NOVA ROTA: AJUSTE ------------------
@app.route("/ajuste", methods=["POST"])
def ajuste():
    try:
        dados = request.get_json()

        x = dados.get("x")
        y = dados.get("y")

        if not x or not y:
            return jsonify({"error": "Dados inválidos"}), 400

        # 👉 Aqui você pode depois colocar cálculo real
        a, b, c = 0.5, 0.1, -1

        return jsonify({
            "pontos": list(zip(x, y)),
            "coeficientes": {"a": a, "b": b, "c": c},
            "animacao": {
                "x_min": min(x),
                "x_max": max(x)
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ------------------ Roda o Flask ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
