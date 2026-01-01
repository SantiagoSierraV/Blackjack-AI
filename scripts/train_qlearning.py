from env import Blackjack_Env
from agents import QLearningAgent


def main():
    blackjack_env = Blackjack_Env()
    agent = QLearningAgent(gamma=1.0, epsilon=0.2)

    episodes = 5000000

    for ep in range(1, episodes+1):
        state = blackjack_env.reset()
        done = False

        while not done:
            action = agent.act(state, explore=True)
            next_state, done, reward = blackjack_env.step(action)

            agent.update(state, action, reward, next_state, done)

            state = next_state

        # Decay epsilon
        agent.epsilon = max(0.05, agent.epsilon * 0.999999)

        if ep % (episodes/10) == 0:
            print(f'Episode {ep} completed')

    # Save the Q values
    agent.save('checkpoints/q_learning_5M.pkl')

if __name__ == '__main__':
    main()