from brownie import network,config,accounts
import eth_utils


LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat","development","ganache","mainnet-fork"]


    
def get_account(index=None,id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


# box.store, 1 --> byte코드로 변환 시켜서 읽을 수 있도록 만들어 줌
def encode_function_data(initializer=None,*args):
    if not len(args): args=b''

    if initializer: return initializer.encode_input(*args)

    return b''


def upgrade(
    account,
    proxy, #어떤 proxy를 업그레이드 할지
    new_implementation_address, # 새 주소
    proxy_admin_contract=None, #admin
    initializer=None,
    *args
    ):
    transaction = None
    if proxy_admin_contract:
        #업그레이드 두가지 방식
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy_admin_contract.upgradeAndCall(
                proxy.address,
                new_implementation_address,
                encode_function_data,
                {"from":account},
            )
        else:
            transaction = proxy_admin_contract.upgrade(
                    proxy.address,
                    new_implementation_address,
                    {"from":account},
            )
    else:
        if initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            transaction = proxy.upgradeToAndCall(
                    new_implementation_address,
                    encoded_function_call,
                    {"from":account}
            ) 
        else:
            transaction = proxy.upgradeTo(new_implementation_address,{"from":account})
    return transaction
