// NFT 제작
// tokenURI는 강아지 3개 중 하나
// random하게 셋 중 하나 선택

// SPDX-License-Identifer: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
  uint256 public tokenCounter;
  bytes32 public keyhash;
  uint256 public fee;
  enum Breed{PUG,SHIBA_INU, ST_BERNARD}
  mapping(uint256 => Breed) public tokenIdToBreed;
  mapping(bytes32 => address) public requestIdToSender;
  event requestedCollectible(bytes32 indexed requestId, address requester); //index는 찾기 쉽게 만드는 용도
  event breedAssigned(uint256 indexed tokenId, Breed breed);

  //constructor. ERC721, VRFConsumerBase 에 필요한 argument넣음
  constructor(address _vrfcoordinator, address _linkToken, bytes32 _keyHash, uint256 _fee) public
    VRFConsumerBase(_vrfcoordinator, _linkToken)
    ERC721("Dogie", "DOG"){
      tokenCounter = 0;
      keyhash = _keyHash;
      fee = _fee;
    }

    //NFT 생성
    // random 호출 --> requestId와 호출자 mapping --> 다시 fulfillRandomness에서 가져옴
    function createCollectible() public returns (bytes32){
      bytes32 requestId = requestRandomness(keyhash,fee); 
      requestIdToSender[requestId] = msg.sender;
      emit requestedCollectible(requestId, msg.sender);
    }

    //verifiable random 사용. 무작위로 멍멍멍이 부여 
    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
      Breed breed = Breed(randomNumber % 3);
      //tokenId를 받아와서, 종과 mapping 함
      uint256 newTokenId = tokenCounter;
      tokenIdToBreed[newTokenId] = breed; 
      emit breedAssigned(newTokenId, breed);
      //minting. 이전처럼 _safeMint실행. 이떄 msg.sender를 어떻게 처리할지 --> mapping
      address owner = requestIdToSender[requestId];
      _safeMint(owner, newTokenId);
      tokenCounter = tokenCounter +1;

    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public{
      //토큰 ID 소유자 또는 허가된 사람만 ID의 TokenURI 변경가능. openzeppelin기능
      require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: 호출한 사람이 소유자 또는 허가된 이가 아닙니다");
      _setTokenURI(tokenId, _tokenURI);
    }

}
