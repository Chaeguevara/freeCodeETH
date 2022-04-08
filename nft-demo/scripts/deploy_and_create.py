from scripts.helpful_scripts import get_account
from brownie import SimpleCollectible

sample_token_uri = "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}" #contract주소 + asset number

def deploy_and_create():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from":account})
    tx = simple_collectible.createCollectible(sample_token_uri,{"from":account})
    tx.wait(1)
    print(f"이제 NFT를 {OPENSEA_URL.format(simple_collectible.address,simple_collectible.tokenCounter()-1)}에서 볼 수 있음")
    return simple_collectible



def main():
    deploy_and_create()