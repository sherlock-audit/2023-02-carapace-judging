0x52

medium

# Adversary can DOS seller premium payments by creating a large number of tiny protections

## Summary

ProtectionPool#_accruePremiumAndExpireProtections loops through every active protection. An adversary could create a large number of small protections that would cause an OOG error blocking accrual of premium.

## Vulnerability Detail

See summary

## Impact

## Code Snippet

https://github.com/sherlock-audit/2023-02-carapace/blob/main/contracts/core/pool/ProtectionPool.sol#L963-L1021

## Tool used

ChatGPT

## Recommendation

Modify accruePremiumAndExpireProtection to work in a modular manner that would allow a subset of protections to be cycled