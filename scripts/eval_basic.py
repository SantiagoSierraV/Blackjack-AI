from env import Blackjack_Env
from strategies import BasicStrategyAgent

def print_hands(env):
    print(f"Dealer: {env.dealer_hand.cards[0]}")    
    print(f"Player: {env.player_hand.cards} (value={env.player_hand.best_value})")

def main():
    blackjack_env = Blackjack_Env()
    basic_strategy_agent = BasicStrategyAgent()

    episodes = 1000000
    total_reward = 0

    for episode in range(1, episodes+1):
        state = blackjack_env.reset()
        done = False

        while not done:
            action = basic_strategy_agent.act(state)
            state, done, reward = blackjack_env.step(action)

        total_reward += reward

        if episode % (episodes/10) == 0:
            print(f'Episode {episode} completed')

    print(f'Average reward over {episodes} episodes: {total_reward/episodes}')

if __name__ == '__main__':
    main()