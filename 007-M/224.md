0Kage

medium

# Pause/unpause can have unintended side-effects such as shortening the `RenewalGracePeriod`

## Summary
Critical functions such as `deposit`, `withdraw`, `renew`, `claimUnlockedCapital`, `requestWithdraw` are all using the `whenNotPaused` modifier. While protocol may have valid reasons for pausing the contract, this might have unintended consequences for users. 

One such scenario is when existing protection buyers have 1 day grace period remaining & the contract goes into `pause` state for that day. As a result, a protection buyer might forever lose the chance to buy protection. 

## Vulnerability Detail

## Impact
`renewProtection` uses `whenNotPaused` modifier - genuine buyer will lose out an opportunity to renew even though she is well within grace period

It is unclear from docs as to when protocol can pause/unpause. Even disregarding the centralization risk from such functions, executing a `pause` function can potentially cause irreversible loss for a genuine protection buyer looking to renew protection (specially when fresh protection buying on that pool has stopped). 

## Code Snippet
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L179

## Tool used
Manual Review

## Recommendation
Extend grace period for all buyers who are falling in the `pause` window. Or consider removing `whenNotPaused` modifier for `renewProtection`