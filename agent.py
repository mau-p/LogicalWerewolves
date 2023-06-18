import itertools
import random
import numpy as np

class Agent:
    id_iter = itertools.count()

    def __init__(self, n_agents):
        self.id = next(Agent.id_iter)
        self.n_agents = n_agents
        self.beliefs = self.create_beliefs()
        

    def create_beliefs(self):
        values = [random.choice([-1, 0, 1]) for _ in range(self.n_agents)]
        return {index: value for index, value in enumerate(values)}
    

    def tie_argmax(self, arr):
        max_value = np.max(arr)
        max_indices = np.where(arr == max_value)[0]
        random_index = np.random.choice(max_indices)
        return random_index
    

    def tie_argmin(self, arr):
        min_value = np.min(arr)
        min_indices = np.where(arr == min_value)[0]
        random_index = np.random.choice(min_indices)
        return random_index
    

class Werewolf(Agent):
    def __init__(self, n_agents):
        super().__init__(n_agents)

    def vote(self):
        return self.tie_argmax(self.beliefs)


class Villager(Agent):
    def __init__(self, n_agents):
        super().__init__(n_agents)

    def vote(self, rel_scores, all_agents, villagers, werewolves):
        vote = all_agents[np.argmin(rel_scores)]
        if vote is self:
            vote = random.choice(villagers)
        return vote

class LittleGirl(Agent):
    def __init__(self, n_agents, vote_prob=0.5):
        super().__init__(n_agents)
        self.vote_prob = vote_prob

    def vote(self, rel_scores, all_agents, villagers, werewolves):
        if np.random.rand() > self.vote_prob:
            vote = random.choice(werewolves)
        else:
            vote = all_agents[np.argmin(rel_scores)]
        return vote
