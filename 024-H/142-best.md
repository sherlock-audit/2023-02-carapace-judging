MalfurionWhitehat

high

# Protection seller will lose unlocked capital if it fails to claim during more than one period

## Summary

The protection seller will lose unlocked capital if it fails to claim during more than one period.

## Vulnerability Detail

The function `DefaultStateManager._calculateClaimableAmount`, used by `DefaultStateManager.calculateAndClaimUnlockedCapital`, which in turn is used by `ProtectionPool.claimUnlockedCapital`, [overrides the claimable unlocked capital](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L500-L505) on every loop iteration on the [`lockedCapitals` array](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L476-L478). 

As a result, [only the last snapshot is returned](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L479) by this function, regardless if the protection seller has claimed the unlocked capital or not. The purpose of this code was to prevent sellers from [claiming the same snapshot twice](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L487), but since the `_claimableUnlockedCapital` variable is being overwritten instead of incremented, on each loop iteration, it will also make sellers lose unlocked capital if they fail to claim at each snapshot.

Proof of concept:

1. Pool goes to locked state with snapshotId 1
2. Pool goes to active state
3. Pool goes to locked state with snapshotId 2
4. Pool goes to active state
5. Protection seller calls `ProtectionPool.claimUnlockedCapital`, but they will only receive what's due from snapshotId 2, not from snapshotId 1

## Impact

The protection seller will lose unlocked capital if it fails to claim during more than one period.

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L500-L505

## Tool used

Manual Review

## Recommendation

Increment `_claimableUnlockedCapital` [for all](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L502-L505) locked capital instances.
