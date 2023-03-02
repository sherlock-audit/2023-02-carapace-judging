ast3ros

high

# # [H-02] Protection seller could front-run DefaultStateManager to withdraw funds which is supposed to be locked.

## Summary

Protection sellers can running away when a default event is likely to happen.
Protection sellers could enjoy risk-free premium and do not lose fund when default event happens. Because it could front-run the DefaultStateManager and withdraw the funds before the DefaultStateManager calls `assessState` and change the state to late and lock fund. It can happens if the lending pool is late when the protection pool cycle is in `open` period.

## Vulnerability Details

When DefaultStateManager calls `DefaultStateManager.assessStates` daily, the state of each lending pool is updated. The lending pool is moved to locked state and capital is also locked.

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L324-L332

In case the state of the lending pool is change to late when the protection pool is in open period, a protection seller could identify the late state of landing pool earlier than the DefaultStateManager and can withdraw all the underlying amount from the protection pool before the capital is locked.

The requestWithdrawal could be created continuously at each cycle period without checking how much requested amount is outstanding. 


POC: He could do it as followed:

- At the beginning of each cycle, he creates a `requestWithdrawal`. He can request to withdraw all of the balance at the requested time.
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L1062-L1065

- When a lending pool in the protection pool that he sells protection is late, he can know it by listening to events or has a cronjob that call the lending pool more frequent to get the status earlier than `DefaultStateManager` (because DefaultStateManager only calls daily).
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L119

- If the time lending pool has late status is within the `open` period (pool cycle), he could call `ProtectionPool.withdraw` function to withdraw all of his balance. It happens before DefaultStateManager can lock the capital.
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L226

- He incurs no lost and can enjoy the previous premium.

## Impact

The protection seller can avoid being exposed to default risk at the expense of the protection buyers. Protection buyers will incurs lose because the underlying assets is less for claim.

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/DefaultStateManager.sol#L324-L332
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L1061-L1097


## Tool used

Manual

## Recommendation

Add checking how much requestWithdrawal is outstanding and total requestWithdrawal amount cannot be over total balance of users. A user cannot create requestWithdrawal if at the current pool cycle, the total withdraw amount of all outstanding requests (requests created in the last 2 cycles + current cycle) are more than total balance of users.