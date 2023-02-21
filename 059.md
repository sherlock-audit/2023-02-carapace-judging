sorrynotsorry

high

# Protections can be arbitrarily expired and system can be DoS'ed.

## Summary
Protections can be arbitrarily expired and the system can be DoS'ed.
## Vulnerability Detail
`ProtectionPoolHelper` contract implements `expireProtection` function in order to mark the given protection as `expired` and move it from active to expired protection indexes. This function visibility is public and there is no modifier for caller restriction. So anybody can call this function with arbitrary valid `protectionBuyerAccounts`, `protectionInfo`, `lendingPoolDetail`, and `_protectionIndex`.

The function also does not validate any timestamp to assess the expiration of the protection. By this vulnerability, it can be used to DoS the system.

The path;
1. Alice buys protection for Lending Pool A with ProtectionInfo-Alice and LendingPoolDetail-A
2. An actor calls `ProtectionPoolHelper::expireProtection` and iterates over all the existing `_protectionIndex`
3. Alice's protection gets expired before its expiry time (`protectionInfo.startTimestamp + protectionInfo.purchaseParams.protectionDurationInSeconds` )

[Code Link](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L286-L321)

## Impact
DoS, Loss of user funds

## Code Snippet
```solidity
  /**
   * @notice Marks the given protection as expired and moves it from active to expired protection indexes.
   * @param protectionBuyerAccounts storage pointer to protection buyer accounts
   * @param protectionInfo storage pointer to protection info
   * @param lendingPoolDetail storage pointer to lending pool detail
   * @param _protectionIndex The index of the protection to expire.
   */
  function expireProtection(
    mapping(address => ProtectionBuyerAccount) storage protectionBuyerAccounts,
    ProtectionInfo storage protectionInfo,
    LendingPoolDetail storage lendingPoolDetail,
    uint256 _protectionIndex
  ) public {
    /// Update protection info to mark it as expired
    protectionInfo.expired = true;


    /// remove expired protection index from activeProtectionIndexes of lendingPool & buyer account
    address _buyer = protectionInfo.buyer;
    lendingPoolDetail.activeProtectionIndexes.remove(_protectionIndex);
    ProtectionBuyerAccount storage buyerAccount = protectionBuyerAccounts[
      _buyer
    ];
    buyerAccount.activeProtectionIndexes.remove(_protectionIndex);


    /// Update buyer account to add expired protection index to expiredProtectionIndexes of lendingPool
    ProtectionPurchaseParams storage purchaseParams = protectionInfo
      .purchaseParams;
    buyerAccount.expiredProtectionIndexByLendingPool[
      purchaseParams.lendingPoolAddress
    ][purchaseParams.nftLpTokenId] = _protectionIndex;


    /// update total protection amount of lending pool by subtracting the expired protection amount
    lendingPoolDetail.totalProtection -= protectionInfo
      .purchaseParams
      .protectionAmount;
  }
```


## Tool used

Manual Review

## Recommendation
The function is called by `ProtectionPool::accruePremiumAndExpireProtections` so it can be restricted accordingly by changing the visibility to `internal` visibility.