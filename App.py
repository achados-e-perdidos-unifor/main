import os
# pyrefly: ignore [missing-import]
from flask import Flask, jsonify, request
from flask_cors import CORS
from Controller.RotasObjetoP import criar_rotasP
from Controller.RotasObjetoA import criar_rotasA
from Model.Database import (
    inicializar_banco,
    verificar_conexao_BD,
    registrar_crime_bd,
    obter_placar_crimes,
    zerar_crimes_bd
)

app = Flask(__name__, static_folder='View', static_url_path='')
CORS(app)
inicializar_banco()
criar_rotasP(app)
criar_rotasA(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/jogo')
def jogo():
    return app.send_static_file('jogo.html')


@app.route('/health')
def health():
    db_conectado = verificar_conexao_BD()
    status_db = "connected" if db_conectado else "disconnected"
    codigo_http = 200 if db_conectado else 503

    return jsonify({
        'status': 'healthy' if db_conectado else 'unhealthy',
        'database': status_db
    }), codigo_http


@app.route('/api/registrar_crime', methods=['POST'])
def registrar_crime():
    dados = request.get_json() or {}
    integrante = dados.get('integrante')
    crime = dados.get('crime')
    if not integrante or not crime:
        return jsonify({'mensagem': 'Dados incompletos'}), 400

    resultado = registrar_crime_bd(integrante, crime)
    if resultado:
        return jsonify({'mensagem': 'Crime registrado com sucesso'}), 201
    return jsonify({'mensagem': 'Erro ao registrar crime'}), 500


@app.route('/api/placar_crimes', methods=['GET'])
def placar_crimes():
    dados = obter_placar_crimes()
    placar = []
    for row in dados:
        placar.append({
            'integrante': row[0],
            'total': row[1],
            'ultimo_crime': row[2]
        })
    return jsonify(placar), 200


@app.route('/api/zerar_crimes', methods=['POST'])
def zerar_crimes():
    resultado = zerar_crimes_bd()
    if resultado:
        return jsonify({'mensagem': 'Ficha criminal zerada com sucesso'}), 200
    return jsonify({'mensagem': 'Erro ao zerar ficha criminal'}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
