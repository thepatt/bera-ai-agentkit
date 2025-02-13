import json
from .web3_connection import web3  # Import the established Web3 connection


def get_transaction(tx_hash):
    try:
        tx = web3.eth.get_transaction(tx_hash)
        tx_dict = dict(tx)
        friendly_output = json.dumps(tx_dict, indent=2, default=str)
        return f"Transaction {tx_hash} details:\n{friendly_output}"
    except Exception as e:
        return f"Error retrieving transaction details: {e}"
