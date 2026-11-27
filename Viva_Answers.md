# Lab 10 Viva Questions and Model Answers

**Name / Roll No:** ______________________

## Q1. What is different on-chain?

On a real blockchain, contract code is executed and replicated by many nodes under a consensus protocol. Execution costs gas, the resulting state is committed to the chain, and every transaction is authorized by a cryptographic signature. Our Python escrow runs on one machine, with no consensus, no gas, and no signatures, so it only imitates the logic of a contract.

## Q2. Who verifies delivery?

Code cannot observe the physical world, so it cannot know whether goods were delivered. A real application needs an authorized external **oracle** to report delivery, or a **dispute-resolution mechanism** such as an arbitrator. In this lab, the `delivered` argument is simply trusted input to the function.

## Q3. Why are bugs and upgrades difficult?

On-chain code often controls valuable state, and deployed code is immutable or only changeable through governance rules. A bug can therefore be exploited before it is fixed, and patching is costly and risky. This is why contracts need careful testing and auditing before deployment.

## Bonus: Why does the refund need both parties?

If only the buyer could trigger a refund, the buyer could take the money back after the seller shipped the goods. Requiring both parties prevents this one-sided cancellation. In `refund()`, the state check (`FUNDED`) also prevents a second refund, so the same money cannot be paid out twice.
