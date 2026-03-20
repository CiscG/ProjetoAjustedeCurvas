from flask import Flask, request, abort, jsonify, render_template

app = Flask(__name__)
TOKEN = "123"

# Proteção
@app.before_request
def proteger():
    if request.path.startswith("/static/") or request.path == "/favicon.ico":
        return
    token = request.headers.get("X-Token") or request.args.get("token")
    if token != TOKEN:
        abort(403)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ajuste", methods=["POST"])
def ajuste():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"error": "JSON inválido"}), 400

        x = dados.get("x")
        y = dados.get("y")

        if not isinstance(x, list) or not isinstance(y, list):
            return jsonify({"error": "x e y devem ser listas"}), 400

        if len(x) != len(y):
            return jsonify({"error": "x e y devem ter o mesmo tamanho"}), 400

        # Exemplo de ajuste quadrático
        a, b, c = 0.5, 0.1, -1
        curva = [[xi, a*xi**2 + b*xi + c] for xi in x]
        coef = {"a": a, "b": b, "c": c}

        return jsonify({
            "pontos": list(zip(x, y)),
            "curva": curva,
            "coeficientes": coef,
            "animacao": {"x_min": min(x), "x_max": max(x)}
        })

    except Exception as e:
        # Nunca retorna 500 para o cliente, só informa o erro
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
