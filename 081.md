immeas

high

# possible race condition between `ProtectionPool::withdraw` and `DefaultStateManager::assessState`

## Summary
If a protection seller correctly predicts a loan to default/late on payment and requested a withdrawal two cycles ago, their withdrawal can get front run with `assessState` to burn their `sTokens`.

## Vulnerability Detail
Alice is a protection seller with a pending withdrawal for the current cycle. Alice was good at predicting that a loan was going to go late and does a `withdraw`

Anyone can call `DefaultStateManager::assessState` (batch or all). Bob sees this in the mempool and either front runs Alice or just gambles that his tx will be included first by calling `assessState`.

`assessState` will call `lockCapital` which locks `totalSTokenUnderlying`, reducing or completely removing Alice share. Alice will have unwantingly burnt `sTokens`. Since given that the funds are locked Alice might have chosen to bet that the borrower will make the payment and Alice then could get her funds when they are unlocked.

## Impact
Worst case a protection seller could lose all their funds they wanted to withdraw or get less than expected. This could benefit another seller of protection who bets that the borrower will make the payment and thus the pool will return back to active and thus get a larger share of the then unlocked funds or a buyer of protection who wants to make sure they will get paid when the loan defaults. 

## Code Snippet
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L226-L275

## Tool used
Manual Review

## Recommendation
I recommend adding a minimum amount expected when doing `withdraw`.