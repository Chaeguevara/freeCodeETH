# 50달러 ETH = 0.0147 ETH(220330 현재)
# 147000000000000000 (위에 10^18)
import pytest
from brownie import Lottery, accounts, config, exceptions, network
from scripts.deploy_lottery import deploy_lottery, fund_with_link
from scripts.helpful_scripts import (LOCAL_BLOCKCHAIN_ENVIRONMENTS,
                                     fund_with_link, get_account, get_contract)
from web3 import Web3


def test_get_entrance_fee():
    #Local 에서 테스트 할때만 테스
    #brownie test -k test_get_entrance_fee --network rinkeby 로 테스트
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    #arrange
    lottery = deploy_lottery()
    #Act
    expected_entrance_fee = Web3.toWei(0.025,"ether")
    entrance_fee = lottery.getEntranceFee()
    #assert
    assert expected_entrance_fee == entrance_fee

# lottery state가OPEN이어야 시작 가능 
def test_cant_enter_unless_starter():
    #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    #시작되지 않았다면 revert
    #brownie test -k test_cant_enter_unless_starter
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from":get_account(), "value": lottery.getEntranceFee()})

# 정말 시작 가능한지 체크
# lottery.player(0) == account 인지만 본다... 이게 맞나?
# lottery.state == 1 은?? test 해보자
def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value":lottery.getEntranceFee()})
    assert lottery.players(0) == account
    # lottery state == 0 (open)인지 확인
    assert lottery.lottery_state() == 0


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from":account})
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value": lottery.getEntranceFee()})
    lottery.enter({"from":get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from":get_account(index=2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    transaction = lottery.endLottery({"from":account})
    request_id = transaction.events["RequestedRandomness"]["requestId"] # "이벤트"안의 "값"
    STATIC_RNG=777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from":account}
            ) # VRF를 작동시키는 것 처럼 simulation
    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()
    assert lottery.recentWinner() == account
    assert lottery.balance() ==0
    assert account.balance() == starting_balance_of_account + balance_of_lottery

