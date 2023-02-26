rvierdiiev

medium

# If noone called ProtectionPoolCycleManager.calculateAndSetPoolCycleState during the cycle, then cycle calculation is broken

## Summary
If noone called ProtectionPoolCycleManager.calculateAndSetPoolCycleState during the cycle, then cycle calculation is broken. Because of that users will have to wait more time in order to withdraw.
## Vulnerability Detail
ProtectionPoolCycleManager.calculateAndSetPoolCycleState function is responsible for changing cycles and their states. When cycle is locked and cycle duration has passed, then [new cycle is started](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/ProtectionPoolCycleManager.sol#L133-L137).

Cycles are very important in the system as they control when users can buy protection, when they can withdraw.
For example when user creates withdraw request, then he will be able to withdraw in 2 cycles.

`ProtectionPoolCycleManager.calculateAndSetPoolCycleState` function is called when someone [withdraws](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L104-L105) or when new [protection is bought](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L462). Also this function can be called directly.

But it's also possible that users will be not active for some time, so noone will call ProtectionPoolCycleManager.calculateAndSetPoolCycleState. As result, cycle calculation will be broken.

Example.
1. Cycle duration is 90 days.
2.At cycle 1 user request a withdraw. So he will be able to withdraw at 3 cycle, which will be started at 181 day.
3.During next 100 days noone called ProtectionPoolCycleManager.calculateAndSetPoolCycleState.
4.User who wants to withdraw on 181 day, can't do that as current cycle is 2 now.
## Impact
Cycle calculation is broken.
## Code Snippet
Provided above
## Tool used

Manual Review

## Recommendation
Should be called regularly.