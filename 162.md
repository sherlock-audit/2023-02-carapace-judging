ctf_sec

medium

# Before protection sellers withdraw fund, accruePremiumAndExpireProtections should be called.

## Summary

Before protection sellers withdraw fund, accruePremiumAndExpireProtections should be called.

## Vulnerability Detail

Before protection sellers withdraw fund, accruePremiumAndExpireProtections should be called.

## Impact

WIthout calling accruePremiumAndExpireProtections before the withdrawal transction from protection sellers, the totalSTokenUnderying and totalPremiumAccured and totalProtection, which are used to the calculate how many underlying token can be withdrawal given amount of SToken are not in sync

```solidity
    /// Gas optimization: only update storage vars if there was premium accrued
    if (_totalPremiumAccrued > 0) {
      totalPremiumAccrued += _totalPremiumAccrued;
      totalSTokenUnderlying += _totalPremiumAccrued;
    }

    /// Reduce the total protection amount of this protection pool
    /// by the total protection amount of the expired protections
    if (_totalProtectionRemoved > 0) {
      totalProtection -= _totalProtectionRemoved;
    }
```

Which leads to loss of premium reward for protection when they want to withdraw the fund using sToken after 2 cycle passes.

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L276-L355

## Tool used

Manual Review

## Recommendation

Before protection sellers withdraw fund, accruePremiumAndExpireProtections should be called.
