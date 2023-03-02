0xmuxyz

high

# `default payouts` and `locked capital` would not be subtracted from `total seller deposits + premium accrued`, which lead to miscalculation of the actual `claimable unlocked capital` to be transferred into the Protection Seller

## Summary
According to the document, `default payouts` and `locked capital` are supposed to be subtracted from `total seller deposits + premium accrued` like this:
> total capital = total seller deposits + premium accrued - locked capital - default payouts

However, through entire calculation process above, 
the `default payouts` and the `locked capital` would not be subtracted from the `total seller deposits + premium accrued`. 

This lead to miscalculation of the actual `claimable unlocked capital` to be transferred into the Protection Seller. As a result, the Protection Seller can receive the premium that is more than actual premium receivable.

## Vulnerability Detail
ProtectionPool# `claimUnlockedCapital()`,
`_claimableAmount` is calculated via the DefaultStateManager# `calculateAndClaimUnlockedCapital()`
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L433-L434
```solidity
  function claimUnlockedCapital(address _receiver)  /// @audit info - A caller (msg.sender) is a "Seller"
    external
    override
    whenNotPaused
  {
    /// Investors can claim their total share of released/unlocked capital across all lending pools
    uint256 _claimableAmount = defaultStateManager
      .calculateAndClaimUnlockedCapital(msg.sender);  /// @audit

    if (_claimableAmount > 0) {
      console.log(
        "Total sToken underlying: %s, claimableAmount: %s",
        totalSTokenUnderlying,
        _claimableAmount
      );
      /// transfer the share of unlocked capital to the receiver
      poolInfo.underlyingToken.safeTransfer(_receiver, _claimableAmount);
    }
  }
```

Within the DefaultStateManager# `calculateAndClaimUnlockedCapital()`,
`_unlockedCapitalPerLendingPool` is calculated via the DefaultStateManager# `_calculateClaimableAmount()`
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L187-L190
```solidity
  /// @dev This method is only callable by a protection pool
  function calculateAndClaimUnlockedCapital(address _seller)
    external
    override
    returns (uint256 _claimedUnlockedCapital)
  {
    /// Get the state of the pool by looking up the index in the mapping from sender address
    ProtectionPoolState storage poolState = protectionPoolStates[
      protectionPoolStateIndexes[msg.sender]  /// @audit info - A caller (msg.sender) is a ProtectionPool
    ];

    /// Only assess the state if the protection pool is registered
    if (poolState.updatedTimestamp == 0) {
      revert ProtectionPoolNotRegistered(msg.sender);
    }

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
      (
        uint256 _unlockedCapitalPerLendingPool,  /// @audit 
        uint256 _snapshotId
      ) = _calculateClaimableAmount(poolState, _lendingPool, _seller); /// @audit 
      _claimedUnlockedCapital += _unlockedCapitalPerLendingPool;

      /// update the last claimed snapshot id for the seller for the given lending pool,
      /// so that the next time the seller claims, the calculation starts from the last claimed snapshot id
      poolState.lastClaimedSnapshotIds[_lendingPool][_seller] = _snapshotId;

      unchecked {
        ++_lendingPoolIndex;
      }
    }
  }
```

Within the the DefaultStateManager# `_calculateClaimableAmount()`,
`_claimableUnlockedCapital` is calculated and returned like this:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L502-L505
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
        _claimableUnlockedCapital = /// @audit
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

According to the document, `default payouts` and `locked capital` are supposed to be subtracted from `total seller deposits + premium accrued` like this:
> total capital = total seller deposits + premium accrued - locked capital - default payouts

Within the the DefaultStateManager# `_calculateClaimableAmount()` above, the `_claimableUnlockedCapital` is equal to the result of `total seller deposits + premium accrued`.

Thus, `default payouts` and `locked capital` are supposed to be subtracted from  the `_claimableUnlockedCapital`.

However, through entire calculation process above, 
`default payouts` and `locked capital` would not be subtracted from the `_claimableUnlockedCapital` (`total seller deposits + premium accrued`). 

This lead to miscalculation of the actual `claimable unlocked capital` to be transferred into the Protection Seller. 

## Impact
This lead to miscalculation of the actual `claimable unlocked capital` to be transferred into the Protection Seller. As a result, the Protection Seller can receive the premium that is more than actual premium receivable.

## Code Snippet
- https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L433-L434
- https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L187-L190
- https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L502-L505

## Tool used
Manual Review

## Recommendation
Consider adding the calculation that `default payouts` and `locked capital` would be subtracted from the `_claimableUnlockedCapital` (`total seller deposits + premium accrued`) within the DefaultStateManager# `_calculateClaimableAmount()` like this:
(NOTE：both `locked capital (LOCKED_CAPITAL)` and `default payouts (DEFAULT_PAYOUTS)` used below have to be calculated in advance)
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
        /// The claimable amount for the given seller is proportional to the seller's share of the total supply at the snapshot
        /// claimable amount = (seller's snapshot balance / total supply at snapshot) * locked capital amount
        _claimableUnlockedCapital =
          (_poolSToken.balanceOfAt(_seller, _snapshotId) *
            lockedCapital.amount) /
          _poolSToken.totalSupplyAt(_snapshotId);


        /// @audit - Consider adding the calculation like this: 
+       _claimableUnlockedCapital = _claimableUnlockedCapital - LOCKED_CAPITAL - DEFAULT_PAYOUTS

        /// Update the last claimed snapshot id for the seller
        _latestClaimedSnapshotId = _snapshotId;

        console.log(
          "Claimable amount for seller %s is %s",
          _seller,
          _claimableUnlockedCapital
        );
      }
      ...
```
