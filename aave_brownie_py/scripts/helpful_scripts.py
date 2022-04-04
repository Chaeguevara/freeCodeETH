from brownie import (
        accounts,config,network
        )

LOCAL_BLOCKCHAIN_ENVIRONMENTS=[
        "development",
        "ganache",
        "hardhat",
        "local-ganache",
        "mainnet-fork",
        ]

def get_account(index=None,id=None):
    #로컬 환경에서 구동하는 경우,계정을 가져오는 방법
    # 로컬은 다시 MOCK과 FORK로 나뉨. 어쨋든 둘다List로 계정이 저장되니까 맨 처음것만 가져옴
    
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if(network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

