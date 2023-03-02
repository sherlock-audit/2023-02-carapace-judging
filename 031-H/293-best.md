0x52

high

# User can game protection via renewal to get free insurance

## Summary

When renewing a position, the new protectionAmount can be higher than what was previously bought. A user can abuse this to get insurance for free. Most of the time they would keep the protection amount at 1 and pay virtually no premium. Since late payments can be seen very far in advance they would simply renew their insurance at the max value of token right before the borrower was officially late and gain the full protection.

## Vulnerability Detail

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/ProtectionPoolHelper.sol#L383-L398

When evaluating if a user can renew their insurance only the time, token and lending contract are verified. It never checks the amount of protection that the user is renewing for. This can be abused to renew for MORE protection than originally bought. A user could abuse this to renew right before there was a late payment for the full amount of protection.

They can abuse another quirk of the renewal system to make sure they they are always able to renew at any time. Since a user is allowed to open an unlimited number of positions on a single LP token they can open a large number of positions with 1 protection amount. They would space out each protection to expire exactly with the grace period. The results it that they would be able to renew any position at a moments notice. 

They would abuse this by choosing to renew their protection for the max value of the token right before a payment was officially late. This would allow them to collect a full repayment while paying basically nothing in premium.

## Impact

User can get full protection for free

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L176-L195

## Tool used

Manual Review

## Recommendation

When renewing protection, the user should only be allowed to renew up to the value of their expired insurance