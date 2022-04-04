from scripts.helpful_scripts import get_account
from brownie import interface, config, network

def main():
    get_weth()

def get_weth():
    """
    Aave사용을 위해 WETH필요함
    Kovan 에 있는 Weth contract를 이용해서 ETH --> WETH로 변경
    이 중 deposit기능을 사용해서 변경
    """
    #ABI
    #Address 사용
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from":account, "value": 0.1 * 10 ** 18})#10^18 == 1ETH        
    tx.wait(1)
    print("Received 0.1 WETH")
    return tx
            
