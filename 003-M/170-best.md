MalfurionWhitehat

medium

# Premium calculation and accrual rounds down when converting from 18Decimals to UnderlyingDecimals, leading to protocol loss of funds

## Summary

Premium calculation and accrual rounds down when converting from 18Decimals to UnderlyingDecimals, leading to protocol loss of funds.

## Vulnerability Detail

`ProtectionPool.calculateProtectionPremium` and `ProtectionPool.accruePremiumAndExpireProtections` both use `ProtectionPoolHelper.scale18DecimalsAmtToUnderlyingDecimals`, which [rounds down](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L344-L349) when converting from 18 decimals to the underlying number of decimals. 

In this particular case, where the underlying is USDC, this means that converting from 18 to 6 decimals will round down, leading to loss of funds by the protocol. 

For example, assuming the value `0.1234567e18` is scaled from 18 to 6 decimals, it rounds down to `123456`, but since premium calculation is a value that the protocol receives from protection buyers, it should round up to `123457`.  With time, these rounding errors can add up and become significant.

## Impact

Protocol will lose value on every premium calculation and accrual.

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L344-L349

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L128-L131

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L278-L282

## Tool used

Manual Review

## Recommendation

Whenever the protocol is receiving funds from users, it should round up.
