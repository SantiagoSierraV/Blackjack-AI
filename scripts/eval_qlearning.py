from env import Blackjack_Env
from agents import QLearningAgent

def main():
    blackjack_env = Blackjack_Env()
    agent = QLearningAgent()
    agent.load('checkpoints/q_learning_5M.pkl')

    episodes = 1000000
    total_reward = 0

    for episode in range(1, episodes+1):
        state = blackjack_env.reset()
        done = False

        while not done:
            action = agent.act(state, explore=False)
            state, done, reward = blackjack_env.step(action)

        total_reward += reward

        if episode % (episodes/10) == 0:
            print(f'Episode {episode} completed')

    print(f'Average reward over {episodes} episodes: {total_reward/episodes}')

if __name__ == '__main__':
    main()