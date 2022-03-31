from brownie import (
        accounts,config,network, MockV3Aggregator,Contract, VRFCoordinatorMock, LinkToken
        )

DECIMALS=8
INITIAL_VALUE=200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS=["development","ganache-local"]
FORKED_LOCAL_ENVIRONMENTS=["mainnet-fork","mainnet-fork-dev"]

def get_account(index=None,id=None):
    #로컬 환경에서 구동하는 경우,계정을 가져오는 방법
    # 로컬은 다시 MOCK과 FORK로 나뉨. 어쨋든 둘다List로 계정이 저장되니까 맨 처음것만 가져옴
    
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
            or network.show_active() in FORKED_LOCAL_ENVIRONMENTS):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

#contract_name에 해당하는 contract로 매핑함
contract_to_mock = {
        "eth_usd_price_feed" : MockV3Aggregator,
        "vrf_coordinator" : VRFCoordinatorMock,
        "link_token" : LinkToken,

        }

def get_contract(contract_name):
    """
        컨트랙트 이름을 받아, 현재 테스트하는 블록체인에 같은 이름의 계약이 있다면 이를 가져오고 없다면 mock contract를 배포함


    Args:
        contract_name (string)

    Returns:
        가장 최근에 배포된 계약
        ex)MockV3Aggregator[-1]

    """
    contract_type = contract_to_mock[contract_name] # dictionary
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0: #배포된 계약이 없다면
            deploy_mocks() #배포
        contract = contract_type[-1] #가장 최근 배포 버
    else: # fork 또는 TestNet,MainNet
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
    return contract    
    

def deploy_mocks(decimals=DECIMALS,initial_value=INITIAL_VALUE):
    account=get_account()
    MockV3Aggregator.deploy(
            decimals,initial_value,{"from":account}
            )
    link_token = LinkToken.deploy({"from":account}) #constructor에 아무것도 없음
    VRFCoordinatorMock.deploy(link_token.address,{"from":account})

    print("Deployed!")
