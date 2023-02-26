0x52

high

# Protection sellers can easily game withdrawal requests to collect risk free yield

## Summary

ProtectionPool#requestWithdrawal places a three period restriction for withdraw. This prevents sellers from withdrawing ahead of potential late payments or defaults. The current system however has no penalty for withdraws and sellers can queue overlapping withdraws across multiple cycles. The result is that after the first few cycles they can join for the only the open period of the cycle risk free and collect interest then leave before the pool is locked. The initial risk of these first few cycles can also be dramatically reduced, see my submission on sharing/borrowing sTokens for increased withdrawals. 

A user could abuse other quirks of the cycle system to extend their Due to how late payments are calculated the user could deposit 

## Vulnerability Detail

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L1061-L1083

_requestWithdrawal allows msg.sender to request a withdraw up to their current sToken balance. This schedules their withdraw for 2 cycles after the current period. The issues is that it doesn't check if the user has any other outstanding withdraws. This allows the user to stack a withdraw across every cycle and maintain constant liquidity. 

Example:
Imagine a cycle length of 30 days with an open period of 10 days. A user deposit 1000 USDC in cycle n and immediately request a withdraw for 1000 USDC for cycle n+2. In cycle n+1 they request a withdraw for cycle n+3. Now in cycle n+2 they request a withdraw for cycle n+4 then withdraw their tokens on day 10 of the cycle right before it locks. Now when cycle n+3 starts they deposit and make a request for cycle n+5. Before the open period of cycle n+3 closes they withdraw. They continue this cycle to collect the 10 days of free interest from each cycle.

The user could abuse other quirks of the cycle system to extend their stolen yield even if the open period is small. A pool is considered late if the debt has gone more than the standard period without being repaid. This can be combined with the fact that deposits are allowed even when a pool is locked. Now imagine that the loan receives its payment on the 15th day of the cycle. Since it would take a minimum of 30 days to become late, the user can now deposit on day 15 after the payment is made and collect risk free interest.

Submitting as high because the user gaming the withdrawals is effectively stealing yield from the legitimate insurance providers.

## Impact

Protection sellers collect risk free interest payments

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L1061-L1097

## Tool used

ChatGPT

## Recommendation

When requesting a withdraw, look at the withdraws scheduled and revert if the sum is greater than their current token amount. As an example if the current cycle is n then sum n, n+1, and n+2.