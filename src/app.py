from flask import Flask, request, jsonify
from calculadora import calcula_preco_final

app = Flask(__name__)


@app.route("/calc", methods=["GET"])
def calc():
    try:
        preco = float(request.args["preco"])
        desconto = int(request.args["desconto"])
        aliquota = float(request.args["aliquota"])
    except (KeyError, ValueError):
        return jsonify(erro="parâmetros inválidos ou ausentes"), 400

    try:
        resultado = calcula_preco_final(preco, desconto, aliquota)
    except ValueError as e:
        return jsonify(erro=str(e)), 400

    return jsonify(resultado=resultado)


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
