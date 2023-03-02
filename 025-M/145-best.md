Allarious

medium

# `_assessState` does not transfer from `late` to `active` within `TwoPaymentPeriodsInSeconds`

## Summary
`_assessState` does not transfer from `late` state to `active` state even if the payment was made withing the `TwoPaymentPeriodsInSeconds` and the `_assessState` is called.

## Vulnerability Detail
I case the underlying pool is back to active within the `TwoPaymentPeriodsInSeconds`, the pool keeps the funds locked when there is no need for such thing. While the comments mention that the funds stay locked for such amount, there is no need to keep the funds locked while the underlying pool is back to active. This can cause desync between the underlying pool and state manager where it can lead to further bugs. The behaviour of the lending pools should be delegated to them and if the pool is active, it means that the funds should be unlocked.

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L342-L364

## Impact
Funds stay locked for a longer time, and the protection seller has to lock the funds for `TwoPaymentPeriodsInSeconds` even if the payment is made seconds later than the deadline. 

## Code Snippet

## Tool used

Manual Review

## Recommendation
The active check should happen before the check for `TwoPaymentPeriodsInSeconds`:
```solidity
        else if (_previousStatus == LendingPoolStatus.Late) {
          /// State transition 2: Late -> Active
         if (_currentStatus == LendingPoolStatus.Active) {
           /// Update the current status of the lending pool to Active
           /// and move the lending pool to the active state
           lendingPoolStateDetail.currentStatus = LendingPoolStatus.Active;
           _moveFromLockedToActiveState(poolState, _lendingPool);

           /// Clear the late timestamp
           lendingPoolStateDetail.lateTimestamp = 0;
         }
        if (
          block.timestamp >
          (lendingPoolStateDetail.lateTimestamp +
            _getTwoPaymentPeriodsInSeconds(poolState, _lendingPool))
        ) {
          /// State transition 3: Late -> Defaulted
            if (_currentStatus == LendingPoolStatus.Late) {
            /// Update the current status of the lending pool to Active
            lendingPoolStateDetail.currentStatus = LendingPoolStatus.Defaulted;

            // Default state transition will be implemented in the next version of the protocol
            // _moveFromLockedToDefaultedState(poolState, _lendingPool);
          }
        }
```