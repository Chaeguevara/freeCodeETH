// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol"; // ERC20기능만 가져다 씀
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol"; //Price Feed


contract TokenFarm is Ownable {
  // 기능
  // stake - unstake - issue - addAllowed - getValue
  // stake = 스테이킹 시작, unstake = 스테이킹 종료
  // issue = 스테이킹에 대한 보상 발행
  // addAllowed = 스테이킹 가능한 토큰 추가
  // getValue = 각 토큰의 가치 계
    mapping(address => mapping(address=>uint256)) public stakingBalance; //token -> user -> userstaked token. 토큰 : 유저매핑인데 문제가..? 안생기나..?
    mapping(address => uint256) public uniqueTokenStaked; //각 유저당 stake한 토큰의 종류 수
    mapping(address => address) public tokenPriceFeedMapping; // token주소 --> priceFeed 주소
    address[] public stakers;
    address[] public allowedTokens; // Stake허용하는 token들(ETH, DAI 등등)
    IERC20 public dappToken; // 여기서 사용하는 토큰의


    constructor(address _dappTokenAddress) public {
      dappToken = IERC20(_dappTokenAddress); //계약 생성시 토큰 주소 설정
    }

    function setPriceFeedContract(address _token, address _priceFeed)
    public
    onlyOwner
    {
      tokenPriceFeedMapping[_token] = _priceFeed; //각 토큰 컨트랙트 주소와 _priceFeed 주소 매핑. chainlink에서 각 토큰별 pricefeed주소가 달라서 생기는 일

    }


    function issueTokens() public onlyOwner {
      // Staking하는 모든 사람들에게 토큰 발행
      for (
        uint256 stakersIndex = 0;
        stakersIndex < stakers.length;
        stakersIndex++
      ){
        address recipient = stakers[stakersIndex]; // 보상을 받을 주소     
        uint256 userTotalValue = getUserTotalValue(recipient); // 보상받을 총량
        dappToken.transfer(recipient, userTotalValue); //ERC20 Interface 
        
        }
    
    }

    // user가 가진 토큰 가치 총합 계산
    function getUserTotalValue(address _user) public view returns (uint256){
      uint256 totalValue = 0;
      require(uniqueTokenStaked[_user] > 0, "No tokens"); 
      for(
          uint256 allowedTokensIndex = 0;
          allowedTokensIndex < allowedTokens.length; 
          allowedTokensIndex++
         ){
          totalValue = totalValue + getUserSingleTokenValue(_user, allowedTokens[allowedTokensIndex]); 
         }
         return totalValue;
    }

    //유저가 staking한 하나의 토큰의 가치 계
    function getUserSingleTokenValue (address _user, address _token)
    public
    view
    returns (uint256){
        // stake한 토큰이 없다면return 0
        if(uniqueTokenStaked[_user] <= 0){
          return 0;
        } 
        //각 토큰의 가격과 decimal값 받아옴 --> 가격 / 10**decimal하면 USD계산 가능한
      (uint256 price, uint256 decimals) = getTokenValue(_token);
      return
            (stakingBalance[_token][_user] * price / (10**decimals));
      
    }


    function getTokenValue(address _token) public view returns (uint256, uint256) {
      //pricefeed주소
      address priceFeedAddress = tokenPriceFeedMapping[_token];
      AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddress);
      (,int256 price,,,) = priceFeed.latestRoundData();
      uint256 decimals = uint256(priceFeed.decimals());
      return (uint256(price), decimals);
    
    }


    function stakeTokens(uint256 _amount, address _token) public {
      require(_amount > 0, "Amount must be more than 0");
      require(tokenIsAllowed(_token), "Token is currently no allowed");
      IERC20(_token).transferFrom(msg.sender, address(this), _amount);
      updateUniqueTokensStaked(msg.sender, _token);
      stakingBalance[_token][msg.sender] = stakingBalance[_token][msg.sender] + _amount;  
      if (uniqueTokenStaked[msg.sender] == 1){ //staking한 토큰의 종류가 1개가 되는 순간 staker가 된다고 가정...아닐거 같은데? unstake해서 다시 0이 되면?
        stakers.push(msg.sender);
      } 
    }


    function unstakeTokens(address _token) public {
      uint256 balance = stakingBalance[_token][msg.sender];
      require(balance > 0, "Staking balance cannot be 0");
      IERC20(_token).transfer(msg.sender, balance);
      stakingBalance[_token][msg.sender] = 0;
      uniqueTokenStaked[msg.sender] = uniqueTokenStaked[msg.sender] -1; //stake한 token종류 -1개가
      //staker가 두번 일어나는 문제 해결 --> unstake 할때 더이상 staking하는게 없는 유저를 안없애면 생기는문제 인듯
      if(uniqueTokenStaked[msg.sender] == 0) {
        for (
          uint256 stakersIndex = 0;
            stakersIndex < stakers.length;
          stakersIndex++
        ){
          if (stakers[stakersIndex] == msg.sender){
              stakers[stakersIndex] = stakers[stakers.length -1]; // array의 마지막 주소로 덮어쓰고
              stakers.pop(); //마지막 array없앰. 왜냐하면 이미 덮어쓰기로 두개 됨
          
          }
          
          
          }
      }

    
    }

    //해당 토큰을 새롭게 stake하는 거라면 --> token종류 +1
    function updateUniqueTokensStaked(address _user, address _token) internal {
      if (stakingBalance[_token][_user] <= 0){
        uniqueTokenStaked[_user] = uniqueTokenStaked[_user] + 1;
      }
    
    }

    function addAllowedTokens(address _token) public onlyOwner{
      allowedTokens.push(_token);
    }

    function tokenIsAllowed(address _token) public returns (bool){
      for (uint256 allowedTokensIndex=0; allowedTokensIndex < allowedTokens.length; allowedTokensIndex ++){
        if(allowedTokens[allowedTokensIndex] == _token){
          return true;
        }
        return false;
      }
    
    }
}
