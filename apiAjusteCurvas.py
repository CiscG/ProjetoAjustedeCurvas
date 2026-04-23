import os
import json
import numpy as np
from flask import Flask, render_template, jsonify, request, abort

app = Flask(__name__)
TOKEN = "123"

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "data")

# --- AJUSTE 1: Função Auxiliar para Formatação da Equação ---
def formatar_termo(val, sufixo, primeiro=False):
    if val == 0: return ""
    abs_val = abs(val)
    # Usa notação científica para valores muito pequenos, senão decimal fixo
    val_str = f"{abs_val:.2e}" if abs_val < 0.001 else f"{abs_val:.4f}"
    
    if primeiro:
        # O primeiro termo não precisa de espaço antes do sinal
        return f"-{val_str}{sufixo}" if val < 0 else f"{val_str}{sufixo}"
    else:
        # Termos b e c com sinais bem espaçados (evita o "+ -")
        sinal = " - " if val < 0 else " + "
        return f"{sinal}{val_str}{sufixo}"

def calcular(dados):
    try:
        x = np.array(dados["x"])
        y = np.array(dados["y"])

        # Cálculo dos coeficientes do Polinômio de 2º Grau (MQM)
        coef = np.polyfit(x, y, 2)
        a, b, c = float(coef[0]), float(coef[1]), float(coef[2])

        # Montagem da string da equação limpa
        term_a = formatar_termo(a, "x²", primeiro=True)
        term_b = formatar_termo(b, "x")
        term_c = formatar_termo(c, "")
        equacao_formatada = f"y = {term_a}{term_b}{term_c}"

        return jsonify({
            "x": dados["x"].tolist() if isinstance(dados["x"], np.ndarray) else dados["x"],
            "y": dados["y"].tolist() if isinstance(dados["y"], np.ndarray) else dados["y"],
            "coeficientes": {
                "a": a,
                "b": b,
                "c": c
            },
            "equacao": equacao_formatada
        })
    except Exception as e:
        print(f"Erro no cálculo: {e}")
        return jsonify({"error": "Falha ao processar dados", "details": str(e)}), 400

# --- ROTAS ---

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

@app.route("/data/<nome_json>.json")
def get_json(nome_json):
    caminho = os.path.join(DATA_FOLDER, f"{nome_json}.json")
    
    if not os.path.exists(caminho):
        return jsonify({"error": "Arquivo não encontrado"}), 404

    try:
        with open(caminho, 'r') as f:
            dados = json.load(f)
        return calcular(dados)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/data_temp", methods=["POST"])
def data_temp():
    dados = request.json
    if not dados:
        return jsonify({"error": "Dados inválidos"}), 400
    return calcular(dados)

@app.route("/api/ajuste-puro/<nome_json>")
def api_ajuste_puro(nome_json):
    caminho = os.path.join(DATA_FOLDER, f"{nome_json}.json")
    
    if not os.path.exists(caminho):
        return jsonify({"error": "Arquivo não encontrado"}), 404
        
    with open(caminho) as f:
        dados = json.load(f)
        
    return calcular(dados)

if __name__ == "__main__":
    # Rodando em 0.0.0.0 para ser acessível na sua rede local (casa do Chico)
    app.run(host='0.0.0.0', port=5050, debug=True)