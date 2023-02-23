clems4ever

high

# Dos due to unbounded array on claiming of unlocked capitals

## Summary
To determine the claimable amount for a user, the protocol uses the function `calculateAndClaimUnlockedCapital`, which iterates over
all `lendingPools` of a protectionPool and for each `lendingPool` over all capital locking events (`lockedCapitals`).

Both arrays only grow over time, and it is highly probable that this function will revert with OUT-OF-GAS once these arrays become big enough.

## Vulnerability Detail
In `calculateAndClaimUnlockedCapital`:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L173-L200

We iterate over all lendingPools of `referenceLendingPools`, and since it is impossible even for the owner to remove once added lendingPools (see `ReferenceLendingPools.sol`), this array only grows.

In `_calculateClaimableAmount`:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L453-L521

we iterate over all elements of
```solidity
/// Retrieve the locked capital instances for the given lending pool
LockedCapital[] storage lockedCapitals = poolState.lockedCapitals[
    _lendingPool
];
```

## Impact
Claiming functionality becomes unusable once `lendingPools` and/or `lockedCapitals` become large enough, locking user funds.

Note: this can also affect `_assessState`:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L305

## Code Snippet

## Tool used

Manual Review

## Recommendation
Multiple remediations are possible:
- Implement `lendingPool` removal to remove expired lendingPools
- Implement a function allowing the user to restrict which lending pools they will be claiming from.