unforgiven

high

# Function PremiumCalculator.calculatePremium() would use wrong premium rate when leverageRatio<Pool.leverageRatioFloor which can cause fund loss

## Summary
Function calculatePremium() calculates premium and when the leverageRatio is not between the floor and ceiling code would use `Poll.minCarapaceRiskPremiumPercent` as `carapacePremiumRateToUse` and would return the minimum premium but when `leverageRatio < Pool.leverageRatioFloor` the risk is very high and code should return the highest premium.

## Vulnerability Detail
This is `calculatePremium()` code in PremiumCalculator:
```solidity
  function calculatePremium(
    uint256 _protectionDurationInSeconds,
    uint256 _protectionAmount,
    uint256 _protectionBuyerApy,
    uint256 _leverageRatio,
    uint256 _totalCapital,
    ProtectionPoolParams calldata _poolParameters
  )
    external
    view
    virtual
    override
    returns (uint256 _premiumAmount, bool _isMinPremium)
  {
    console.log(
      "Calculating premium... protection duration in seconds: %s, protection amount: %s, leverage ratio: %s",
      _protectionDurationInSeconds,
      _protectionAmount,
      _leverageRatio
    );

    int256 _carapacePremiumRate;

    /// Calculate the duration in years
    uint256 _durationInYears = _calculateDurationInYears(
      _protectionDurationInSeconds
    );

    /// Verify if the risk factor can be calculated
    if (
      RiskFactorCalculator.canCalculateRiskFactor(
        _totalCapital,
        _leverageRatio,
        _poolParameters.leverageRatioFloor,
        _poolParameters.leverageRatioCeiling,
        _poolParameters.minRequiredCapital
      )
    ) {
      int256 _riskFactor = RiskFactorCalculator.calculateRiskFactor(
        _leverageRatio,
        _poolParameters.leverageRatioFloor,
        _poolParameters.leverageRatioCeiling,
        _poolParameters.leverageRatioBuffer,
        _poolParameters.curvature
      );

      /// Calculate the carapace premium rate based on the calculated risk factor
      _carapacePremiumRate = _calculateCarapacePremiumRate(
        _durationInYears,
        _riskFactor
      );
      console.logInt(_carapacePremiumRate);
    } else {
      /// This means that the risk factor cannot be calculated because of either
      /// min capital not met or leverage ratio out of range.
      /// Hence, the premium is the minimum premium
      _isMinPremium = true;
    }

    int256 _minCarapaceRiskPremiumPercent = int256(
      _poolParameters.minCarapaceRiskPremiumPercent
    );

    /// carapacePremiumRateToUse = max(carapacePremiumRate, minCarapaceRiskPremiumPercent)
    int256 _carapacePremiumRateToUse = _carapacePremiumRate >
      _minCarapaceRiskPremiumPercent
      ? _carapacePremiumRate
      : _minCarapaceRiskPremiumPercent;
    console.logInt(_carapacePremiumRateToUse);
.....
```
As you can see when the return value of the `RiskFactorCalculator.canCalculateRiskFactor()` is false code won't set the value of the `_carapacePremiumRate` and it would have 0 value and after the IF cod would set the `_minCarapaceRiskPremiumPercent` as the `_carapacePremiumRate` and the returned premium would be lowest possible.
this is `canCalculateRiskFactor()` code:
```solidity
 function calculateRiskFactor(
    uint256 _currentLeverageRatio,
    uint256 _leverageRatioFloor,
    uint256 _leverageRatioCeiling,
    uint256 _leverageRatioBuffer,
    uint256 _curvature
  ) external view returns (int256 _riskFactor) {
    console.log(
      "Calculating risk factor... leverage ratio: %s, floor: %s, ceiling: %s",
      _currentLeverageRatio,
      _leverageRatioFloor,
      _leverageRatioCeiling
    );

    int256 _numerator = int256(
      (_leverageRatioCeiling + _leverageRatioBuffer) - _currentLeverageRatio
    );

    int256 _denominator = int256(_currentLeverageRatio) -
      int256(_leverageRatioFloor - _leverageRatioBuffer);

    _riskFactor = (int256(_curvature) * _numerator) / _denominator;
    console.logInt(_riskFactor);
  }
```
As you can see  there are two states that causes risk factor to be incalculable:
1. `leverageRatio < Pool.leverageRatioFloor`
2. `leverageRatio > Pool.leverageRatioCeiling`
in both this states code returns the minimum risk factor but when `leverageRatio < Pool.leverageRatioFloor` code should return the maximum risk factor because according to the docs: " The lower the leverage ratio is, the higher the risk factor and the premium are because the market believes that underlying loans are unsafe."

## Impact
wrong premium calculations when  `leverageRatio < Pool.leverageRatioFloor` which can cause other logics that use this function to work incorrectly and some users would lose funds because of the lower calculated premiumes.

## Code Snippet
https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/libraries/RiskFactorCalculator.sol#L33-L56

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/PremiumCalculator.sol#L63-L102

## Tool used
Manual Review

## Recommendation
when  `leverageRatio < Pool.leverageRatioFloor` then set value of the `_carapacePremiumRateToUse` to highest.