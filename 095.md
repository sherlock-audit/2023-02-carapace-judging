rvierdiiev

medium

# defaultStateManager.getLendingPoolStatus can be stale which allows user to buy/renew protection when he should not

## Summary
defaultStateManager.getLendingPoolStatus can be stale which allows user to buy/renew protection when he should not
## Vulnerability Detail
When user wants to buy/renew protection then some [checks are done](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L802-L810). 
One of them is to [check if pool is active](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L63-L67). This check will just [fetch lending pool status](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L412-L415) from `DefaultStateManager` and will revert if it's not active.

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L273-L281
```solidity
  function getLendingPoolStatus(
    address _protectionPoolAddress,
    address _lendingPoolAddress
  ) external view override returns (LendingPoolStatus) {
    return
      protectionPoolStates[protectionPoolStateIndexes[_protectionPoolAddress]]
        .lendingPoolStateDetails[_lendingPoolAddress]
        .currentStatus;
  }
```
As you can see when you fetch status, it's just use already stored status.
`DefaultStateManager._assessState` function is responsible for changing status for specific lending pool.

It's possible that the status has already changed from active to late when new user wants to buy protection. And this function should revert. But because, `assessStateBatch` is not called for that protection pool, status for lending pool was not changed and protection was sold.
## Impact
Protection is sold to user, when status of lending pool is changed to late, which means that pool can be defaulted soon.
## Code Snippet
Provided above
## Tool used

Manual Review

## Recommendation
You need to update lending pool status when selling protection in order to detect not active status.