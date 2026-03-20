from flask import Flask, request, jsonify, send_from_directory
import numpy as np

app = Flask(__name__, static_folder="static")

# rota principal (abre o frontend)
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# rota de cálculo
@app.route("/ajuste", methods=["POST"])
def ajuste():
    dados = request.json
    
    x = np.array(dados["x"])
    y = np.array(dados["y"])
    
    n = len(x)

    # somatórios (igual sua tabela)
    Sx = np.sum(x)
    Sy = np.sum(y)
    Sx2 = np.sum(x**2)
    Sx3 = np.sum(x**3)
    Sx4 = np.sum(x**4)
    Sxy = np.sum(x*y)
    Sx2y = np.sum((x**2)*y)

    # sistema linear
    A = np.array([
        [n,   Sx,  Sx2],
        [Sx,  Sx2, Sx3],
        [Sx2, Sx3, Sx4]
    ])

    B = np.array([Sy, Sxy, Sx2y])

    # resolve sistema
    coef = np.linalg.solve(A, B)
    c, b, a = coef

    # gera pontos da curva
    x_curve = np.linspace(min(x), max(x), 100)
    y_curve = a*x_curve**2 + b*x_curve + c

    return jsonify({
        "a": float(a),
        "b": float(b),
        "c": float(c),
        "pontos": list(zip(x.tolist(), y.tolist())),
        "curva": list(zip(x_curve.tolist(), y_curve.tolist()))
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)