__141345__

medium

# `totalSTokenUnderlying` not timely updated

## Summary

The accruing of premium is after the expiry of protection, and then `totalSTokenUnderlying` will be updated. And the updates are triggered manually by hand or by bot, not built into the smart contracts, so it is possible that there is some time gap when `totalSTokenUnderlying` is not timely updated. The inaccurate value of `totalSTokenUnderlying` could lead to problem when users deposit and withdraw.


## Vulnerability Detail

When there is un-accrued premium and `totalSTokenUnderlying` are delayed, 
`convertToUnderlying()/convertToSToken()` functions could return inaccurate results. Hence when users deposit and withdraw, the calculated amount will be inaccurate.


Currently, accruing of premium only happens after the protection is expired.

```solidity
File: contracts/core/pool/ProtectionPool.sol
0963:   function _accruePremiumAndExpireProtections() {

0985:       /// Verify & accrue premium for the protection and
0986:       /// if the protection is expired, then mark it as expired
0987:       (
0988:         uint256 _accruedPremiumInUnderlying,
0989:         bool _expired
0990:       ) = ProtectionPoolHelper.verifyAndAccruePremium(
0991:           poolInfo,
0992:           protectionInfo,
0993:           _lastPremiumAccrualTimestamp,
0994:           _latestPaymentTimestamp
0995:         );
0996:       _accruedPremiumForLendingPool += _accruedPremiumInUnderlying;
0997: 
0998:       if (_expired) {
0999:         /// Add removed protection amount to the total protection removed
1000:         _totalProtectionRemoved += protectionInfo
1001:           .purchaseParams
1002:           .protectionAmount;

File: contracts/libraries/ProtectionPoolHelper.sol
201:   function verifyAndAccruePremium(

228:     /// Only accrue premium if the protection is expired
229:     /// or latest payment is made after the protection start & last premium accrual
230:     if (
231:       _protectionExpired ||
232:       (_latestPaymentTimestamp > _startTimestamp &&
233:         _latestPaymentTimestamp > _lastPremiumAccrualTimestamp)
234:     ) {
```

And the accrued amount will be added to `totalSTokenUnderlying`.

```solidity
279:   function accruePremiumAndExpireProtections(address[] memory _lendingPools)

317:       /// Iterate all active protections for this lending pool and
318:       /// accrue premium and expire protections if there is new payment
319:       (
320:         uint256 _accruedPremiumForLendingPool,
321:         uint256 _totalProtectionRemovedForLendingPool
322:       ) = _accruePremiumAndExpireProtections(
323:           lendingPoolDetail,
324:           _lastPremiumAccrualTimestamp,
325:           _latestPaymentTimestamp
326:         );
327:       _totalPremiumAccrued += _accruedPremiumForLendingPool;

341:     }

344:     if (_totalPremiumAccrued > 0) {
345:       totalPremiumAccrued += _totalPremiumAccrued;
346:       totalSTokenUnderlying += _totalPremiumAccrued;
347:     }
```
`totalSTokenUnderlying` is used for exchange rate when deposit and withdraw.

Imagine, the un-accrued premium is $100, and `totalSTokenUnderlying` is $10,000, when deposit, users could get 1% more sToken, and 1% less when withdraw.


## Impact

When users deposit and withdraw, the amounts would be inaccurate, some user will get undeserved fund and some will get less then they should.


## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core//pool/ProtectionPool.sol#L987-L1002

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core//pool/ProtectionPool.sol#L230-L234

## Tool used

Manual Review

## Recommendation

When referring to `totalSTokenUnderlying`, first accruing the premium to make sure the value is up to date. 

Or accrue premium as soon as it is transferred at the beginning.
