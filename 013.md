csanuragjain

medium

# User may lose protection due to paused contract

## Summary
User is not allowed to renew protection if contract is paused. This becomes a problem because renewal is only allowed till grace period.

## Vulnerability Detail
1. Lets say User protection was expiring on timestamp X and user wanted to renew it
2. User has time till X+Y (Y being the grace period)
3. User renew the protection at say X+Y-10 (within grace period) by calling `renewProtection` function

```solidity
function renewProtection(
    ProtectionPurchaseParams calldata _protectionPurchaseParams,
    uint256 _maxPremiumAmount
  ) external override whenNotPaused nonReentrant {
...
}
```

4. Since contract was paused so `whenNotPaused` modifier fails and User is unable to renew
5. Lets say Admin unpause after X+Y timestamp
6. User cannot renew now as grace period is over


## Impact
If pause is long enough then User will lose access to renew his protection due to contract's fault

## Code Snippet
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L179

## Tool used
Manual Review

## Recommendation
Calculate the time difference between pausing/unpausing of contract. Extend the grace period temporarily by that time so that User may renew their protection in a fairly given time