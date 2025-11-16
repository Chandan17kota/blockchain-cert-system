from flask import Flask, request, jsonify
from flask_cors import CORS
from web3 import Web3
from dotenv import load_dotenv
import os

# 1. LOAD SECRETS (From .env file)
load_dotenv()

alchemy_url = os.getenv("ALCHEMY_URL")
private_key = os.getenv("PRIVATE_KEY")
contract_address = os.getenv("CONTRACT_ADDRESS")

# 2. SETUP FLASK
app = Flask(__name__)
CORS(app) # Allow the frontend to talk to us

# 3. SETUP BLOCKCHAIN CONNECTION
w3 = Web3(Web3.HTTPProvider(alchemy_url))
account = w3.eth.account.from_key(private_key)
my_address = account.address

# Ensure address is checksummed
contract_address = w3.to_checksum_address(contract_address)

# The ABI (Same as before)
contract_abi = [
	{
		"inputs": [{"internalType": "string","name": "_name","type": "string"},{"internalType": "string","name": "_course","type": "string"},{"internalType": "string","name": "_date","type": "string"}],
		"name": "issueCertificate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [{"internalType": "string","name": "_name","type": "string"},{"internalType": "string","name": "_course","type": "string"},{"internalType": "string","name": "_date","type": "string"}],
		"name": "verifyCertificate",
		"outputs": [{"internalType": "bool","name": "","type": "bool"}],
		"stateMutability": "view",
		"type": "function"
	}
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

print(f"✅ Server connected to Blockchain via: {my_address}")

# --- ROUTE 1: ISSUE CERTIFICATE (POST) ---
@app.route('/issue', methods=['POST'])
def issue_certificate():
    try:
        # Get data from the JSON request
        data = request.get_json()
        name = data['name']
        course = data['course']
        date = data['date']

        print(f"📝 Request to issue: {name}")

        # 1. Build Transaction
        nonce = w3.eth.get_transaction_count(my_address)
        tx = contract.functions.issueCertificate(name, course, date).build_transaction({
            'chainId': 11155111, # Sepolia ID
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
            'from': my_address
        })

        # 2. Sign Transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)

        # 3. Send Transaction
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        # 4. Wait for Receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        return jsonify({
            "success": True, 
            "message": f"Certificate Issued for {name}!", 
            "tx_hash": w3.to_hex(tx_hash)
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


# --- ROUTE 2: VERIFY CERTIFICATE (GET) ---
@app.route('/verify', methods=['GET'])
def verify_certificate():
    try:
        # Get parameters from URL (e.g., ?name=Bob&course=Math&date=2022)
        name = request.args.get('name')
        course = request.args.get('course')
        date = request.args.get('date')

        print(f"🔍 Verifying: {name}")

        # Call Contract (Read-only)
        is_valid = contract.functions.verifyCertificate(name, course, date).call()

        return jsonify({
            "success": True, 
            "is_valid": is_valid,
            "message": "Valid Certificate" if is_valid else "Invalid Certificate"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# Start the Server
if __name__ == '__main__':
    app.run(debug=True, port=5000)