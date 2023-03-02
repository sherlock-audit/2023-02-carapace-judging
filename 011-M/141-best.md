peanuts

medium

# Sellers should be able to withdraw when protocol is paused

## Summary

Sellers should be able to withdraw when protocol is paused.

## Vulnerability Detail

The protocol uses the pausing functionality for deposit and withdrawal, assumably for security reasons. However, withdrawals should never be paused because it affects the decentralization nature of the blockchain. In other words, protocol should not block any form of withdrawals. Being unable to withdraw in this protocol is even more detrimental because the protocol relies on time and uncertainty. If the protocol is paused and during the pause, the lending market defaults because of a hack or just a price crash (like Maple Finance in Sherlock or UST crash), then users will not be able to rescue their money.

The withdraw functions have the whenNotPaused modifier:

```solidity
  function requestWithdrawal(uint256 _sTokenAmount)
    external
    override
    whenNotPaused
  {
    _requestWithdrawal(_sTokenAmount);
  }


  /// @inheritdoc IProtectionPool
  function depositAndRequestWithdrawal(
    uint256 _underlyingAmountToDeposit,
    uint256 _sTokenAmountToWithdraw
  ) external virtual override whenNotPaused nonReentrant {
    _deposit(_underlyingAmountToDeposit, msg.sender);
    _requestWithdrawal(_sTokenAmountToWithdraw);
  }


  /// @inheritdoc IProtectionPool
  function withdraw(uint256 _sTokenWithdrawalAmount, address _receiver)
    external
    override
    whenPoolIsOpen
    whenNotPaused
    nonReentrant
  {
```

## Impact

Sellers are unable to withdraw after requesting a withdrawal if the protocol is paused, which may affect seller's money if the lending market defaults during the pause.

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L208-L232

## Tool used

Manual Review

## Recommendation

Recommend taking out the whenNotPaused modifier for withdrawals.