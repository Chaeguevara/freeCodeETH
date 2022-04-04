from scripts.helpful_scripts import get_account
from brownie import OurToken
from web3 import Web3


initial_supply = Web3.toWei(1000,"ether")

def deploy_erc20():
    print("hi")
    account = get_account()
    erc20 = OurToken.deploy(initial_supply,{"from":account})
    latestErc = OurToken[-1]
    print(latestErc.balanceOf(account))


def main():
    deploy_erc20()

