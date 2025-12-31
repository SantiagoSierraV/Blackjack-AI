from env import Blackjack_Env
from agents import MonteCarloAgent


def main():
    blackjack_env = Blackjack_Env()
    agent = MonteCarloAgent(epsilon=0.1)

    episodes = 5000000

    for ep in range(1, episodes+1):
        state = blackjack_env.reset()
        episode = []
        done = False

        while not done:
            action = agent.act(state, explore=True)
            next_state, done, reward = blackjack_env.step(action)

            episode.append((state, action))
            state = next_state

        agent.update(episode, reward)

        if ep % (episodes/10) == 0:
            print(f'Episode {ep} completed')

    # Save the Q values
    agent.save('checkpoints/mc_q_5M.pkl')

if __name__ == '__main__':
    main()