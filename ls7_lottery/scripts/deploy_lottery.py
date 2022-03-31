from scripts.helpful_scripts import get_account, get_contract
from brownie import Lottery, network, config


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


def main():
    deploy_lottery()
