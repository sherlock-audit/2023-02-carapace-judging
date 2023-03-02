yixxas

high

# Deposits can be made even if pool is locked

## Summary
Missing `whenPoolIsOpen` modifier allows users to deposit even when pool is locked.

## Vulnerability Detail
According to the doc specs,

> enum ProtectionPoolCycleState {
  None, // The cycle state for unregistered pools.
  Open, // The cycle is open for deposit & withdraw
  Locked // The cycle is in progress & locked for deposit & withdraw
  }

We see that there are 3 states for a cycle. When a pool is in Locked state, users should not be able to deposit. This is an important invariant that is broken. Decisions that are made based on this assumption can affect many parts of the protocol.



## Impact
Important invariant of blocking deposits and withdrawals when cycle state is locked is broken.

## Code Snippet
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L198-L205

## Tool used

Manual Review

## Recommendation
Consider adding the modifier `whenPoolIsOpen` to `deposit()`.
