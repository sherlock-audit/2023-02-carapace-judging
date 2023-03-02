clems4ever

high

# Protection premium is never accrued if protocol defaults without issuing a payment after protection start

## Summary
If a protection buyer buys protection and the lending pool status defaults right afterwards (without making a payment after protection buy), the protection premium is locked.

## Vulnerability Detail
As we see in `ProtectionPool.sol`:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L216-L223

In our case `_latestPaymentTimestamp < _startTimestamp`, so premium is never accrued for this protection, even if the protection expires. 
Additionally, this is inconsistent with the behavior of protections which have at least one payment after their start, since at their expiration the whole amount is accrued regardless of payments in the lending pool.

## Impact
Some premium amounts stay locked in the contract, accounted for in the variable `totalPremium` but never to be released

## Code Snippet

## Tool used

Manual Review

## Recommendation
Check also for expiration in this condition, and proceed anyway if the protection is expired