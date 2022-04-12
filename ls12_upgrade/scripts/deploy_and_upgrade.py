from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import network, Box, ProxyAdmin, TransparentUpgradeableProxy , Contract, BoxV2


def main():
    account = get_account()
    print(f"{network.show_active()}에 배포중")
    box = Box.deploy({"from":account})
    print(box.retrieve())

    proxy_admin = ProxyAdmin.deploy({"from":account}) #proxyadmin기능. 정확한건 찾아봐야 할듯
    #initializer --> Proxy constructor중 데이터에 들어가는 내용. 새로운 스마트 컨트랙으로 업그레이드 할때 상속받을 데이터
    #initializer를 쓸거면 아래 내용 살리기
    # box_encoded_initializer_function = encode_function_data(initializer=box.store,1)
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
            box.address,
            proxy_admin.address,
            box_encoded_initializer_function,
            {"from":account, "gas_limit":1000000}, # gas_limit은 옵션인듯

            ) 
    print(f"Proxy가 {proxy}에 배포되었습니다. V2로 업그레이드 가능합니다") #proxy를 통해 배포하면 업그레이드 가능하다는 얘기인듯
    proxy_box = Contract.from_abi("Box",proxy.address, Box.abi) #
    proxy_box.store(1,{"from":account})
    print(proxy_box.retrieve()) #proxy --> box로 명령호출
    ### --------- 이 윗부분 까지 있으면 proxy --> box에 호출 위임 까진 끝 ---------###
    # 이 밑으론 업그레이드 부분
    box_v2 = BoxV2.deploy({"from":account})
    upgrade_transaction = upgrade(
        account, proxy, box_v2.address , proxy_admin_contract=proxy_admin 
            )
    upgrade_transaction.wait(1)
    print("Proxy 업그레이드 됨")
    proxy_box = Contract.from_abi("BoxV2",proxy.address, BoxV2.abi)
    proxy_box.increment({"from":account})
    print(proxy_box.retrieve()) 
