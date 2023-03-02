clems4ever

medium

# Protection buys can happen when _hasMinRequiredCapital is false

## Summary
After protection sellers withdrawals, the protection pool may end up with `totalSTokenUnderlying < poolInfo.params.minRequiredCapital`. The documentation says that buyers should not be able to buy protection in that case but it is not checked in `buyProtection` once the pool is already open.

## Vulnerability Detail
We can see here:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L533

That `_hasMinRequiredCapital` is only checked to make the state transition, but later it is not checked before a buyer buys protection

## Impact
Protection buys may happen even if `_hasMinRequiredCapital` is false, provided leverage ratio boundaries are preserved.

## Code Snippet

## Tool used

Manual Review

## Recommendation
Either lock (`OpenToSellers`) the pool when `totalSTokenUnderlying < poolInfo.params.minRequiredCapital` or check `_hasMinRequiredCapital` on protection buy.