chaduke

high

# Sandwich attack to accruePremiumAndExpireProtections()

## Summary
``accruePremiumAndExpireProtections()`` will increase ``totalSTokenUnderlying``, and thus increase the exchange rate of the ``ProtectionPool``. A malicious user can launch a sandwich attack and profit. This violates the ``Fair Distribution`` principle of the protocol: 
[https://www.carapace.finance/WhitePaper#premium-pricing](https://www.carapace.finance/WhitePaper#premium-pricing)

## Vulnerability Detail
Let's show how a malicious user, Bob, can launch a sandwich attack to ``accruePremiumAndExpireProtections()`` and profit. 

1. Suppose there are 1,000,000 underlying tokens for the ``ProtectionPool``, and ``totalSupply = 1,000,000``, therefore the exchange rate is 1/1 share. Suppose Bob has 100,000 shares. 

2. Suppose ``accruePremiumAndExpireProtections()`` is going to be called and add 100,000 to ``totalSTokenUnderlying`` at L346. 

[https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L279-L354](https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L279-L354)

3) Bob front-runs ``accruePremiumAndExpireProtections()`` and calls ``deposit()`` to deposit 100,000 underlying tokens into the contract. The check for ``ProtectionPoolPhase`` will pass for an open phase. As a result, there are 1,100,000 underlying tokens, and 1,100,000 shares, the exchange rate is still 1/1 share. Bob now has 200,000 shares. 
 
```javascript
 function deposit(uint256 _underlyingAmount, address _receiver)
    external
    override
    whenNotPaused
    nonReentrant
  {
    _deposit(_underlyingAmount, _receiver);
  }

  function _deposit(uint256 _underlyingAmount, address _receiver) internal {
    /// Verify that the pool is not in OpenToBuyers phase
    if (poolInfo.currentPhase == ProtectionPoolPhase.OpenToBuyers) {
      revert ProtectionPoolInOpenToBuyersPhase();
    }

    uint256 _sTokenShares = convertToSToken(_underlyingAmount);
    totalSTokenUnderlying += _underlyingAmount;
    _safeMint(_receiver, _sTokenShares);
    poolInfo.underlyingToken.safeTransferFrom(
      msg.sender,
      address(this),
      _underlyingAmount
    );

    /// Verify leverage ratio only when total capital/sTokenUnderlying is higher than minimum capital requirement
    if (_hasMinRequiredCapital()) {
      /// calculate pool's current leverage ratio considering the new deposit
      uint256 _leverageRatio = calculateLeverageRatio();

      if (_leverageRatio > poolInfo.params.leverageRatioCeiling) {
        revert ProtectionPoolLeverageRatioTooHigh(_leverageRatio);
      }
    }

    emit ProtectionSold(_receiver, _underlyingAmount);
 }
```
4) Now ``accruePremiumAndExpireProtections()``gets  called and 100,000  is added to  ``totalSTokenUnderlying`` at L346. As a result, we have 1,200,000 underlying tokens with 1,100,000 shares. The exchange rate becomes 12/11 share. 

5) Bob calls the ``withdraw()`` function (assume he made a request two cycles back, he could do that since he had 100,000 underlying tokens in the pool) to withdraw 100,000 shares and he will get ``100,000*12/11 = 109,090`` underlying tokens. So he has a profit of 9,090 underlying tokens by the sandwich attack. 

## Impact
A malicious user can launch a sandwich attack to ``accruePremiumAndExpireProtections()``and profit. 


## Code Snippet
See above

## Tool used
VScode

Manual Review

## Recommendation
- Create a new contract as a temporary place to store the accrued premium, and then deliver it to the ``ProtectionPool`` over a period of time (delivery period) with some ``premiumPerSecond``  to lower the incentive of a quick profit by sandwich attack. 
- Restrict the maximum deposit amount for each cycle. 
- Restrict the maximum withdraw amount for each cycle.

