ctf_sec

medium

# Front-runnable state update for lending pool

## Summary

Front-runnable state update for lending pool

## Vulnerability Detail

In the current implementation, the lending pool state needs to be manually called:

```solidity
  /// @inheritdoc IDefaultStateManager
  function assessStates() external override {
    /// gas optimizations:
    /// 1. capture length in memory & don't read from storage for each iteration
    /// 2. uncheck incrementing pool index
    uint256 _length = protectionPoolStates.length;

    /// assess the state of all registered protection pools except the dummy pool at index 0
    for (uint256 _poolIndex = 1; _poolIndex < _length; ) {
      _assessState(protectionPoolStates[_poolIndex]);
      unchecked {
        ++_poolIndex;
      }
    }

    emit ProtectionPoolStatesAssessed();
  }
```

Only after this assetState function is called, the lending pool state is modified, and the state can change from active to late to default to expired.

According to the documentation:

https://www.carapace.finance/docs/protocol-mechanics/protection_buyers#new-protection

> A buyer can only buy new protection within 90 days after a lending pool is added to our pool. After that point, they will not be able to purchase protection. Existing lenders cannot buy protection anytime they want. Otherwise, they would buy protection right before the missed payment. Since credit default swaps exist to deal with uncertainty, we cannot allow them to buy when they are certain that a borrower is gonna default.

But if the pool goes to default within 90 days, it is fairly easy for the buyer to monitor the assetState function call and front-run the assetState function call, and right before the lending pool default, the buyer can the buy the protection. The issue is that the preimum paid will have no time to go to the protection sellers and protection sellers earns no premium if such frontrunning happens.

When the pool moves from active to late state, the capital provided by the protection sellers is locked.

But the protection sellers can monitor the state up function call and right before the pool mobes from active to late state and right before their capital get locked, the protection seller can use SToken to request withdraw if the protection sellers happens to call request withdrawal prior to 2 cycle before (meaning they can withdraw in the current cycle). This is not fair for buyers that pay the premium.

## Impact

Buyer can front run the state up from late to default to purchase the protection before the default and pay no premium to protection sellers.

Protection sellers can earn premium from the buyer and frontrun the state update from active to late to avoid locking their capital to cover the default.

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L284-L383

## Tool used

Manual Review

## Recommendation

Calling state update (_assetState) every time before buyer purchase the protection and pay the premium and before the seller deposit fund or request withdraw or withdraw to make sure the lending pool state is updated first.

