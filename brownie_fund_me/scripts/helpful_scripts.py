from brownie import accounts,config,network,MockV3Aggregator
from web3 import Web3

DECIMALS=8
STARTING_PRICE=2*(10**10)
LOCAL_BLOCKCHAIN_ENVIRONMENTS=["development","ganache-local"]

def get_account():
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deply MockV3Aggregator...")
    if len(MockV3Aggregator) <= 0:
        print("deploying")
        MockV3Aggregator.deploy(DECIMALS,Web3.toWei(STARTING_PRICE,"ether"),{"from":get_account()})
    print("Mock deployed!")

    
