from web3 import Web3
import json

# 1. CONNECT TO BLOCKCHAIN
# Paste your Alchemy URL here
alchemy_url = "https://eth-sepolia.g.alchemy.com/v2/jzaOkoHGaBp31VHkI9BVz"
w3 = Web3(Web3.HTTPProvider(alchemy_url))

# Check connection
if w3.is_connected():
    print("✅ Connected to Sepolia Network!")
else:
    print("❌ Connection Failed")

# 2. SETUP CONTRACT
# Paste your Contract Address from Remix (Deployed Contracts section)
# We wrap the string in this function to fix the capitalization automatically
contract_address = w3.to_checksum_address("0x1f2c8cc8e4c35cd6cba0d8de7087dc2701015b44")
# Paste the ABI you copied from Remix (Keep it as a standard string or load from file)
# For simplicity, I'll put a placeholder. Replace this list with your ACTUAL COPIED ABI.
contract_abi = [
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "bytes32",
				"name": "certHash",
				"type": "bytes32"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "name",
				"type": "string"
			}
		],
		"name": "CertificateIssued",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"name": "certificates",
		"outputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "course",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "date",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "isValid",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_course",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_date",
				"type": "string"
			}
		],
		"name": "issueCertificate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_course",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_date",
				"type": "string"
			}
		],
		"name": "verifyCertificate",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

# Create the Contract Object
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# 3. INTERACT (READ DATA)
# Let's verify the "Alice" certificate you created in Remix
# name = "Bob"
# course = "Advanced Python"
# date = "2025-05-20" # Make sure this matches EXACTLY what you wrote
# --- OLD HARDCODED DATA (DELETE THIS) ---
# name = "Bob"
# course = "Advanced Python"
# date = "2025-05-20"

# --- NEW DYNAMIC INPUT (ADD THIS) ---
print("\n--- 🔍 VERIFY A CERTIFICATE ---")
name = input("Enter Student Name to Verify: ")
course = input("Enter Course Name: ")
date = input("Enter Issue Date (YYYY-MM-DD): ")

print(f"\nChecking Blockchain for: {name}, {course}, {date}...")
# print(f"🔍 Verifying certificate for {name}...")

# Call the function (Local execution, no gas)
is_valid = contract.functions.verifyCertificate(name, course, date).call()

if is_valid:
    print("✅ Certificate is VALID and exists on the Blockchain!")
else:
    print("❌ Certificate INVALID or not found.")