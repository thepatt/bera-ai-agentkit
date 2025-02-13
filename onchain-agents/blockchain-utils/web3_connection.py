from web3 import Web3

BERACHAIN_RPC_URL = "https://bartio.rpc.berachain.com/"
web3 = Web3(Web3.HTTPProvider(BERACHAIN_RPC_URL))

if web3.is_connected():
    print("Connected to Berachain!")
else:
    raise Exception("Unable to connect to Berachain.")
