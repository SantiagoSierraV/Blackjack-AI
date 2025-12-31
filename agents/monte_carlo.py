from env import Action
from collections import defaultdict
import random
import pickle

class MonteCarloAgent:
    def __init__(self, epsilon: float = 0.1):
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
        # If equal, stand
        return Action.HIT if q_hit > q_stand else Action.STAND
    
    def update(self, episode, reward):
        
        visited = set() # Update each (state, action) once per episode

        for state, action in episode:
            if (state, action) in visited:  # If the the pair was already updated in the episode, then skip it
                continue

            visited.add((state, action))

            self.returns_count[(state, action)] += 1    # Add one to the amount of visited times

            # Learning rate, fist update: α = 1.0, second: α = 0.5, third: α = 0.33
            alpha = 1 / self.returns_count[(state, action)]

            # Then Q is set to the average of all observed rewards
            self.Q[(state, action)] += alpha * (reward - self.Q[(state, action)])

    # Save the Q values
    def save(self, path: str):
        with open(path, "wb") as f:
            pickle.dump(dict(self.Q), f)

    # Load the Q values
    def load(self, path: str):
        with open(path, "rb") as f:
            self.Q = pickle.load(f)