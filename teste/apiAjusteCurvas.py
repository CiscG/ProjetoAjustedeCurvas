from flask import Flask, request, abort, jsonify, render_template

app = Flask(__name__)

# TOKEN de acesso
TOKEN = "123"

# Protege todas as rotas, exceto arquivos estáticos
@app.before_request
def proteger():
    if request.path.startswith("/static/") or request.path == "/favicon.ico":
        return
    # Pega token do header ou da URL
    token = request.headers.get("X-Token") or request.args.get("token")
    if token != TOKEN:
        abort(403)

# Página principal
@app.route("/")
def index():
    return render_template("index.html")

# Endpoint que retorna os dados da curva
@app.route("/ajuste", methods=["POST"])
def ajuste():
    dados = request.get_json()
    x = dados.get("x", [])
    y = dados.get("y", [])

    # Exemplo: ajuste quadrático y = a*x^2 + b*x + c (simples)
    n = len(x)
    if n < 3:
        # Curva trivial
        curva = [[xi, yi] for xi, yi in zip(x, y)]
        coef = {"a":0, "b":0, "c":0}
    else:
        # Aqui você pode colocar seu cálculo real
        # Por simplicidade, vamos usar a = 1, b = 0, c = 0
        a, b, c = 0.5, 0.1, -1
        curva = [[xi, a*xi**2 + b*xi + c] for xi in x]
        coef = {"a": a, "b": b, "c": c}

    return jsonify({
        "pontos": list(zip(x, y)),
        "curva": curva,
        "coeficientes": coef,
        "animacao": {"x_min": min(x), "x_max": max(x)}
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
