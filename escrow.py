"""Lab 10 - Escrow state machine (toy smart contract, simulated, no real blockchain)."""
from dataclasses import dataclass


@dataclass
class Escrow:
    buyer: str = 'Alice'
    seller: str = 'Bob'
    price: int = 150
    state: str = 'CREATED'
    escrowed: int = 0

    # CREATED -> FUNDED
    def deposit(self, actor, amount):
        if self.state != 'CREATED' or actor != self.buyer or amount != self.price:
            raise ValueError('Only buyer may deposit exact price before funding')
        self.escrowed = amount
        self.state = 'FUNDED'

    # FUNDED -> RELEASED
    def release(self, actor, delivered):
        if self.state != 'FUNDED' or actor != self.buyer or not delivered:
            raise ValueError('Release needs funded contract, buyer approval and delivery')
        self.state = 'RELEASED'
        return self.escrowed

    # FUNDED -> REFUNDED  (the required extension: needs BOTH parties)
    def refund(self, buyer_actor, seller_actor):
        if self.state != 'FUNDED' or buyer_actor != self.buyer or seller_actor != self.seller:
            raise ValueError('Refund requires FUNDED state and both parties consent')
        amount = self.escrowed
        self.escrowed = 0
        self.state = 'REFUNDED'
        return amount

    # CREATED -> CANCELLED
    def cancel(self, actor):
        if self.state != 'CREATED' or actor != self.buyer:
            raise ValueError('Only buyer can cancel before funding')
        self.state = 'CANCELLED'
