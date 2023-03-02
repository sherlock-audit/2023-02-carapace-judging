__141345__

medium

# DoS when `_assessState()`

## Summary

The `activeProtectionIndexes` array could grow unbounded and result in DoS when `_assessState()`.


## Vulnerability Detail

When crate protection, there is no limit on how many protections can be created. 
```solidity
File: contracts/core/pool/ProtectionPool.sol
795:   function _verifyAndCreateProtection() {

887:     lendingPoolDetail.activeProtectionIndexes.add(_protectionIndex);
888:     protectionBuyerAccounts[msg.sender].activeProtectionIndexes.add(
889:       _protectionIndex
890:     );
```

As a result, the `activeProtectionIndexes` array could grow quite large, the transaction’s gas cost could exceed the block gas limit and make it impossible to call this function `_assessState()` at all. Since inside the for loop, there are storage load and function calls, the gas cost of these are relatively high.

```solidity
File: contracts/core/DefaultStateManager.sol
289:   function _assessState(ProtectionPoolState storage poolState) internal {

303:     uint256 _length = _lendingPools.length;
304:     for (uint256 _lendingPoolIndex; _lendingPoolIndex < _length; ) {
305:       /// Get the lending pool state details
306:       address _lendingPool = _lendingPools[_lendingPoolIndex];
307:       LendingPoolStatusDetail storage lendingPoolStateDetail = poolState
308:         .lendingPoolStateDetails[_lendingPool];

```


## Impact

The pool could fail to `_assessState()`, not able to assess states of all registered protection pools and initiate state changes & related actions as needed.

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L980-L1020

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/DefaultStateManager.sol#L303-L381

## Tool used

Manual Review

## Recommendation

Consider introducing a reasonable upper limit based on block gas limits. For large size `activeProtectionIndexes` array, the handling of assess State can be break into separate parts with different function calls, and combine the results at last in another function.
