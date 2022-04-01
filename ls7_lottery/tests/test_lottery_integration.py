#TestNet과 통합이 잘 되는지 테스트
import time

import pytest
from brownie import network
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_scripts import (LOCAL_BLOCKCHAIN_ENVIRONMENTS,
                                     fund_with_link, get_account)


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()    
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value":lottery.getEntranceFee()})
    lottery.enter({"from":account, "value":lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from":account})
    time.sleep(180) #여기서는 진짜 linknode 사용
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    #brownie test -k test_can_pick_winner --network rinkeby -s "-s"는 print?
