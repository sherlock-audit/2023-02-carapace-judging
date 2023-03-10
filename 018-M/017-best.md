chaduke

medium

# Withdraw transactions might fail during periods when they are supposed to be open for withdrawal.

## Summary
There are two edges cases under which ``withdraw()`` is disabled when it is supposed to be enabled: 
a) when ``_cycleParams.openCycleDuration == _cycleParams.cycleDuration``, that means there is no locked state, it is always open. 

b)  ``_cycleParams.openCycleDuration`` is near ``_cycleParams.cycleDuration``. That means, the open period is long, and the locked period is short. The cron job does not get a chance to be called during the locked period, but the locked period has already passed. 

The root cause for both cases is the same: the ``ProtectionPoolCycle`` state transition machine does not allow a transition from an open state of one cycle to the open state of the next cycle directly without going through a locked state first. This occurs even when the locked period has already passed.  

## Vulnerability Detail
In the following, we show when the ``withdraw()`` function might fail even though it should not have.  

1) Suppose ``cycleDuration = 7 days``, and ``openCycleDuration = 6.9 days``. Suppose the cron job is called each noon to transition the states. As a result, the cron job will fail to transition the pool state to the locked state in the last day. It has to wait until noon of day 8 to do that. We were hoping ``withdraw()`` will do the transition as well, but it will fail to do that for this case. 

2) In the morning of day 8, although the whole cycle has finished, and the state is supposed to be an open state, the ``withdraw()`` function  will still fail. Because the ``withdraw()`` function  calls the modifier ``whenPoolIsOpen()``, which calls ``poolCycleManager.calculateAndSetPoolCycleState(address(this)`` to transition the state of the protection pool when necessary. 

```javascript
function withdraw(uint256 _sTokenWithdrawalAmount, address _receiver)
    external
    override
    whenPoolIsOpen
    whenNotPaused
    nonReentrant
  {
    /// Step 1: Retrieve withdrawal details for current pool cycle index
    uint256 _currentCycleIndex = poolCycleManager.getCurrentCycleIndex(
      address(this)
    );
    WithdrawalCycleDetail storage withdrawalCycle = withdrawalCycleDetails[
      _currentCycleIndex
    ];

    /// Step 2: Verify withdrawal request exists in this withdrawal cycle for the user
    uint256 _sTokenRequested = withdrawalCycle.withdrawalRequests[msg.sender];
    if (_sTokenRequested == 0) {
      revert NoWithdrawalRequested(msg.sender, _currentCycleIndex);
    }

    /// Step 3: Verify that withdrawal amount is not more than the requested amount.
    if (_sTokenWithdrawalAmount > _sTokenRequested) {
      revert WithdrawalHigherThanRequested(msg.sender, _sTokenRequested);
    }

    /// Step 4: calculate underlying amount to transfer based on sToken withdrawal amount
    uint256 _underlyingAmountToTransfer = convertToUnderlying(
      _sTokenWithdrawalAmount
    );

    /// Step 5: burn sTokens shares.
    /// This step must be done after calculating underlying amount to be transferred
    _burn(msg.sender, _sTokenWithdrawalAmount);

    /// Step 6: Update total sToken underlying amount
    totalSTokenUnderlying -= _underlyingAmountToTransfer;

    /// Step 7: update seller's withdrawal amount and total requested withdrawal amount
    withdrawalCycle.withdrawalRequests[msg.sender] -= _sTokenWithdrawalAmount;
    withdrawalCycle.totalSTokenRequested -= _sTokenWithdrawalAmount;

    /// Step 8: transfer underlying token to receiver
    poolInfo.underlyingToken.safeTransfer(
      _receiver,
      _underlyingAmountToTransfer
    );

    emit WithdrawalMade(msg.sender, _sTokenWithdrawalAmount, _receiver);
  }
modifier whenPoolIsOpen() {
    /// Update the pool cycle state
    ProtectionPoolCycleState cycleState = poolCycleManager
      .calculateAndSetPoolCycleState(address(this));

    if (cycleState != ProtectionPoolCycleState.Open) {
      revert ProtectionPoolIsNotOpen();
    }
    _;
  }
```

5) Unfortunately, although  in the morning of day 8, we hope ``withdraw()`` will succeed by transitioning the state from the ``open`` state of the previous cycle to the ``open`` state of the new cycle, ``withdraw()`` will fail. This is because  in its current design, the state is forced to go through a ``locked`` state first before transitioning to another ``open`` state, even though the locked period has already passed. ``withdraw()``'s modifier ``whenPoolIsOpen`` will call  ``poolCycleManager.calculateAndSetPoolCycleState(address(this)`` and transition the state to the locked state, but then ``whenPoolIsOpen``  will revert after the transition reaches a locked state. As a result, ``withdraw`` will revert and no transition will occur. As a matter of factor, ``withdraw()`` will always fail the whole morning until the cron job is called to transition the state to a locked state first.  ``withdraw()``'s modifier ``whenPoolIsOpen`` does not have the capability to transition the state from an open state to a locked state, as it will always fail in this case. 


The case of  ``_cycleParams.openCycleDuration == _cycleParams.cycleDuration`` is similar: even though the intention is for the pool to be always open for withdraw, in the morning of day 8, ``withdraw()`` will still fail because it needs to wait for the noon cron job to bring the state to the locked state first before it can enter a new open state of the following cycle. Again,  ``withdraw()``'s modifier ``whenPoolIsOpen`` does not have the capability to transition the state from an open state to a locked state, as it will always fail in this case. 

 
This should not be the case. A redesign of the state transition machine is necessary: when the whole cycle has already completed, a state should be able to transit from an open state to another open state of the new cycle without having to going though a locked state in this case - since the locked period has already passed!

[https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/ProtectionPoolCycleManager.sol#L94-L143](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/ProtectionPoolCycleManager.sol#L94-L143)




## Impact
The current state transition machine of ``ProtectionPoolCycle`` cannot not transition from an open state to the open state of the next cycle directly, as a result, withdraw will fail even during the periods that are supposed to be open: a) when we want a pool to be always open; 2) when the locked period is short and it has already passed but the cron job is not called during that period. 

## Code Snippet
See above

## Tool used
VSCode

Manual Review

## Recommendation
We revise the state transition machine to allow the transition from ``open`` to ``open`` when the locked period has already passed (ZERO locked period is just a special case that is taken care of automatically): 

```diff
function calculateAndSetPoolCycleState(address _protectionPoolAddress)
    external
    override
    returns (ProtectionPoolCycleState _newState)
  {
    ProtectionPoolCycle storage poolCycle = protectionPoolCycles[
      _protectionPoolAddress
    ];

    /// Gas optimization:
    /// Store the current cycle state in memory instead of reading it from the storage multiple times.
    ProtectionPoolCycleState currentState = _newState = poolCycle
      .currentCycleState;

    /// If cycle is not started, that means pool is NOT registered yet.
    /// So, we can't move the cycle state
    if (currentState == ProtectionPoolCycleState.None) {
      return _newState;
    }

    /// If cycle is open, then check if it's time to move to LOCKED state.
    if (currentState == ProtectionPoolCycleState.Open) {
      /// If current time is past the initial open duration, then move to LOCKED state.
      if (
        block.timestamp - poolCycle.currentCycleStartTime >
        poolCycle.params.openCycleDuration
+     && block.timestamp - poolCycle.currentCycleStartTime <= // @audit: if not yet next cycle
+       poolCycle.params.cycleDuration
      ) {
        poolCycle.currentCycleState = _newState = ProtectionPoolCycleState
          .Locked;
      }
    }
    /// If cycle is locked, then check if it's time to start a new cycle.
-    else if (currentState == ProtectionPoolCycleState.Locked) {
+   else {
      /// If current time is past the total cycle duration, then start a new cycle.
      if (
        block.timestamp - poolCycle.currentCycleStartTime >
        poolCycle.params.cycleDuration
      ) {
        /// move current cycle to a new cycle
        _startNewCycle(
          _protectionPoolAddress,
          poolCycle,
          poolCycle.currentCycleIndex + 1
        );
        _newState = ProtectionPoolCycleState.Open;
      }
    }
```
