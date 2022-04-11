from scripts.helpful_scripts import get_account, OPENSEA_URL, get_contract, fund_with_link
from brownie import AdvancedCollectible, network, config


def deploy_and_create():
    account = get_account()
    #Opensea testNet은 Rinkeby만 있음
    advanced_collectible = AdvancedCollectible.deploy(
            get_contract("vrf_coordinator"),
            get_contract("link_token"),
            config["networks"][network.show_active()]["keyhash"],
            config["networks"][network.show_active()]["fee"],
            {"from":account},
            publish_source=config["networks"][network.show_active()].get("verify"), # verify
            )
    fund_with_link(advanced_collectible.address)#link를 채워 넣음 --> random 호출
    creating_tx = advanced_collectible.createCollectible({"from":account})
    creating_tx.wait(1)
    print("New token has benn created!")
    return advanced_collectible, creating_tx


def main():
    deploy_and_create()
