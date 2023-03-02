RaymondFam

medium

# `movePoolPhase()` could unexpectedly transition to Open phase

## Summary
`movePoolPhase()` allows the owner to move pool phase after verification. Once the pool is in `Open` phase, phase cannot be updated anymore.

## Vulnerability Detail
In the `else if` block of `movePoolPhase()`, the nested if statement checks `calculateLeverageRatio() <= poolInfo.params.leverageRatioCeiling` prior to moving the phase of the pool from `OpenToBuyers` to `Open`. The issue lies with a logic flaw in `calculateLeverageRatio()` that will return `0` if `totalProtection == 0`, presumably to avoid division by zero in the next return statement. This has created an unexpected issue, i.e. making `(calculateLeverageRatio() <= poolInfo.params.leverageRatioCeiling) == true` outright if `movePoolPhase()` is called when `totalProtection == 0` that leads to `calculateLeverageRatio() == 0`, a function execution that will prematurely transition the pool phase to the irreversible `Open`.

## Impact
The new phase of the pool, `Open`, has literally zero protection bought with `poolInfo.params.leverageRatioCeiling` very much exceeded by the leverage ratio for the pool where the supply is way higher than the demand. This inadvertently creates a very unhealthy situation excessively favoring protection buyers because the risk factor and the premium will be so much lower. 

## Code Snippet
`movePoolPhase()` is going to invoke `calculateLeverageRatio()` on line 540:

[File: ProtectionPool.sol#L521-L544](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L521-L544)

```solidity
  function movePoolPhase()
    external
    payable
    onlyOwner
    returns (ProtectionPoolPhase _newPhase)
  {
    ProtectionPoolPhase _currentPhase = poolInfo.currentPhase;

    /// Pool starts in OpenToSellers phase.
    /// Once the pool has enough capital, it can be moved to OpenToBuyers phase
    if (
      _currentPhase == ProtectionPoolPhase.OpenToSellers &&
      _hasMinRequiredCapital()
    ) {
      poolInfo.currentPhase = _newPhase = ProtectionPoolPhase.OpenToBuyers;
      emit ProtectionPoolPhaseUpdated(_newPhase);
    } else if (_currentPhase == ProtectionPoolPhase.OpenToBuyers) {
      /// when the pool is in OpenToBuyers phase, it can be moved to Open phase,
      /// if the leverage ratio is below the ceiling
540:      if (calculateLeverageRatio() <= poolInfo.params.leverageRatioCeiling) {
        poolInfo.currentPhase = _newPhase = ProtectionPoolPhase.Open;
        emit ProtectionPoolPhaseUpdated(_newPhase);
      }
    }
```
[File: ProtectionPool.sol#L584-L586](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L584-L586)

```solidity
  function calculateLeverageRatio() public view override returns (uint256) {
    return _calculateLeverageRatio(totalSTokenUnderlying);
  }
```
`_calculateLeverageRatio()` could return `0` on line 951, resulting in line 540 of `movePoolPhase()` easily get through to make an undesirable phase transition from `OpenToBuyers` to `Open`:

[File: ProtectionPool.sol#L945-L955](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L945-L955)

```solidity
  function _calculateLeverageRatio(uint256 _totalCapital)
    internal
    view
    returns (uint256)
  {
    if (totalProtection == 0) {
951:      return 0;
    }

    return (_totalCapital * Constants.SCALE_18_DECIMALS) / totalProtection;
  }
```
## Tool used

Manual Review

## Recommendation
Consider refactoring `_calculateLeverageRatio()` as follows:

```diff
  function _calculateLeverageRatio(uint256 _totalCapital)
    internal
    view
    returns (uint256)
  {
    if (totalProtection == 0) {
-      return 0;
+      revert ProtectionPoolIsNotOpen();
    }

    return (_totalCapital * Constants.SCALE_18_DECIMALS) / totalProtection;
  }
```
This prevents the unintended incident from happening when the pool is attempting to make leverage ratio effective, i.e. sitting in between the floor and ceiling while avoiding division by zero still in `(_totalCapital * Constants.SCALE_18_DECIMALS) / totalProtection`.