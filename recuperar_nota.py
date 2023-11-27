from flask import Flask, request, jsonify
from web3 import Web3

app = Flask(__name__)

# Configuración del contrato y web3
URL_DEL_NODO_ETH = "https://eth-sepolia.g.alchemy.com/v2/VqTlF6ORKjhjct9N0ldF_GDB92afAq9l"
DIRECCION_DEL_CONTRATO = Web3.to_checksum_address('0x8B021EF0404dAE0F566aF78B542BBD77356aF57c')
web3 = Web3(Web3.HTTPProvider(URL_DEL_NODO_ETH))

abi = [
    {
        "inputs": [
            {"internalType": "string", "name": "idExamen", "type": "string"},
            {"internalType": "string", "name": "nuevaNota", "type": "string"},
        ],
        "name": "actualizarNota",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "idExamen", "type": "string"},
            {"internalType": "string", "name": "nota", "type": "string"},
        ],
        "name": "guardarNota",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "", "type": "string"}],
        "name": "notasDeExamenes",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "string", "name": "idExamen", "type": "string"}],
        "name": "obtenerNota",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function",
    },
]
contrato = web3.eth.contract(address=DIRECCION_DEL_CONTRATO, abi=abi)

# Función para recuperar la nota de un examen
def recuperar_nota(id_examen):
    nota = contrato.functions.obtenerNota(id_examen).call()
    return nota

# Ruta para recibir solicitudes GET
@app.route('/obtener-nota', methods=['GET'])
def obtener_nota():
    # Obtener el parámetro del ID del examen desde la solicitud
    id_examen = request.args.get('id_examen')

    # Verificar si el parámetro está presente
    if id_examen is None:
        return jsonify({"error": "Parámetro 'id_examen' faltante"}), 400

    # Llamar a la función 'recuperar_nota' y devolver el resultado como JSON
    nota_recuperada = recuperar_nota(id_examen)
    return jsonify({"nota_recuperada": nota_recuperada})

# Iniciar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, port=9876)
