from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import Box, ProxyAdmin , TransparentUpgradeableProxy, Contract, BoxV2


def test_proxy_delegates_calls():
    account = get_account()
    box = Box.deploy({"from":account})
    proxy_admin = ProxyAdmin.deploy({"from":account})
    box_encoded_intializer_function =  encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
            box.address,
            proxy_admin.address,
            box_encoded_intializer_function,
            {"from":account, "gas_limit":1000000},
    )
    proxy_box = Contract.from_abi("Box",proxy.address, Box.abi)
    assert proxy_box.retrieve() == 0
    box_v2 = BoxV2.deploy({"from":account})
    upgrade_transaction = upgrade(
       account, proxy, box_v2.address, proxy_admin_contract=proxy_admin     
            )
    upgrade_transaction.wait(1)
    proxy_box = Contract.from_abi("BoxV2",proxy.address, BoxV2.abi)
    proxy_box.increment({"from":account})
    assert proxy_box.retrieve() == 1
