import itertools
import random
class Agent:
    id_iter = itertools.count(0)

    def __init__(self, n_agents):
        self.id = next(Agent.id_iter)
        self.n_agents = n_agents
        self.beliefs = self.create_beliefs()
        self.memory = {'WEREWOLF': 0, 'VILLAGER': 0}

    def create_beliefs(self):
        values = [random.choice([-1, 0, 1]) for _ in range(self.n_agents)]
        return {index: value for index, value in enumerate(values)}
    
    def tie_argmin(self, dictionary):
        min_value = min(dictionary.values())
        min_keys = [key for key, value in dictionary.items() if value == min_value] 
        random_key = random.choice(min_keys)  
        return random_key

    def tie_argmax(self, dictionary):
        max_value = max(dictionary.values())  
        max_keys = [key for key, value in dictionary.items() if value == max_value]  
        random_key = random.choice(max_keys)  
        return random_key
    
    def reset_iteration():
        Agent.id_iter = itertools.count(0)


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


class LittleGirl(Villager):
    def __init__(self, n_agents, discovery_prob):
        super().__init__(n_agents)
        self.discovery_prob = discovery_prob
    
    def look_overnight(self, werewolves):
        for werewolf in werewolves:
            if random.random() < self.discovery_prob:
                # print(f"Little girl spotted werewolf {werewolf.id} killing during the night")
                self.beliefs[werewolf.id] = -100000
