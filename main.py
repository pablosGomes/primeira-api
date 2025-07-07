from flask import Flask, request, jsonify

app = Flask(__name__)
chamados = []

@app.route("/chamados", methods=["POST"])
def cadastrar_chamado():
    data = request.get_json()
    chamado = {
        "id": len(chamados),
        "cliente": "LINX",
        "fornecedor": "ENG",
        "serviço": data.get("serviço", "").upper(),
        "problema": data.get("problema", ""),
        "resolvido": False
    }
    chamados.append(chamado)
    return jsonify({"mensagem": "Chamado registrado com sucesso!", "chamado": chamado}), 201


@app.route("/chamados", methods=["GET"])
def listar_chamados():
    servico = request.args.get("servico", "").upper()
    filtrar_resolvido = request.args.get("pendente", "false").lower() == "true"

    resultado = [
        c for c in chamados
        if (not filtrar_resolvido or not c["resolvido"])
        and (not servico or c["serviço"] == servico)
    ]
    return jsonify(resultado)


@app.route("/chamados/<int:chamado_id>/resolver", methods=["PUT"])
def resolver_chamado(chamado_id):
    if 0 <= chamado_id < len(chamados):
        chamados[chamado_id]["resolvido"] = True
        return jsonify({"mensagem": "Chamado resolvido com sucesso!"})
    else:
        return jsonify({"erro": "ID de chamado inválido!"}), 404


if __name__ == "__main__":
    app.run(debug=True)
