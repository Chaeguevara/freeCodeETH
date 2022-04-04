# Brownie aave 실습

1. ETH -> WETH로 변경
    1. contract가 사용하는 기본 단위
1. WETH를 deposit 보증금 제출
1. ETH를 담보로 token 빌림
    1. shortsell 해보기
1. 다시 갚음

## TESTING
Integation test: Kovan에 하면 됨

unitTst : Mainnet-fork에 하면 됨. 아마 aave에서 mock을 제공하지 않기 때문에 fork로만 작업할 수 있는듯?

## WETH 받기
WETH컨트랙트에 ETHㄹ르 맡기면 받을 수 있음

테스트하기 위한 interface는 [IWETH](./interfaces/IWeth.sol)임
# aave연결 설정
1. local mainnet-fork 사용
1. ILendingPool사용
    1. 각 test-net별 주소가 다름 --> ILendingPoolAddressProvier사용
    1. [AddressProvider](./interfaces/ILendingPoolAddressesProvider.sol), [LendingPool](./interfaces/ILendingPool.sol)
    1. V2에는 mainnet과 kovan만 있음
    

