from env import Blackjack_Env, Action
import random

def random_action() -> Action:
    return random.choice([Action.HIT, Action.STAND])

def print_hands(env):
    print(f"Dealer: {env.dealer_hand.cards[0]}")    
    print(f"Player: {env.player_hand.cards} (value={env.player_hand.best_value})")

def main():
    blackjack_env = Blackjack_Env()

    episodes = 100000
    total_reward = 0

    for _ in range(episodes):
        _state = blackjack_env.reset()
        done = False

        while not done:
            action = random_action()
            _state, done, reward = blackjack_env.step(action)

        total_reward += reward

    print(f'Average reward over {episodes} episodes: {total_reward/episodes}')

if __name__ == '__main__':
    main()