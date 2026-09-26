import os
# pyrefly: ignore [missing-import]
from flask import Flask, jsonify
from flask_cors import CORS
from Controller.RotasObjetoP import criar_rotasP
from Controller.RotasObjetoA import criar_rotasA
from Model.Database import inicializar_banco

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
    return jsonify({'status': 'healthy'}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
