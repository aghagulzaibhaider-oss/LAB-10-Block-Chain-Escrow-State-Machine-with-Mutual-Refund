"""Unit tests for every transition (including cancel, which the demo skips)."""
import unittest
from escrow import Escrow


class TestEscrow(unittest.TestCase):
    def setUp(self):
        self.e = Escrow()

    def test_deposit_ok(self):
        self.e.deposit('Alice', 150)
        self.assertEqual((self.e.state, self.e.escrowed), ('FUNDED', 150))

    def test_deposit_wrong_actor_or_amount(self):
        with self.assertRaises(ValueError): self.e.deposit('Bob', 150)
        with self.assertRaises(ValueError): self.e.deposit('Alice', 100)

    def test_early_release_rejected(self):
        with self.assertRaises(ValueError): self.e.release('Alice', True)

    def test_release_needs_delivery_and_buyer(self):
        self.e.deposit('Alice', 150)
        with self.assertRaises(ValueError): self.e.release('Alice', False)
        with self.assertRaises(ValueError): self.e.release('Bob', True)
        self.assertEqual(self.e.release('Alice', True), 150)
        self.assertEqual(self.e.state, 'RELEASED')

    def test_release_replay_rejected(self):
        self.e.deposit('Alice', 150); self.e.release('Alice', True)
        with self.assertRaises(ValueError): self.e.release('Alice', True)

    def test_refund_needs_both_parties(self):
        self.e.deposit('Alice', 150)
        with self.assertRaises(ValueError): self.e.refund('Alice', 'Eve')
        with self.assertRaises(ValueError): self.e.refund('Eve', 'Bob')
        self.assertEqual(self.e.refund('Alice', 'Bob'), 150)
        self.assertEqual((self.e.state, self.e.escrowed), ('REFUNDED', 0))

    def test_refund_before_funding_and_twice_rejected(self):
        with self.assertRaises(ValueError): self.e.refund('Alice', 'Bob')
        self.e.deposit('Alice', 150); self.e.refund('Alice', 'Bob')
        with self.assertRaises(ValueError): self.e.refund('Alice', 'Bob')

    def test_cancel(self):
        with self.assertRaises(ValueError): self.e.cancel('Bob')
        self.e.cancel('Alice')
        self.assertEqual(self.e.state, 'CANCELLED')
        with self.assertRaises(ValueError): self.e.deposit('Alice', 150)

    def test_cancel_after_funding_rejected(self):
        self.e.deposit('Alice', 150)
        with self.assertRaises(ValueError): self.e.cancel('Alice')


if __name__ == '__main__':
    unittest.main(verbosity=2)
