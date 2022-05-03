
# Solidity 
[Freecodecamp 솔리디티강의](https://youtu.be/M576WGiDBdQ)를 기준으로 작성하였습니다.

## 작성자 지갑주소

[지갑주소](https://rinkeby.etherscan.io/address/0xf7575c46ea44411e5181fc2ac913f04e5dfc487c)에서 관련 스마트 컨트랙트 배포 내용 등을 확인 할 수 있습니다. 

## [AAVE](./aave_brownie_py)

aave 테스트넷을 이용하여 defi landing을 구현한 프로젝트 입니다. Solidity Interface 코드를 주로 사용합니다

## [brownie fund me](./brownie_fund_me)

smartcontract를 이용해 펀딩받는 예시를 보여줍니다. 이떄 USD <-> ETH 교환비를 위해 Chainlink pricefeed를 사용합니다 

## [brownie simple storage](./brownieSimpleStorage)

smartcontract에 값을 쓰는(write) 기본적인 코드를 보여줍니다

## [Defi stake yield](./defi-stake-yield-brownie)

 위 튜토리얼 최종 프로젝트 입니다. usedapp을 사용하는데, 몇몇 이유로 잘 작동하지 않았습니다. adblock문제거나, etherscan api를 사용하는 거 같은데 관리자측 api문제로 보입니다

## [Fund me](./Ls3_FundMe)

 fundme + overflow예시를 보여줍니다. 아마도 remix에서 작업하던 파일

## [Lottery](./ls7_lottery)

 복권 추첨 시뮬레이션 입니다. Chainlink VRFConsumerBase를 이용 Pseudo random 해결. chainlink pricefeed 이용. Enum을 통해 Lottery state(시작, 돌아가는중, 종료 등)를 표현합니다

## [ERC20](./ls9_erc20)

ERC20 토큰을 발급합니다

## [Upgrade](./ls12_upgrade)

 Proxy패턴을 이용해서 smartcontract를 업그레이드 하는 방법을 배웁니다. 다른 프로젝트들과 큰 연계성은 없습니다

## [nft-demo](./nft-demo)

OpenSea schema에 맞게 메타데이터를 생성하여 nft를 만듭니다. json 형식으로 만든 데이터를 ipfs에 저장(-> CID) / NFT Minting / OpenSea에서 확인이 주된 활동입니다

