from scripts.helpful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time


def deploy_lottery():
    print("Deploy lottery!!")
    account= get_account() #로컬에ㅈ 정의된 id또는 index를 넣는다.
    # deploy를 각 환경에 따라 달리 설정
    # 컨스트럭터에 5개의 아규먼트 필요 + 주소 + publish_source
    print(account)
    print(config["networks"][network.show_active()].get("verify",False))
    lottery= Lottery.deploy(
            get_contract("eth_usd_price_feed").address,
            get_contract("vrf_coordinator").address,
            get_contract("link_token").address,
            config["networks"][network.show_active()]["fee"],
            config["networks"][network.show_active()]["keyhash"],
            {"from":account},
            publish_source=config["networks"][network.show_active()].get("verify",False)
    )
    print("Lottery Deployed!!")
    return lottery


def start_lottery():
    account=get_account()
    lottery = Lottery[-1] #Latest 
    starting_tx = lottery.startLottery({"from":account})
    starting_tx.wait(1)
    print("The Lottery is started!!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000 #fail safe. 미니멈 값에 아주 소량 추가
    tx = lottery.enter({"from":account, "value":value})
    tx.wait(1)
    print("You entered lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from":account})
    ending_transaction.wait(1)
    time.sleep(60) #random 계산될때까지 대기
    print(f"{lottery.recentWinner()} is the new winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
