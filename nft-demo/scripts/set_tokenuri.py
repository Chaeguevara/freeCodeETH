from brownie import network,AdvancedCollectible
from scripts.helpful_scripts import OPENSEA_URL, get_breed, get_account

dog_metadata_dic = {
            "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
                "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
                    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
                    }


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_collectibles =  advanced_collectible.tokenCounter() #sol에 정의된 값
    print(f"{number_of_collectibles}만큼의 TokenId를 가지고 있습니다")
    for token_id in range(number_of_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id)) #sol에 정의된 mapping
        if not advanced_collectible.tokenURI(token_id).startswith("https://"): #URI가 없다면
            print(f"{token_id}에 tokenURI를 설정합니다")
            set_tokenURI(token_id, advanced_collectible, dog_metadata_dic[breed])


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract.setTokenURI(token_id, tokenURI, {"from":account})
    tx.wait(1)
    print(
        f"멋집니다. 이제 NFT를 {OPENSEA_URL.format(nft_contract.address, token_id)}에서 확인할 수 있습니다"
            )
    print("최대 20분이 걸릴 수 있습니다")
