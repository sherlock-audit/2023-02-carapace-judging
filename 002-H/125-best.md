0x52

high

# Unbounded loop in ProtectionPool#lockCapital can be maliciously dos'd

## Summary

ProtectionPool#lockCapital loops through the entire activeProtectionIndexes when calculating the amount of underlying to lock. A malicious user could make a large number of protections to inflate this array and cause an out-of-gas error. The lockCapital call is essential to locking the pool in case a default occurs, making it impossible.

## Vulnerability Detail

See summary

## Impact

The protection pool won't be able to locked in the event of a defaulted

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L357-L424

## Tool used

Manual Review

## Recommendation

Rework accounting for protections