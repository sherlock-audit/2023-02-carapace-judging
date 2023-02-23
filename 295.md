ctf_sec

high

# Deposit and withdraw in protectionPool lacks of slippage control, deposit / withdraw transaction can be pending in the mempool for a long time and executes in very sub-optimal exchange rate

## Summary

Deposit and withdraw in protectionPool lacks of slippage control, deposit / withdraw transaction can be pending in the mempool for a long time and executes in very sub-optimal exchange rate

## Vulnerability Detail

The ProtectionPool contract allows users to deposit and withdraw underlying assets in exchange for sToken shares. The exchange rate between the underlying asset and sToken shares is calculated based on the total capital in the pool and the total supply of sToken shares. However, there is no slippage control mechanism in place to prevent large changes in the exchange rate, which can result in significant losses or gains for users.

The impact of slippage is amplified by the withdraw timelock, user need to put withdraw request prior to n - 2 cycle and user can withdraw in the current n cycle, there is no way for the user to know the exchange rate 2 cycles (180 days) before.

## Impact

It is possible that when user submit a withdraw / deposit transaction, the transaction is pending in the mempool for a long and before the deposit / withdraw transaction landed, other transaction executed, which impact the exchange rate.

 Without slippage control, users may experience unexpected losses or gains when depositing or withdrawing from the ProtectionPool contract. For example, if the exchange rate suddenly drops due to a large sell-off of underlying assets, users who deposit assets may receive fewer sToken shares than expected, resulting in a loss of value. Similarly, if the exchange rate suddenly increases due to a large influx of buyers, users who withdraw assets may receive more underlying assets than expected, resulting in a gain of value.

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L196-L206

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L224-L276

## Tool used

Manual Review

## Recommendation

By implementing a slippage control mechanism, users can have greater confidence in the expected value of their deposits and withdrawals, reducing the risk of unexpected losses or gains.
