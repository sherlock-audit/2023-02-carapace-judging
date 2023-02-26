rvierdiiev

high

# ProtectionPool.lockCapital doesn't check if protection is already expired

## Summary
ProtectionPool.lockCapital doesn't check if protection is already expired which increases locked capital. Excess amount can be locked forever.
## Vulnerability Detail
In case if lending pool is late in payment, then `lockCapital` is called for that pool.
This function will iterate over [active protection of lending pool](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L382) and will calculate [amount that should be covered](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L401-L404) by pool. 

Then it will decrease `totalSTokenUnderlying` variable with `_lockedAmount`.

The problem is that on the moment of call, some [protections from array](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L386) can already be expired, which means that protection period has ended for them.
As result, more underlying tokens are locked then needed and depending on implementation for default state(which is not done yet) this extra funds can be lost.
## Impact
More funds are locked.
## Code Snippet
Provided above.
## Tool used

Manual Review

## Recommendation
Check for expired and not started protections when calculating locked amount.