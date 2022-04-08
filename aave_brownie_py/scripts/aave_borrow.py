from brownie import network,config, interface
from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from web3 import Web3

#0.1 Token
AMOUNT = Web3.toWei(0.1,"ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        #fork에선 아직 weth를 받지 않았기 때문에
        get_weth()
    #ABI + Address --> aave의 leanding pool작
    lending_pool = get_lending_pool()
    print(lending_pool)
    # ERC20 Token approve해야함
    # approve_erc20()
    approve_erc20(AMOUNT,lending_pool.address, erc20_address, account)
    #function deposit(address asset, uint256 amount, address onBehalfOf, uint16 referralCode)
    print("---------------담보설정중....WETH---------------")
    tx = lending_pool.deposit(erc20_address, AMOUNT, account.address,0,{"from":account})
    tx.wait(1)
    print("---------------담보설정 완료---------------")
    #getUserAccountData
    borrowable_eth,total_dept = get_borrowable_data(lending_pool,account)
    #Borrow DAI(aave token) 1. DAI <-> ETH 교환비 구하기
    # price_feed address 는 chainlink가서 
    dai_eth_price = get_asset_price(config["networks"][network.show_active()]["dai_eth_price_feed"])
    #풀대출 떙겨
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    print(f"{amount_dai_to_borrow} DAI 대출하겠습니다 ")
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_pool.borrow(dai_address, Web3.toWei(amount_dai_to_borrow,"ether"), 1, 0, account.address,{"from":account})
    borrow_tx.wait(1)
    print("We borrowed some DAI")
    #대출 후 데이터 확인 --> 담보, 대출 등 값을 확인하여 대출이 실행됬는지 확인
    get_borrowable_data(lending_pool,account)
    #대출 상환
    repay_all(Web3.toWei(amount_dai_to_borrow,"ether"), lending_pool,account)
    #마지막 값 검사
    get_borrowable_data(lending_pool,account)
    print(
            "Aave, Brownie, chainlink에서 담보 , 대출, 상환 끝"

            )
           


def repay_all(amount,lending_pool, account):
    approve_erc20(
            Web3.toWei(amount,"ether"),
            lending_pool,
            config["networks"][network.show_active()]["dai_token"],
            account
     )
    #function repay(address asset, uint256 amount, uint256 rateMode, address onBehalfOf)
    repay_tx = lending_pool.repay(
                config["networks"][network.show_active()]["dai_token"],
                amount,
                1,
                account.address,
                {"from":account},
            )
    repay_tx.wait(1)
    print("repayed!")


def get_asset_price(price_feed_address):
    #ABI + Address -> interface
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price,"ether")
    print(f"DAI/ETH 가격은 {converted_latest_price}")
    return float(converted_latest_price)


def get_borrowable_data(lending_pool, account):
    """
    function getUserAccountData(address user) -> returns
    (
        totalCollateralETH
        totalDebtETH
        availableBorrowsETH
        .
        .
        .
    )
    """
    print("-------------유저 계좌 정보 가져오는 중------------")
    (total_collateral_eth,
            total_debt_eth,
            available_borrows_eth,
            current_liquidation_threshold,
            ltv,
            health_factor
     ) = lending_pool.getUserAccountData(account.address)
    available_borrows_eth = Web3.fromWei(available_borrows_eth,"ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth,"ether")
    total_debt_eth = Web3.fromWei(total_debt_eth,"ether")
    print(f"{total_collateral_eth} ETH 만큼 담보로 설정하였습니다")
    print(f"{total_debt_eth} ETH만큼 대출한 상태입니다")
    print(f"{available_borrows_eth} ETH만큼 더 대출할 수 있습니다.")#Liquidation threshold로 결정됨. 자세한건 risk-parameter ㅂㅜ분 참조 
    print("-------------유저 계좌 정보 완료------------")
    return (float(available_borrows_eth),float(total_debt_eth))
    
def get_lending_pool():
    """
    AAVe 마켓별로, lending_pool주소가 다름
    """
    #ABI + Address 를 사용해야 하지만 interface로 할것임
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(
            config["networks"][network.show_active()]["lending_pool_addresses_provider"]
            )
    lending_pool_address = lending_pool_address_provider.getLendingPool()
    #이제 lending_pool_address 확인 --> ABI + address --> interface
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20(amount, spender, erc20_address, account):
    """
    erc20 토큰을 사용할 수 있도록 권한 설정. EIP20을 보고 하거나, https://github.com/PatrickAlphaC/aave_brownie_py/blob/main/interfaces/IERC20.sol
    에서 따와도 됨
    approve(address speneer, uint256 value) --> 누가 얼마나 쓸 수 있는지 허
    Input : 누가(spender) 얼마나(value) 어떤 토큰을(erc20_address) 사용하게 할지. 관리자가(account)
    """
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender,amount,{"from":account})
    tx.wait(1)
    print("Approved!")
    return tx
