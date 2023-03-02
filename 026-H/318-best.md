unforgiven

high

# Function verifyAndAccruePremium() In ProtectionPoolHelper incorrectly calculate accrued premium for expired protections

## Summary
Function `verifyAndAccruePremium()` calculates accrue premium until the last payment of the lending pool but for the expired protections that the expire time is after last payment the calculation done until the expired time and it would cause `totalPremiumAccrued` and `totalSTokenUnderlying` to have wrong values.

## Vulnerability Detail
This is `verifyAndAccruePremium()` code in ProtectionPoolHelper:
```solidity
  function verifyAndAccruePremium(
    ProtectionPoolInfo storage poolInfo,
    ProtectionInfo storage protectionInfo,
    uint256 _lastPremiumAccrualTimestamp,
    uint256 _latestPaymentTimestamp
  )
    external
    view
    returns (uint256 _accruedPremiumInUnderlying, bool _protectionExpired)
  {
    uint256 _startTimestamp = protectionInfo.startTimestamp;

    /// This means no payment has been made after the protection is bought or protection starts in the future.
    /// so no premium needs to be accrued.
    if (
      _latestPaymentTimestamp < _startTimestamp ||
      _startTimestamp > block.timestamp
    ) {
      return (0, false);
    }

    /// Calculate the protection expiration timestamp and
    /// Check if the protection is expired or not.
    uint256 _expirationTimestamp = protectionInfo.startTimestamp +
      protectionInfo.purchaseParams.protectionDurationInSeconds;
    _protectionExpired = block.timestamp > _expirationTimestamp;

    /// Only accrue premium if the protection is expired
    /// or latest payment is made after the protection start & last premium accrual
    if (
      _protectionExpired ||
      (_latestPaymentTimestamp > _startTimestamp &&
        _latestPaymentTimestamp > _lastPremiumAccrualTimestamp)
    ) {
      /**
       * <-Protection Bought(second: 0) --- last accrual --- now(latestPaymentTimestamp) --- Expiration->
       * The time line starts when protection is bought and ends when protection is expired.
       * secondsUntilLastPremiumAccrual is the second elapsed since the last accrual timestamp.
       * secondsUntilLatestPayment is the second elapsed until latest payment is made.
       */

      // When premium is accrued for the first time, the _secondsUntilLastPremiumAccrual is 0.
      uint256 _secondsUntilLastPremiumAccrual;
      if (_lastPremiumAccrualTimestamp > _startTimestamp) {
        _secondsUntilLastPremiumAccrual =
          _lastPremiumAccrualTimestamp -
          _startTimestamp;
      }

      /// if loan protection is expired, then accrue premium till expiration and mark it for removal
      uint256 _secondsUntilLatestPayment;
      if (_protectionExpired) {
        _secondsUntilLatestPayment = _expirationTimestamp - _startTimestamp;
        console.log(
          "Protection expired for amt: %s",
          protectionInfo.purchaseParams.protectionAmount
        );
      } else {
        _secondsUntilLatestPayment = _latestPaymentTimestamp - _startTimestamp;
      }

      /// Calculate the accrued premium amount scaled to 18 decimals
      uint256 _accruedPremiumIn18Decimals = AccruedPremiumCalculator
        .calculateAccruedPremium(
          _secondsUntilLastPremiumAccrual,
          _secondsUntilLatestPayment,
          protectionInfo.K,
          protectionInfo.lambda
        );

      console.log(
        "accruedPremium from second %s to %s: ",
        _secondsUntilLastPremiumAccrual,
        _secondsUntilLatestPayment,
        _accruedPremiumIn18Decimals
      );

      /// Scale the premium amount to underlying decimals
      _accruedPremiumInUnderlying = scale18DecimalsAmtToUnderlyingDecimals(
        _accruedPremiumIn18Decimals,
        poolInfo.underlyingToken.decimals()
      );
    }
  }
```
when a protection has this state for it's timeline:
```solidity
- Protection_start(seconds=0)
- last_accrual(seconds=100)
- latestPaymentTimestamp(seconds=200)
- Protection_Expiration(seconds=300)
- now(seconds=350)
```
in current implementation code would set:
```solidity
_secondsUntilLastPremiumAccrual = 100 - 0 = 100;
_secondsUntilLatestPayment = 300 - 0 = 300; 
// because Protection is expired code set it to this value but it should have been 200 because last payment < expiration.
```
so code set wrong value for `_secondsUntilLatestPayment` and `_accruedPremiumInUnderlying` would get calculated based on entire Protection time while `latestPaymentTimestamp` is less than expiration time and the whole payment is not accrued yet.
because the result of premium accrued that  `ProtectionPoolHelper.verifyAndAccruePremium()` returns is added to `totalPremiumAccrued` in ProtectionPool and `totalPremiumAccrued` would not show the "The total premium accrued in underlying token up to the last premium accrual timestamp" as comment in code says. the value of the `totalPremiumAccrued` would be higher than real accrued premium until the timestamp.
because `totalPremiumAccrued` is used in other logics this can cause other logics like lock capital or deposit or withdraw to work wrongly. code may try to transfer extra funds or lock more funds while they are not in the contract balance and transaction would fail.

## Impact
Funds can be lost(all the calculations based on the `totalPremiumAccrued` would be wrong) or logics can be broken.

## Code Snippet
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L250-L260

## Tool used
Manual Review

## Recommendation
when loan is expired but expire time is before the last payment time, then calculate `_secondsUntilLatestPayment ` based on last payment time.