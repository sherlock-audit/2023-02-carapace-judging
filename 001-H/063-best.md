Ruhum

medium

# Too many active protections can cause the ProtectionPool reach the block gas limit

## Summary
There are two instances where the ProtectionPool contract loops over an unbounded array. These can cause the transaction to succeed the block gas limit causing the transaction to revert, see https://swcregistry.io/docs/SWC-128.

## Vulnerability Detail
Both in `lockCapital()` and in `_accruePremiumAndExpireProtections()` the contract loops over the unbounded array of protections. If there are too many protections the transaction will revert because it reached the block gas limit.

## Impact
Both the `lockCapital()` and `_accruePremiumAndExpireProtections()` functions are critical components of the contract. Them not being accessible renders the contract useless. Protection buyers won't be covered in case of the underlying pool defaulting because the deposited tokens can't be locked up

## Code Snippet
`lockCapital()`: https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L378-L411
```sol
    /// Iterate all active protections and calculate total locked amount for this lending pool
    /// 1. calculate remaining principal amount for each loan protection in the lending pool.
    /// 2. for each loan protection, lockedAmt = min(protectionAmt, remainingPrincipal)
    /// 3. total locked amount = sum of lockedAmt for all loan protections
    uint256 _length = activeProtectionIndexes.length();
    for (uint256 i; i < _length; ) {
      /// Get protection info from the storage
      uint256 _protectionIndex = activeProtectionIndexes.at(i);
      ProtectionInfo storage protectionInfo = protectionInfos[_protectionIndex];

      /// Calculate remaining principal amount for a loan protection in the lending pool
      uint256 _remainingPrincipal = poolInfo
        .referenceLendingPools
        .calculateRemainingPrincipal(
          _lendingPoolAddress,
          protectionInfo.buyer,
          protectionInfo.purchaseParams.nftLpTokenId
        );

      /// Locked amount is minimum of protection amount and remaining principal
      uint256 _protectionAmount = protectionInfo
        .purchaseParams
        .protectionAmount;
      uint256 _lockedAmountPerProtection = _protectionAmount <
        _remainingPrincipal
        ? _protectionAmount
        : _remainingPrincipal;

      _lockedAmount += _lockedAmountPerProtection;

      unchecked {
        ++i;
      }
    }
```

`_accruePremiumAndExpireProtections()`: https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L957-L1021
```sol
  /**
   * @dev Accrue premium for all active protections and mark expired protections for the specified lending pool.
   * Premium is only accrued when the lending pool has a new payment.
   * @return _accruedPremiumForLendingPool the total premium accrued for the lending pool
   * @return _totalProtectionRemoved the total protection removed because of expired protections
   */
  function _accruePremiumAndExpireProtections(
    LendingPoolDetail storage lendingPoolDetail,
    uint256 _lastPremiumAccrualTimestamp,
    uint256 _latestPaymentTimestamp
  )
    internal
    returns (
      uint256 _accruedPremiumForLendingPool,
      uint256 _totalProtectionRemoved
    )
  {
    /// Get all active protection indexes for the lending pool
    uint256[] memory _protectionIndexes = lendingPoolDetail
      .activeProtectionIndexes
      .values();

    /// Iterate through all active protection indexes for the lending pool
    uint256 _length = _protectionIndexes.length;
    for (uint256 j; j < _length; ) {
      uint256 _protectionIndex = _protectionIndexes[j];
      ProtectionInfo storage protectionInfo = protectionInfos[_protectionIndex];

      /// Verify & accrue premium for the protection and
      /// if the protection is expired, then mark it as expired
      (
        uint256 _accruedPremiumInUnderlying,
        bool _expired
      ) = ProtectionPoolHelper.verifyAndAccruePremium(
          poolInfo,
          protectionInfo,
          _lastPremiumAccrualTimestamp,
          _latestPaymentTimestamp
        );
      _accruedPremiumForLendingPool += _accruedPremiumInUnderlying;

      if (_expired) {
        /// Add removed protection amount to the total protection removed
        _totalProtectionRemoved += protectionInfo
          .purchaseParams
          .protectionAmount;

        ProtectionPoolHelper.expireProtection(
          protectionBuyerAccounts,
          protectionInfo,
          lendingPoolDetail,
          _protectionIndex
        );
        emit ProtectionExpired(
          protectionInfo.buyer,
          protectionInfo.purchaseParams.lendingPoolAddress,
          protectionInfo.purchaseParams.protectionAmount
        );
      }

      unchecked {
        ++j;
      }
    }
  }
```

## Tool used

Manual Review

## Recommendation
You either have to limit the number of protections so that it is impossible that you surpass the block gas limit. Or, you change the logic so that you're never forced to loop over all the existing protections.
