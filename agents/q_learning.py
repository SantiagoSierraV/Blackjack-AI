from env import Action
from collections import defaultdict
import random
import pickle

class QLearningAgent:
    def __init__(self, gamma: float = 1.0, epsilon: float = 0.1):
        self.gamma = gamma
        self.epsilon = epsilon

        # We use defaultdict so it returns 0.0 when the key doesn't exist
        self.Q = defaultdict(float)

        # How many times has the agent seen the state
        self.returns_count = defaultdict(int)

    def act(self, state: tuple, explore: bool = True) -> Action:
        # Get legal action for state
        legal_actions = [Action.HIT, Action.STAND]
        if state[2]:
            legal_actions.append(Action.DOUBLE)

        # Explore
        if random.random() < self.epsilon and explore:
            return random.choice(legal_actions)
        
        # Exploit
        best_q = max(self.Q[(state, a)] for a in legal_actions)   # Best q value
        best_actions = [a for a in legal_actions if self.Q[(state, a)] == best_q] # Add the action if is equal to the best q value

        # This adds unbiased tie-breaking
        return random.choice(best_actions)
    
    def update(self, state, action, reward, next_state, done):
        self.returns_count[(state, action)] += 1
        alpha = 1.0 / self.returns_count[(state, action)]

        current = self.Q[(state, action)]

        if done:
            # If the episode ended the target will be the reward, since there is no future states
            target = reward
        else:
            # Best possible future in the next state
            next_q = max(
                self.Q[(next_state, a)]
                for a in Action
            )
            # Bellman equation, gamma is 1.0, because episodes are finite and rewards are only at terminal
            target = reward + self.gamma * next_q

        # Moving averge
        self.Q[(state, action)] += alpha * (target - current)

    # Save the Q values
    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(dict(self.Q), f)

    # Load the Q values
    def load(self, path: str):
        with open(path, "rb") as f:
            loaded_Q = pickle.load(f)
        
        self.Q = defaultdict(float, loaded_Q)