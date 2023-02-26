clems4ever

medium

# Freezing of the protocol when totalSTokenUnderlying is zero but totalSupply is non-zero

## Summary
In some cases the protocol can contain zero funds while having a non zero totalSupply of STokens. In that case the protocol will not be able to accept any new deposits and any new protection buys, thus coming to a halt, unless all STokens are burned by their respective holders.

## Vulnerability Detail
In the case `lockCapital` has to lock all available capital:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L415-L419

`totalSTokenUnderlying` becomes zero, but `totalSupply` is still non-zero since no SToken have been burned. 
Which means that new deposits will revert because `_getExchangeRate()` is zero:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L602-L605

And `convertToSToken` tries to divide by `_getExchangeRate()`;
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L602-L605 

Also all new protection buying attempts will revert because `_leverageRatio` is zero, and thus under `leverageRatioFloor`.

## Impact
The protocol comes to a halt, unless every SToken holder burn their shares by calling `withdraw` after enough cycles have passed, returning to the case `totalSupply == 0`.

## Code Snippet

## Tool used

Manual Review

## Recommendation
Keep a minimum amount of totalSTokenUnderlying in the contract in any case (can be 1e6).