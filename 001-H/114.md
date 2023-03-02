clems4ever

high

# Dos due to unbounded array of active protections may prevent locking of capital

## Summary
An user can take an unlimited number of protections for a given `lendingPool`. However when locking capital in case of late payment of a loan, the function `lockCapital` iterates over all active protections to determine the amount of capital to lock.

This means that a malicious user can prevent capital from being locked by buying multiple protections for a very small amount, stuffing the array of active protections and causing `lockCapital` to revert with OUT-OF-GAS.

## Vulnerability Detail
We can see in the function `lockCapital` in `ProtectionPool.sol`:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L325-L355

And any user having lended on Goldfinch can add an entry in the array by buying a protection:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L822-L828

## Impact
A depositor can use this vulnerability to enjoy a risk-free yield, since their capital will never be locked and they can withdraw once enough cycles have passed.

## Code Snippet

## Tool used

Manual Review

## Recommendation
Add a parameter to the function to be able to limit the number of active protections the call iterates upon, to not hit the OUT-OF-GAS limit.