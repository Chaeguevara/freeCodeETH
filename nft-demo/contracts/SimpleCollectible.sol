// SPDX-License-Identifier: MIT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
  uint256 public tokenCounter; //만들어진 토큰 갯수. UniqueID가 되기도 함
  //factory 기능. 만들기만 한다
  constructor () public ERC721 ("Dogie", "DOG"){
    tokenCounter = 0;
  }
  //만들어진 토큰의 소유주 설정이 필요
  //현재 토큰에서 받을 수 있는 attirbute는 tokenURI를 통해 만듬. 관련 기능 추가
  function createCollectible(string memory tokenURI) public returns (uint256){
    uint256 newTokenId = tokenCounter;
    _safeMint(msg.sender, newTokenId);// 새 토큰 minting. 원래 계약의 _safeMint 사용
    _setTokenURI(newTokenId, tokenURI); //URI설정
    tokenCounter =tokenCounter +1;
    return newTokenId;
  }
}
