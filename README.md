# Lab 10: Escrow State Machine with Mutual Refund

**Course:** Introduction to Blockchain
**Name / Roll No:** ______________________

## Purpose

This lab shows how a smart contract works as a set of rules that move a contract between fixed **states**. A transition happens only when the right person acts and the right conditions hold. It is a local Python simulation of an escrow between a buyer (Alice) and a seller (Bob). It does **not** use a real blockchain, Solidity, the EVM, or real money.

The required extension is a **mutual refund** path: `FUNDED -> REFUNDED`, allowed only when both the buyer and the seller consent.

## State Machine

```
CREATED --deposit--> FUNDED --release--> RELEASED
   |                    |
 cancel              refund (buyer + seller)   <- new extension
   v                    v
CANCELLED            REFUNDED
```

| Method | Transition | Rules |
|---|---|---|
| `deposit(actor, amount)` | CREATED -> FUNDED | Actor must be the buyer; amount must equal the price (150) |
| `release(actor, delivered)` | FUNDED -> RELEASED | Buyer approves and `delivered=True` |
| `refund(buyer_actor, seller_actor)` | FUNDED -> REFUNDED | Both named parties must be correct; returns 150 and sets `escrowed=0` |
| `cancel(actor)` | CREATED -> CANCELLED | Only the buyer, and only before funding |

Every method checks the current state first, then who is calling, then the conditions. If any check fails it raises `ValueError` and nothing changes. Because each successful transition changes the state, replays and duplicate refunds are rejected.

## Files

| File | Description |
|---|---|
| `escrow.py` | The `Escrow` class (contract logic) |
| `run_demo.py` | Reproduces the lab's expected output |
| `test_escrow.py` | 9 unit tests covering every transition |
| `Lab10_Escrow_Colab.ipynb` | Colab notebook that creates and runs all of the above |
| `VIVA_ANSWERS.md` | Model answers to the three viva questions |

## How to Run

### On Google Colab
Upload `Lab10_Escrow_Colab.ipynb` and choose **Runtime > Run all**.

### On Linux / locally
```bash
python3 run_demo.py
python3 -m unittest -v test_escrow
python3 -m py_compile escrow.py
```

## Expected Results

| Test | Expected | Result |
|---|---|---|
| Early release | Rejected | Rejected |
| Seller deposits | Rejected | Rejected |
| Release without delivery | Rejected | Rejected |
| Release with delivery | RELEASED, paid 150 | Pass |
| Replay release | Rejected | Rejected |
| Refund with wrong seller (Eve) | Rejected | Rejected |
| Mutual refund | REFUNDED, 150 returned | Pass |
| Repeat refund | Rejected | Rejected |

The unit tests should print `Ran 9 tests ... OK`.

## Limitations

- Consent is simulated with string arguments such as `'Alice'` and `'Bob'`. These are not digital signatures, so this is not secure authorization.
- `delivered` is trusted input. A real contract needs an oracle or dispute mechanism to learn about physical delivery.
- After release, `escrowed` still shows 150 (the lab's expected output). A stricter version would clear it to 0.
