from brownie import network, AdvancedCollectible
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS,get_contract,get_account
from scripts.advanced_collectible.deploy_and_create import deploy_and_create

def test_can_create_advanced_collectible():
    # 배포 --> NFT 생성 --> 랜덤 종 받음
    #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("로컬 테스트 용도임")
    #actign
    advanced_collectible, creation_transaction = deploy_and_create()    
    #assert 
    #최초 생성시 토큰 카운터 값은 1
    # Random값이 들어왔는지 테스트 해봐야함
    requestId = creation_transaction.events["requestedCollectible"]["requestId"]#smart contract의 event불러오는 방
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(requestId, random_number, advanced_collectible.address, {"from":get_account()}) #VRFMock중 callBack~ 기능이 필요로 하는input들    
    #assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
