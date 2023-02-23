ctf_sec

medium

# Goldfinch lending pool can be paused, which impact the state assessment of the Carapace contract

## Summary

Goldfinch lending pool can be paused, which impact the state assessment of the Carapace contract

## Vulnerability Detail

The GoldFinch multisig can pause a lending pool and the borrower is not able to repay the debt + interest.

If the lending pool is paused for a long time, in the current implementation, the Carapace contract state manager would just mark the lending pool as payment late and even default, but it is not fair for protection sellers because it is likely when the goldfinch unpause the lending pool, the borrower can repay the debt and the lending is not default state, while the protection seller still use the capital to cover the falsely default lending pool.

## Impact

When Goldfinch lending pool can be paused, the state manager can mark a not-default lending pool to default state without offering the chance to let the borrower pay the debt after the Goldfinch unpause the contract.

## Code Snippet

https://github.com/goldfinch-eng/goldfinch-contracts/blob/162ea40e526911a5955284f76c454f655645ec30/v2.2.0/protocol/core/TranchedPool.sol#L337

The borrower is only able to pay when the contract is not paused.

```solidity
  /**
   * @notice Allows repaying the creditline. Collects the USDC amount from the sender and triggers an assess
   * @param amount The amount to repay
   */
  function pay(uint256 amount) external override whenNotPaused {
    require(amount > 0, "Must pay more than zero");
    collectPayment(amount);
    _assess();
  }
```

## Tool used

Manual Review

## Recommendation

We recommend the protocol add specific logic to not counting the time elapse towards the default state when the lending pool on Goldfinch side is paused.
