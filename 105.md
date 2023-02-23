ctf_sec

high

# A malicious early user/attacker can manipulate the SToken's pricePerShare to take an unfair share of future users' deposits

## Summary

A malicious early user/attacker can manipulate the SToken's pricePerShare to take an unfair share of future users' deposits

## Vulnerability Detail

When the deposit in ProtectionPool.sol is called, which calls

```solidity
/// @inheritdoc IProtectionPool
function deposit(uint256 _underlyingAmount, address _receiver)
  external
  override
  whenNotPaused
  nonReentrant
{
  _deposit(_underlyingAmount, _receiver);
}
```

which calls:

```solidity
  /**
   * @dev Deposits the specified amount of underlying token to the pool and
   * mints the corresponding sToken shares to the receiver.
   * @param _underlyingAmount the amount of underlying token to deposit
   * @param _receiver the address to receive the sToken shares
   */
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

which calls:

```solidity
  /// @inheritdoc IProtectionPool
  function convertToSToken(uint256 _underlyingAmount)
    public
    view
    override
    returns (uint256)
  {
    uint256 _scaledUnderlyingAmt = ProtectionPoolHelper
      .scaleUnderlyingAmtTo18Decimals(
        _underlyingAmount,
        poolInfo.underlyingToken.decimals()
      );

    /// if there are no sTokens in the pool, return the underlying amount
    if (totalSupply() == 0) return _scaledUnderlyingAmt;

    return
      (_scaledUnderlyingAmt * Constants.SCALE_18_DECIMALS) / _getExchangeRate();
  }
```

note the implementation:

```solidity
    /// if there are no sTokens in the pool, return the underlying amount
    if (totalSupply() == 0) return _scaledUnderlyingAmt;

    return
      (_scaledUnderlyingAmt * Constants.SCALE_18_DECIMALS) / _getExchangeRate();
```

A malicious early user can deposit() with 1 wei of asset token as the first depositor of the SToken, and get 1 wei of shares.

Then the attacker can send 10000e18 - 1 of asset tokens and inflate the price per share exchange rate from 1.0000 to an extreme value of 1.0000e22 ( from (1 + 10000e18 - 1) / 1) .

As a result, the future user who deposits 19999e18 will only receive 1 wei (from 19999e18 * 1 / 10000e18) of shares token.

Basically after the first depositor manipulate the minted totalSupply, the getExchagneRate() is not in the depositor favor.

```solidity
  function _getExchangeRate() internal view returns (uint256) {
    uint256 _totalScaledCapital = ProtectionPoolHelper
      .scaleUnderlyingAmtTo18Decimals(
        totalSTokenUnderlying,
        poolInfo.underlyingToken.decimals()
      );
    uint256 _totalSTokenSupply = totalSupply();
    uint256 _exchangeRate = (_totalScaledCapital *
      Constants.SCALE_18_DECIMALS) / _totalSTokenSupply;

    console.log(
      "Total capital: %s, Total SToken Supply: %s, exchange rate: %s",
      _totalScaledCapital,
      _totalSTokenSupply,
      _exchangeRate
    );

    return _exchangeRate;
  }
```

## Impact

The attacker can profit from future users' deposits. While the late users will lose part of their funds to the attacker.

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L587-L607

## Tool used

Manual Review

## Recommendation

Consider requiring a minimal amount of share tokens to be minted for the first minter, and send a port of the initial mints as a reserve to the DAO so that the pricePerShare exchange rate can be more resistant to manipulation. 
