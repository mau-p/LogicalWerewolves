import itertools
import random
import numpy as np

class Agent:
    id_iter = itertools.count()

    def __init__(self):
        self.beliefs = None
        self.id = next(Agent.id_iter)
        self.reliability = 0

    def update_rel(self, value):
        self.reliability += value

    def get_reliability(self):
        return self.reliability

class Werewolf(Agent):
    def __init__(self):
        super().__init__()

    def vote(self, rel_scores, all_agents, villagers, werewolves):
        return random.choice(villagers)

class Villager(Agent):
    def __init__(self):
        super().__init__()

    def vote(self, rel_scores, all_agents, villagers, werewolves):
        vote = all_agents[np.argmin(rel_scores)]
        if vote is self:
            vote = random.choice(villagers)
        return vote

class LittleGirl(Agent):
    def __init__(self, vote_prob=0.5):
        super().__init__()
        self.vote_prob = vote_prob

    def vote(self, rel_scores, all_agents, villagers, werewolves):
        if np.random.rand() > self.vote_prob:
            vote = random.choice(werewolves)
        else:
            vote = all_agents[np.argmin(rel_scores)]
        return vote
