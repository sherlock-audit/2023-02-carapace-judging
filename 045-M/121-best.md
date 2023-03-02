rvierdiiev

high

# In case if pool state is changing from late to active, locked funds should be returned to pool, as leverage ratio is decreased now

## Summary
In case if pool state is changing from late to active, locked funds should be returned to pool, as leverage ratio is decreased now
## Vulnerability Detail
When lending pool is late in payment, then capital that equals to amount that is needed to cover protections for that pool, [is locked](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L415-L422).
After that protocol waits some time(`_getTwoPaymentPeriodsInSeconds`) and there can be 2 options. If payment was not done, then lending pool has defaulted and protection buyers will receive their payment.
Another option is when payment was done and lending pool state becomes active again. In this case `_moveFromLockedToActiveState` function [is called](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L351).

This function will [unlock locked capital](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L435) and then depositors will be able to call `ProtectionPool.claimUnlockedCapital` which will transfer them part of their deposited funds without withdraw request.
Total amount that will be sent to the users is equal to locked capital that was unlocked.
That means that after lending pool state has changed from late to active, protection pool still needs to cover protection, but it have lost amount of funds that fully backs protections of that lending pool.

This is not good for the protocol as he needs those funds back in order to have healthy leverage ratio. After such incident is unlikely that those people will deposit their unlocked funds back.

Scenario.
1.Protection pool has 10 million usdc inside and 5 lending pools to cover, 20 million in total(4 million each).
2.One lending pool is late, so 4 million usdc is locked. Now pool has 6 million.
3.Payment was done, so lending pool is active again, but locked 4 millions were not returned to the pool.
4.As result now pool has 6 millions to cover 20 millions protections. Big part of funds were withdrawn.
## Impact
Protocol protection funds amount decreases by locked capital, however lending pool is active and needs coverage.
## Code Snippet
Provided above
## Tool used

Manual Review

## Recommendation
Think about the way, how to deposit funds back to the pool evenly among people who participated in capital locking.