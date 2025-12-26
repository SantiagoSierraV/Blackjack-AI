import random
from core.cards import Card

class Deck:
    def __init__(self, num_decks: int = 1):
        self.num_decks = num_decks
        self.cards = []
        self._build()
        self.shuffle()

    def _build(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['♠', '♥', '♦', '♣']

        # List comprehension
        self.cards = [
            Card(rank, suit)
            for _ in range(self.num_decks)
            for rank in ranks
            for suit in suits
        ]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self) -> Card:
        if not self.cards:
            raise RuntimeError('Deck is empty')
        
        # Removes the card and also returns it
        return self.cards.pop()
    
    # So we can call len(deck)
    def __len__(self):
        return len(self.cards)