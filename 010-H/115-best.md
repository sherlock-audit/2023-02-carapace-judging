clems4ever

high

# Seller may bypass the 2 cycles safeguard after initial 2 cycles

## Summary
Carapace has a safeguard which prevents protection sellers to sell instantly, by delaying any withdrawal attempt by 2 cycles.
However any protection seller may circumvent this safeguard by requesting withdrawal for all of their funds at each cycle. This way they will be able to withdraw all of their funds instantly 2 cycles after initial deposit.
They can later use this to front run locking of capital for example, and eliminate their risk on the protocol. 

## Vulnerability Detail
in `_requestWithdrawal`:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L989-L1027

Provided the depositor has enough SToken, they may request a withdrawal for 2 cycles later. However they are not committed in any way to withdraw 2 cycles later, and can request withdrawal again on next cycle. By pipelining requests in this way, it is easy to see that after the second cycle they have the ability to withdraw instantly at any cycle.

Using this they may frontrun an attempt from the owner to lock the funds, and avoid the slashing of their funds (they can monitor onchain data from goldfinch directly and detect default before keepers take action on Carapace).

## Impact
The protocol may not be able to provide adequate locking of funds, and protection buyers would be rugged.

## Code Snippet

## Tool used

Manual Review

## Recommendation
Restrict depositor ability to create new withdrawal accross all cycles if they have an ongoing request.