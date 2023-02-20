sorrynotsorry

high

# Snapshots can be arbitrarily overwritten and users will not be able to claim for their previous snapshots.

## Summary
Snapshots can be arbitrarily overwritten and users will not be able to claim for their previous snapshots.
## Vulnerability Detail
`DefaultStateManager` contract has `calculateAndClaimUnlockedCapital` function to calculate and return the total claimable amount from all locked capital instances in a given protection pool for a user address and marks the unlocked capital as **claimed**.

The NATSPEC stated that the method is only callable by a protection pool.
> @dev This method is only callable by a protection pool
[NATSPEC](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L157)

However, there is no modifier or caller sanitization for the function. So it can be called by anyone with an arbitrary existing `address _seller` input and bricks the claim ability of the unlocked funds for the `_seller`.

Execution,

1. The caller calls the `calculateAndClaimUnlockedCapital` function with any valid `address _seller` input.
2. The function gets the state of the pool by looking up the index in the mapping from` msg.sender`
3. On line #174, it gets the list of all lending pools for the protection pool
4. On line #183, it iterates through all lending pools for a given protection pool and calculate the total claimable amount for the arbitrarily input `_seller` and it internally calls `_calculateClaimableAmount`
5. As per the [NATSPEC](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L445-L446) `_calculateClaimableAmount` calculates the claimable amount across all locked capital instances for the given seller address for a given lending pool.
**And locked capital can be only claimed when it is released and has not been claimed before.**
6. On line #466, the function retrieves the last claimed snapshot id for the `_seller` from storage, not the `msg.sender`
7. On line #471, the function retrieves the locked capital instances for the given lending pool
8. On line #479, the function retrieves the `_snapshotId` for the lockedCapitals
9. On line #508, the function finally updates the last claimed snapshot id for the `_seller` and overwrites the previous one. In addition, there won't be transfer of funds to be executed as in `ProtectionPool::claimunlockedCapital` 
10. When the user whose address was passed as `_seller` calls `ProtectionPool::claimunlockedCapital` to claim user funds, the above scenario will execute until the 8th step. And since the `_snapshotId` is overwritten by an arbitrary call, the user will not be eligible to be paid for the previous snapshots.


## Impact
Loss of user funds, bricking system functionality.

## Code Snippet
```solidity
  function calculateClaimableUnlockedAmount(
    address _protectionPool,
    address _seller
  ) external view override returns (uint256 _claimableUnlockedCapital) {
    ProtectionPoolState storage poolState = protectionPoolStates[
      protectionPoolStateIndexes[_protectionPool]
    ];

    /// Calculate the claimable amount only if the protection pool is registered
    if (poolState.updatedTimestamp > 0) {
      /// Get the list of all lending pools for the protection pool
      address[] memory _lendingPools = poolState
        .protectionPool
        .getPoolInfo()
        .referenceLendingPools
        .getLendingPools();

      /// Iterate through all lending pools for a given protection pool
      /// and calculate the total claimable amount for the seller
      uint256 _length = _lendingPools.length;
      for (uint256 _lendingPoolIndex; _lendingPoolIndex < _length; ) {
        address _lendingPool = _lendingPools[_lendingPoolIndex];

        /// Calculate the claimable amount across all the locked capital instances for a given protection pool
        (uint256 _unlockedCapitalPerLendingPool, ) = _calculateClaimableAmount(
          poolState,
          _lendingPool,
          _seller
        );

        /// add the unlocked/claimable amount for the given lending pool to the total claimable amount
        _claimableUnlockedCapital += _unlockedCapitalPerLendingPool;

        unchecked {
          ++_lendingPoolIndex;
        }
      }
    }
  }
```
```solidity
  function _calculateClaimableAmount(
    ProtectionPoolState storage poolState,
    address _lendingPool,
    address _seller
  )
    internal
    view
    returns (
      uint256 _claimableUnlockedCapital,
      uint256 _latestClaimedSnapshotId
    )
  {
    /// Retrieve the last claimed snapshot id for the seller from storage
    uint256 _lastClaimedSnapshotId = poolState.lastClaimedSnapshotIds[
      _lendingPool
    ][_seller];

    /// Retrieve the locked capital instances for the given lending pool
    LockedCapital[] storage lockedCapitals = poolState.lockedCapitals[
      _lendingPool
    ];

    /// Iterate over the locked capital instances and calculate the claimable amount
    uint256 _length = lockedCapitals.length;
    for (uint256 _index = 0; _index < _length; ) {
      LockedCapital storage lockedCapital = lockedCapitals[_index];
      uint256 _snapshotId = lockedCapital.snapshotId;

      console.log(
        "lockedCapital.locked: %s, amt: %s",
        lockedCapital.locked,
        lockedCapital.amount
      );

      /// Verify that the seller does not claim the same snapshot twice
      if (!lockedCapital.locked && _snapshotId > _lastClaimedSnapshotId) {
        ERC20SnapshotUpgradeable _poolSToken = ERC20SnapshotUpgradeable(
          address(poolState.protectionPool)
        );

        console.log(
          "balance of seller: %s, total supply: %s at snapshot: %s",
          _poolSToken.balanceOfAt(_seller, _snapshotId),
          _poolSToken.totalSupplyAt(_snapshotId),
          _snapshotId
        );


        /// The claimable amount for the given seller is proportional to the seller's share of the total supply at the snapshot
        /// claimable amount = (seller's snapshot balance / total supply at snapshot) * locked capital amount
        _claimableUnlockedCapital =
          (_poolSToken.balanceOfAt(_seller, _snapshotId) *
            lockedCapital.amount) /
          _poolSToken.totalSupplyAt(_snapshotId);

        /// Update the last claimed snapshot id for the seller
        _latestClaimedSnapshotId = _snapshotId;

        console.log(
          "Claimable amount for seller %s is %s",
          _seller,
          _claimableUnlockedCapital
        );
      }

      unchecked {
        ++_index;
      }
    }
  }
```

## Tool used

Manual Review

## Recommendation
The team might consider to implement a modifier to ensure that the call comes from the ProtectionPool contract as stated at the NATSPEC.