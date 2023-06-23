import itertools
import random
class Agent:
    id_iter = itertools.count()

    def __init__(self, n_agents):
        self.id = next(Agent.id_iter)
        self.n_agents = n_agents
        self.beliefs = self.create_beliefs()        

    def create_beliefs(self):
        values = [random.choice([-1, 0, 1]) for _ in range(self.n_agents)]
        return {index: value for index, value in enumerate(values)}
    

    def tie_argmin(self, dictionary):
        min_value = min(dictionary.values())  # Find the minimum value
        min_keys = [key for key, value in dictionary.items() if value == min_value]  # Find keys with minimum value
        random_key = random.choice(min_keys)  # Randomly select a key from the keys with minimum value
        return random_key

    def tie_argmax(self, dictionary):
        max_value = max(dictionary.values())  # Find the maximum value
        max_keys = [key for key, value in dictionary.items() if value == max_value]  # Find keys with maximum value
        random_key = random.choice(max_keys)  # Randomly select a key from the keys with maximum value
        return random_key

class Werewolf(Agent):
    def __init__(self, n_agents):
        super().__init__(n_agents)
        self.beliefs[self.id] = -1000000

    def vote(self):
        return self.tie_argmax(self.beliefs)

class Villager(Agent):
    def __init__(self, n_agents):
        super().__init__(n_agents)
        self.beliefs[self.id] = 1000000

    def vote(self):
        return self.tie_argmin(self.beliefs)

class LittleGirl(Agent):
    def __init__(self, n_agents, discovery_prob):
        super().__init__(n_agents)
        self.beliefs[self.id] = 1000000
        self.discovery_prob = discovery_prob

    def vote(self):
        return self.tie_argmin(self.beliefs)
    
    def look_overnight(self, werewolves):
        for werewolf in werewolves:
            if random.random() < self.discovery_prob:
                print(f"Little girl spotted werewolf {werewolf.id} killing during the night")
                self.beliefs[werewolf.id] = -100000
