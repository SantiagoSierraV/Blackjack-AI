import random
from core.cards import Card

class Hand:
    def __init__(self):
        # The cards is a list and its elements Card, also is an empty list 
        self.cards: list[Card] = []

    def add_card(self, card: Card):
        self.cards.append(card)

    @property
    def values(self) -> list[int]:
        # Return all the possible hand values, accounting for Aces

        # The maximum total
        total = sum(card.value for card in self.cards)
        # Ace count
        num_aces = sum(1 for card in self.cards if card.rank == 'A')

        values = [total]
        while num_aces > 0:
            total -= 10 # Ace value goes from 11 to 1
            values.append(total)
            num_aces -= 1

        return values
    
    @property
    def best_value(self) -> int:
        # Best value <= 21, otherwise lowest value

        valid = [v for v in self.values if v <= 21] # Only append valid values

        # If there are valid values is going to return the highest one, otherwise the lowest value possible
        return max(valid) if valid else min(self.values)

    @property
    def is_blackjack(self) -> bool:
        # True if the hand has 2 cards and the best value is 21
        return len(self.cards) == 2 and self.best_value == 21
    
    @property
    def is_bust(self) -> bool:
        # True if the best value is more than 21
        return self.best_value > 21

    @property
    def is_soft(self) -> bool:
        # If there is no ace in hand, only one valid value if possible
        # If there are two or more two valid values it means that at least one ace can be 11, therefore is soft
        valid = [v for v in self.values if v <= 21] # Only append valid values
        return len(valid) > 1
    
    @property
    def top_card_value(self) -> int:
        return self.cards[0].value