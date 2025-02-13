from web3 import Web3
import json

# Connect to Berachain
BERACHAIN_RPC_URL = "https://bartio.rpc.berachain.com/"
web3 = Web3(Web3.HTTPProvider(BERACHAIN_RPC_URL))

if web3.is_connected():
    print("2.Connected to Berachain!")
else:
    raise Exception("Unable to connect to Berachain.")


def get_balance(address):
    try:
        if not web3.is_address(address):
            return f"{address} is not a valid Ethereum address."
        balance = web3.eth.get_balance(address)
        balance_in_ether = web3.from_wei(balance, "ether")
        return f"The balance of {address} is {balance_in_ether} BERA."
    except Exception as e:
        return f"Error retrieving balance: {e}"


def get_transaction(tx_hash):
    try:
        tx = web3.eth.get_transaction(tx_hash)
        tx_dict = dict(tx)
        friendly_output = json.dumps(tx_dict, indent=2, default=str)
        return f"Transaction {tx_hash} details:\n{friendly_output}"
    except Exception as e:
        return f"Error retrieving transaction details: {e}"
