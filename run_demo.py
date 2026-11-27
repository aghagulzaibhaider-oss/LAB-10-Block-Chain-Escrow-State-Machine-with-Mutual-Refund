"""Lab 10 demo: reproduces the expected transcript from the lab sheet."""
from escrow import Escrow

# --- Scenario 1: normal order -------------------------------------------
e = Escrow()
for title, fn in [('Early release', lambda: e.release('Alice', True)),
                  ('Seller tries to fund', lambda: e.deposit('Bob', 150))]:
    try:
        fn()
    except ValueError as err:
        print('REJECTED', title, ':', err)

e.deposit('Alice', 150)
print('AFTER DEPOSIT:', e)

try:
    e.release('Alice', False)
except ValueError as err:
    print('REJECTED without delivery:', err)

paid = e.release('Alice', True)
print('AFTER RELEASE:', e, 'paid=', paid)

try:
    e.release('Alice', True)
except ValueError as err:
    print('REJECTED replay:', err)
assert paid == 150 and e.state == 'RELEASED'

# --- Scenario 2: mutual refund (required extension) ---------------------
refund_case = Escrow()
refund_case.deposit('Alice', 150)
try:
    refund_case.refund('Alice', 'Eve')
except ValueError as err:
    print('REJECTED unilateral refund:', err)

refund_amount = refund_case.refund('Alice', 'Bob')
print('AFTER MUTUALLY AGREED REFUND:', refund_case, 'refunded=', refund_amount)
assert refund_amount == 150 and refund_case.state == 'REFUNDED' and refund_case.escrowed == 0

try:
    refund_case.refund('Alice', 'Bob')
except ValueError as err:
    print('REJECTED repeat refund:', err)

print('PASS: state transitions and authorization checks enforced.')
print('NOTE: no real blockchain, funds, oracle, EVM or Solidity is involved.')
