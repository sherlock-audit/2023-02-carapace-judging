rvierdiiev

medium

# Pausing can prevent user from renewing protection

## Summary
Pausing can prevent user from renewing or withdrawing
## Vulnerability Detail
ProtectionPool has ability to [be paused](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L452) by owner.
In case, when paused most of functions that users can use are blocked.
Among them `withdraw` and `renewProtection` functions. 

When user wants to renew protection [he has some time](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L390-L397) after his old protection has finished. In case if he is late, then he will lose chance to continue protection. It's possible that contract will be paused during that period and user will not be able to continue his protection after unpausing.
## Impact
User loses chance to continue protection.
## Code Snippet
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L390-L397
## Tool used

Manual Review

## Recommendation
User should not lose that ability because of pausing.