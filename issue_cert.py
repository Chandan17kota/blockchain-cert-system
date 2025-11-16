from web3 import Web3
import json

# --- CONFIGURATION ---
alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/jzaOkoHGaBp31VHkI9BVz"
contract_address = ("0x1f2c8cc8e4c35cd6cba0d8de7087dc2701015b44")
# 🚨 PASTE PRIVATE KEY HERE (Keep it safe!)
private_key = "6bf0e95be7835fb2627808137a49e9d8676e17304e4d45018e62c0acba4321d4"  

# Connect
w3 = Web3(Web3.HTTPProvider(alchemy_url))
account = w3.eth.account.from_key(private_key)
my_address = account.address  # Derives your public address from private key

# Address Safety Fix
contract_address = w3.to_checksum_address(contract_address)

# ABI (Same as before - Compact version)
contract_abi = [
	{
		"inputs": [{"internalType": "string","name": "_name","type": "string"},{"internalType": "string","name": "_course","type": "string"},{"internalType": "string","name": "_date","type": "string"}],
		"name": "issueCertificate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	}
]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# --- THE DATA TO WRITE ---
# --- OLD HARDCODED DATA ---
# student_name = "Bob" ...

# --- NEW DYNAMIC DATA ---
print("--- 🎓 ISSUE NEW CERTIFICATE ---")
student_name = input("Enter Student Name: ")
course_name = input("Enter Course Name: ")
issue_date = input("Enter Issue Date (YYYY-MM-DD): ")

print(f"📝 Preparing to issue certificate for {student_name}...")


# --- THE "UNDERLYING COMPLEXITY" (Transaction Build) ---

# 1. Get the Nonce (The Ticket Number)
# To prevent "replay attacks" (spending money twice), every transaction needs a unique number (0, 1, 2...).
nonce = w3.eth.get_transaction_count(my_address)

# 2. Build the Transaction Dictionary
tx = contract.functions.issueCertificate(student_name, course_name, issue_date).build_transaction({
    'chainId': 11155111,  # Sepolia ID
    'gas': 2000000,       # Max gas we are willing to use
    'gasPrice': w3.eth.gas_price, # Current market price
    'nonce': nonce,
    'from': my_address
})

# 3. Sign the Transaction (The Digital Signature)
# This uses your Private Key to mathematically seal the transaction.
signed_tx = w3.eth.account.sign_transaction(tx, private_key)

# 4. Send it to the Network
print("🚀 Sending transaction to Blockchain...")
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

# 5. Wait for Receipt (The Green Checkmark)
print(f"⏳ Waiting for confirmation... (Hash: {w3.to_hex(tx_hash)})")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("✅ Certificate ISSUED Successfully!")
print(f"Block Number: {tx_receipt.blockNumber}")