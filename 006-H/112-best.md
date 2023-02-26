clems4ever

high

# Protection buyer may buy multiple protections for same goldfinch NFT

## Summary
The Carapace protocol checks that a protection buyer does not buy a protection for an 
amount greater than the remainingPrincipal in the corresponding loan. 
However it possible for the buyer to buy multiple different protections for the same Goldfinch loan.

## Vulnerability Detail
The check for the possibility for a user to buy a protection is done here in `ReferenceLendingPools.canBuyProtection`:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ReferenceLendingPools.sol#L132-L168

It checks the protection about to be created does not cross remaining principal. But it still allows the user to create multiple protections for the same loan position.

## Impact
The malicious user can `overprotect` their loan position on Goldfinch and thus claim a larger amount on loan default than what they lended. For now as the default claiming feature is not implemented, they can use this bug to DOS the protocol by using all funds deposited into the protocol reaching `leverageRatioFloor` and not allowing any new protections to be bought.

## Code Snippet

## Tool used
Manual Review

## Recommendation
Keep track of the total protection subscribed for a given loan and limit total protection value to remaining capital