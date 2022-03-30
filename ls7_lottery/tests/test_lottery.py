# 50달러 ETH = 0.0147 ETH(220330 현재)
# 147000000000000000 (위에 10^18)
from brownie import Lottery, accounts, config, network
from web3 import Web3

def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(config["networks"][network.show_active()]["eth_usd_price_feed"],
            {"from":account})
    assert lottery.getEntranceFee() > Web3.toWei(0.0137,"ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.0177,"ether")
