// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";


// Java의 extends,implements와 비슷한 
contract Lottery is Ownable, VRFConsumerBase{
  address payable[] public players; //참여자 목록
  address payable public recentWinner; // 최근 승자
  uint256 public randomness; //최근 random값
  uint256 public usdEntryFee; // 참가비용 -> $50
  AggregatorV3Interface internal ethUsdPriceFeed;
  uint256 public fee;
  bytes32 public keyhash;
  
  enum LOTTERY_STATE{
    OPEN,
    CLOSED,
    CALCULATING_WINNER
  }

  LOTTERY_STATE public lottery_state; //현재 로터리 상태. 열림 / 닫힘 / 위너 계산중 --> 스테이트 이용 시작 / 끝 등에 사용



  /// 최초 계약이 생성될떄 priceFeed의 주수와 entryFee 설정
  // priceFeed는 각 testNet마다 주소가 달라서 파라미터
  // VRFConsumerBase를 위한 constructor 추가
  constructor(address _priceFeedAddress,
              address _vrfCoordniator,
              address _link,
              uint256 _fee,
              bytes32 _keyhash
             ) public VRFConsumerBase(_vrfCoordniator, _link) {
    usdEntryFee = 50*(10**18); // chailink 기준 decimal 8이라는 얘기가 계속 나옴. 아마 wei & decimal로 인해 18인
    ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
    lottery_state = LOTTERY_STATE.CLOSED;
    fee = _fee;
    keyhash = _keyhash;
   
  }  

  // Lottery에 참가
  // 최소 참가비용이 없으면 참가 불가
  function enter() public payable {
    // 최소 $50필요
    require(lottery_state == LOTTERY_STATE.OPEN,"현재 참여할 수 없습니다");
    require(msg.value >= getEntranceFee(), "Ethereum이 부족합니다!");
    players.push(msg.sender);
  
  }

  function getEntranceFee() public view returns (uint256) {
    (,int price,,,) = ethUsdPriceFeed.latestRoundData();
    uint256 adjustedPrice = uint256(price) * 10**10; // 18 decimal
    uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice; //18decimal로 다 맞추는듯??? 
    return costToEnter;

  }
  
  //관리자가 로터리 시작
  // Openzeplin의 onlyOwner사
  function startLottery() public onlyOwner{
    require(
      lottery_state == LOTTERY_STATE.CLOSED,
      "새 로터리를 시작할 수 없습니다"
    );
    lottery_state = LOTTERY_STATE.OPEN;
  }

  //관리자가 로터리 끝
  function endLottery() public onlyOwner{
    lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
    //random 값 request를 보냄
    bytes32 requestId = requestRandomness(keyhash,fee);
  }

  function fulfillRandomness(bytes32 _requestId, uint256 _randomness) internal override{
    require(lottery_state ==LOTTERY_STATE.CALCULATING_WINNER, "아직 !");
    require(_randomness>0, "랜덤값이 없음");
    uint256 indexOfWinner = _randomness % players.length;
    recentWinner = players[indexOfWinner];
    recentWinner.transfer(address(this).balance);
    //reset
    players = new address payable[](0);
    lottery_state = LOTTERY_STATE.CLOSED;
    randomness =_randomness;
  }



}

