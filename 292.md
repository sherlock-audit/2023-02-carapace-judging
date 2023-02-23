unforgiven

high

# Protection sellers can bypass withdrawal delay mechanism and avoid losing funds when loans are defaulted by creating withdrawal request in each cycle

## Summary
To prevent protection sellers from withdrawing fund immediately when protected lending pools are defaults, there is withdrawal delay mechanism, but it's possible to bypass it by creating withdraw request in each cycle by doing so user can withdraw in each cycle's open state. there is no penalty for users when they do this or there is no check to avoid this.

## Vulnerability Detail
This is `_requestWithdrawal()` code:
```solidity
  function _requestWithdrawal(uint256 _sTokenAmount) internal {
    uint256 _sTokenBalance = balanceOf(msg.sender);
    if (_sTokenAmount > _sTokenBalance) {
      revert InsufficientSTokenBalance(msg.sender, _sTokenBalance);
    }

    /// Get current cycle index for this pool
    uint256 _currentCycleIndex = poolCycleManager.getCurrentCycleIndex(
      address(this)
    );

    /// Actual withdrawal is allowed in open period of cycle after next cycle
    /// For example: if request is made in at some time in cycle 1,
    /// then withdrawal is allowed in open period of cycle 3
    uint256 _withdrawalCycleIndex = _currentCycleIndex + 2;

    WithdrawalCycleDetail storage withdrawalCycle = withdrawalCycleDetails[
      _withdrawalCycleIndex
    ];

    /// Cache existing requested amount for the cycle for the sender
    uint256 _oldRequestAmount = withdrawalCycle.withdrawalRequests[msg.sender];
    withdrawalCycle.withdrawalRequests[msg.sender] = _sTokenAmount;

    unchecked {
      /// Update total requested withdrawal amount for the cycle considering existing requested amount
      if (_oldRequestAmount > _sTokenAmount) {
        withdrawalCycle.totalSTokenRequested -= (_oldRequestAmount -
          _sTokenAmount);
      } else {
        withdrawalCycle.totalSTokenRequested += (_sTokenAmount -
          _oldRequestAmount);
      }
    }

    emit WithdrawalRequested(msg.sender, _sTokenAmount, _withdrawalCycleIndex);
  }
```
As you can see it doesn't keep track of user current withdrawal requests and user can request withdrawal for all of his balance in each cycle and by doing so user can set `withdrawalCycleDetails[Each Cycle][User]` to user's sToken balance. and whenever user wants to withdraw he only need to wait until the end of the current cycle while he should have waited until next cycle end.

## Impact
protection sellers can request withdraw in each cycle for their full sToken balance and code would allow them to withdraw in each cycle end time because code doesn't track how much of the balance of users is requested for withdrawals in the past.

## Code Snippet
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L1061-L1097

## Tool used
Manual Review

## Recommendation
To avoid this code should keep track of user balance that is not in withdraw delay and user balance that are requested for withdraw. and to prevent users from requesting withdrawing and not doing it protocol should have some penalties for withdrawals, for example the waiting withdraw balance shouldn't get reward in waiting duration.