import os
# pyrefly: ignore [missing-import]
from flask import Flask, jsonify
from flask_cors import CORS
from Controller.RotasObjetoP import criar_rotasP
from Controller.RotasObjetoA import criar_rotasA
from Model.Database import inicializar_banco, verificar_conexao_BD

app = Flask(__name__, static_folder='View', static_url_path='')
CORS(app)
inicializar_banco()
criar_rotasP(app)
criar_rotasA(app)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/health')
def health():
    db_conectado = verificar_conexao_BD()
    status_db = "connected" if db_conectado else "disconnected"
    codigo_http = 200 if db_conectado else 503

    return jsonify({
        'status': 'healthy' if db_conectado else 'unhealthy',
        'database': status_db
    }), codigo_http


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
