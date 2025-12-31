from core.deck import Deck
from core.hand import Hand
from env.actions import Action

class Blackjack_Env:
    def __init__(self, num_decks: int = 1, dealer_hits_soft_17: bool = True, blackjack_payout: int = 1.5):
        self.num_decks = num_decks
        self.dealer_hits_soft_17 = dealer_hits_soft_17
        self.blackjack_payout = blackjack_payout
        self.deck = Deck(num_decks)
        self.deck.shuffle()
        self.done: bool = False

    def reset(self) -> dict:
        if self.deck is None or len(self.deck) < 15:
            self.deck = Deck(self.num_decks)

        self.player_hand = Hand()
        self.dealer_hand = Hand()

        self.player_hand.add_card(self.deck.draw())
        self.player_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())
        self.dealer_hand.add_card(self.deck.draw())

        if self.player_hand.best_value == 21 or self.dealer_hand.best_value == 21:
            self.done = True
        else:
            self.done = False

        return self._get_state()

    def step(self, action: Action) -> tuple[dict, bool, float]:
        if self.done:
            return self._get_state(), self.done, self._resolve_round()
        
        if action == Action.HIT:
            self.player_hand.add_card(self.deck.draw())

            if self.player_hand.is_bust:
                self.done = True
                return self._get_state(), self.done, -1.0
            else:
                return self._get_state(), self.done, 0.0
            
        if action == Action.STAND:
            self.done = True
            self._play_dealer()
            return self._get_state(), self.done, self._resolve_round()


    def _play_dealer(self) -> None:
        while self.dealer_hand.best_value < 17:
            self.dealer_hand.add_card(self.deck.draw())

            # Hit if soft 17 and dealer_hits_soft_17 is true
            if self.dealer_hand.best_value == 17 and self.dealer_hand.is_soft and self.dealer_hits_soft_17:
                self.dealer_hand.add_card(self.deck.draw())
        
    def _resolve_round(self) -> float:
        # Blackjack checks
        player_bj = self.player_hand.best_value == 21 and len(self.player_hand.cards) == 2
        dealer_bj = self.dealer_hand.best_value == 21 and len(self.dealer_hand.cards) == 2

        if player_bj and dealer_bj:
            return 0.0
        if player_bj:
            return self.blackjack_payout
        if dealer_bj:
            return -1.0

        # Bust checks
        if self.player_hand.is_bust:
            return -1.0
        if self.dealer_hand.is_bust:
            return 1.0
        
        # Value comparison
        if self.player_hand.best_value > self.dealer_hand.best_value:
            return 1.0
        if self.player_hand.best_value < self.dealer_hand.best_value:
            return -1.0
        
        return 0.0

    def _get_state(self) -> dict:
        return (
            self.player_hand.best_value,    # Player's best value
            self.player_hand.is_soft,       # Is the player soft
            self.dealer_hand.top_card_value # Dealer's top card value
        )