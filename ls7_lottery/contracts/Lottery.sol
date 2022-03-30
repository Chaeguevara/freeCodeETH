// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";


contract Lottery{
  address payable[] public players; //참여자 목록
  uint256 public usdEntryFee; // 참가비용 -> $50
  AggregatorV3Interface internal ethUsdPriceFeed;

  /// 최초 계약이 생성될떄 priceFeed의 주수와 entryFee 설정
  // priceFeed는 각 testNet마다 주소가 달라서 파라미터
  constructor(address _priceFeedAddress) public{
    usdEntryFee = 50*(10**18); // chailink 기준 decimal 8이라는 얘기가 계속 나옴. 아마 wei & decimal로 인해 18인
    ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
  
  }  

  // Lottery에 참가
  // 최소 참가비용이 없으면 참가 불가
  function enter() public payable {
    // 최소 $50필요
    players.push(msg.sender);
  
  }

  function getEntranceFee() public view returns (uint256) {
    (,int price,,,) = ethUsdPriceFeed.latestRoundData();
    uint256 adjustedPrice = uint256(price) * 10**10; // 18 decimal
    uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice; //18decimal로 다 맞추는듯??? 
    return costToEnter;

  }
  
  //관리자가 로터리 시작
  function startLottery() public {
  }

  //관리자가 로터리 끝
  function endLottery() public{
  }



}

