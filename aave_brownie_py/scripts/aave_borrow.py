from brownie import network,config, interface
from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        #fork에선 아직 weth를 받지 않았기 때문에
        get_weth()
    #ABI + Address --> aave의 leanding pool작
    lending_pool = get_lending_pool()
    print(lending_pool)


def get_lending_pool():
    """
    AAVe 마켓별로, lending_pool주소가 다름
    """
    #ABI + Address 를 사용해야 하지만 interface로 할것임
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(
            config["networks"][network.show_active()]["lending_pool_addresses_provider"]
            )
    lending_pool_address = lending_pool_address_provider.getLendingPool()
    #이제 lending_pool_address 확인 --> ABI + address --> interface
    lending_pool = interface.ILendingPoolAddressesProvider(lending_pool_address)
    return lending_pool
