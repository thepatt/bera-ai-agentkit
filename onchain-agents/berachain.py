from web3 import Web3

BERACHAIN_RPC_URL = "https://bartio.rpc.berachain.com/"
web3 = Web3(Web3.HTTPProvider(BERACHAIN_RPC_URL))


# def connect_to_berachain():
#     if web3.is_connected():
#         print("1.Connected to Berachain!")
#         return True
#     else:
#         raise Exception("Unable to connect to Berachain.")


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
        return f"Transaction {tx_hash} details:\n{tx}"
    except Exception as e:
        return f"Error retrieving transaction details: {e}"


def get_token_price(token_address):
    """
    Placeholder for retrieving token price from a price aggregator.
    Replace with actual contract call or external API lookup.
    """
    # Example placeholder logic:
    # aggregator = web3.eth.contract(address=some_aggregator_address, abi=some_aggregator_abi)
    # price = aggregator.functions.latestAnswer().call()
    # return f"Current price of token {token_address}: {price}"
    return f"Price retrieval not implemented for token {token_address}."



