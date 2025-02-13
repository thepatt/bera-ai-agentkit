from .web3_connection import web3  # Import the established Web3 connection


def get_balance(address):
    try:
        if not web3.is_address(address):
            return f"{address} is not a valid Ethereum address."
        balance = web3.eth.get_balance(address)
        balance_in_ether = web3.from_wei(balance, "ether")
        return f"The balance of {address} is {balance_in_ether} BERA."
    except Exception as e:
        return f"Error retrieving balance: {e}"
