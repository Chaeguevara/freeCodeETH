from brownie import network, AdvancedCollectible
import time
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS,get_contract,get_account
from scripts.advanced_collectible.deploy_and_create import deploy_and_create

def test_can_create_advanced_collectible_integration():
    # 배포 --> NFT 생성 --> 랜덤 종 받음
    #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("로컬 테스트 용도임")
    #actign
    advanced_collectible, creation_transaction = deploy_and_create()    
    time.sleep(180)# 튜토리얼에선 1분이지만 실제로는 그 이상인듯
    #assert
    #배포된게 하나라 1개가 될거라 뭐라뭐라
    assert advanced_collectible.tokenCounter() == 1

