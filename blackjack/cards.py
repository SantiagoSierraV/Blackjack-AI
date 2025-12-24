from dataclasses import dataclass
# A dataclass is used since the cards won't change, and also for easier syntax

# Frozen so it doesn't change
@dataclass(frozen=True)
class Card:
    # The rank and the suit are strings
    rank: str   # '2'–'10', 'J', 'Q', 'K', 'A'
    suit: str   # '♠', '♥', '♦', '♣'

    # We use property for cleaner syntax: without ()
    @property
    def value(self) -> int:
        # Blackjack value (Ace valued at 11 by default)
        if self.rank in ['J','Q','K']:
            return 10
        if self.rank == 'A':
            return 11
        return int(self.rank)