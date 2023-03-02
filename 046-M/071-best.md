rvierdiiev

medium

# In case if several lending pools will default and not enough underlying to cover protections for both of them then only first lending pool receives full capital

## Summary
In case if several lending pools will default and not enough underlying to cover protections for both of them then only first lending pool receives full capital
## Vulnerability Detail
Function `_assessState` loops through all lending pools of protection pool in order to check their state.
In case if lending pool is late in payment, then `DefaultStateManager._moveFromActiveToLockedState` function [is called](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L332) in order to lock capital.

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L390-L416
```solidity
  function _moveFromActiveToLockedState(
    ProtectionPoolState storage poolState,
    address _lendingPool
  ) internal {
    IProtectionPool _protectionPool = poolState.protectionPool;


    /// step 1: calculate & lock the capital amount in the protection pool
    (uint256 _lockedCapital, uint256 _snapshotId) = _protectionPool.lockCapital(
      _lendingPool
    );


    /// step 2: create and store an instance of locked capital for the lending pool
    poolState.lockedCapitals[_lendingPool].push(
      LockedCapital({
        snapshotId: _snapshotId,
        amount: _lockedCapital,
        locked: true
      })
    );


    emit LendingPoolLocked(
      _lendingPool,
      address(_protectionPool),
      _snapshotId,
      _lockedCapital
    );
  }
```
It calls `_protectionPool.lockCapital` which locks total protections amount and decreases [amount of available underlying token](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L415-L422).
In case if it's not enough underlying to cover protections it locks all available amount.

When 2 lending pools or more will default in same time, then advantage will be provided depending on their index in array.
And protections that were in latest lending pool can not receive payment.

Scenario.
1.2 lending pools defaults at same time. Both of them has total protection for 75_000.
2.ProtectionPool has deposit for 100_000 underlying.
3.First lending pool protection buyers will receive full protection: 75_000.
4.Second lending pool protection buyers will receive only 25_000.

I understand that protocol believes that such thing will never happen and lending pools will not be defaulted at same time, but still it's possible, that's why i think it's medium. Good decision will be to split loses for protection buyers of different lending pools.
## Impact
Some protection buyers can loose much more than another.
## Code Snippet
Provided above
## Tool used

Manual Review

## Recommendation
Split loses among all protection buyers in case if not enough underlying to cover all protections.