// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LedIoT {

    event ligarDesligarLed(string comando);

    function ligarDesligar(string memory _comando) public {
        emit ligarDesligarLed(_comando);
    }
}