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
        # Explore
        if random.random() < self.epsilon and explore:
            return random.choice([Action.HIT, Action.STAND])
        
        # Exploit
        q_hit = self.Q[(state, Action.HIT)]
        q_stand = self.Q[(state, Action.STAND)]

        # Look at the learned values (if not seen they are equal to 0), then choose the better action
        # If they are the same, choose a random action
        if q_hit == q_stand:
            return random.choice([Action.HIT, Action.STAND])
        return Action.HIT if q_hit > q_stand else Action.STAND
    
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