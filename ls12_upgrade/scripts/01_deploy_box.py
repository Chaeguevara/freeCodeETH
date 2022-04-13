from brownie import (
        Box,
        Contract, 
        ProxyAdmin, 
        TransparentUpgradeableProxy,
        network,
        config
        )

from scripts.helpful_scripts import encode_function_data, get_account


def main():
    account = get_account()
    print(f"{network.show_active()}에 배포중")
    box = Box.deploy(
            {"from":account},
            publish_source=config["networks"][network.show_active()]["verify"],    
            )
    print(box.retrieve())

    proxy_admin = ProxyAdmin.deploy({"from":account},
            publish_source=config["networks"][network.show_active()]["verify"],    
            ) #proxyadmin기능. 정확한건 찾아봐야 할듯
    #initializer --> Proxy constructor중 데이터에 들어가는 내용. 새로운 스마트 컨트랙으로 업그레이드 할때 상속받을 데이터
    #initializer를 쓸거면 아래 내용 살리기
    # box_encoded_initializer_function = encode_function_data(initializer=box.store,1)
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
            box.address,
            proxy_admin.address,
            box_encoded_initializer_function,
            {"from":account, "gas_limit":1000000}, # gas_limit은 옵션인듯
            publish_source=config["networks"][network.show_active()]["verify"],    
            ) 
    print(f"Proxy가 {proxy}에 배포되었습니다. V2로 업그레이드 가능합니다") #proxy를 통해 배포하면 업그레이드 가능하다는 얘기인듯
    proxy_box = Contract.from_abi("Box",proxy.address, Box.abi) #
    proxy_box.store(1,{"from":account})
    print(f"Proxy_box안의 최초 값은 : {proxy_box.retrieve()}") #proxy --> box로 명령호출
    ### --------- 이 윗부분 까지 있으면 proxy --> box에 호출 위임 까진 끝 ---------###
    # 이 밑으론 업그레이드 부분
