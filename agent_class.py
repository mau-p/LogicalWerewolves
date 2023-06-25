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
        beliefs = {index: value for index, value in enumerate(values)}
        beliefs.pop(self.id) # Agents already know themselves
        return beliefs
    
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
        self.known_werewolves = set()

    def vote(self):
        return self.tie_argmax(self.beliefs)
    
    def update_beliefs(self, voter, votee, n_werewolves):
        max_rel_score = max(self.beliefs.values())
        bug_check = False
        # If votee is werewolf
        if isinstance(votee, Werewolf):
            bug_check = True
            # viewer will consider voter a little girl (can be tied)
            self.beliefs[voter] = max_rel_score
        # If voter is werewolf
        if isinstance(voter, Werewolf):
            if bug_check: print(f"Tomfoolery going on")
            # Viewer will consider votee a little girl (can be tied)
            self.beliefs[votee] = max_rel_score


class Villager(Agent):
    def __init__(self, n_agents):
        super().__init__(n_agents)

    def vote(self):
        return self.tie_argmin(self.beliefs)
    
    def update_beliefs(self, voter, votee, n_werewolves):
        max_rel_score = max(self.beliefs.values())
        min_rel_score = min(self.beliefs.values())
        # if viewer considers votee little girl, voter will be considered a werewolf
        if self.beliefs[votee] == max_rel_score:
            self.beliefs[voter] = min_rel_score - 1
        # if viewer considers voter little girl, votee will be considered werewolf (tied if multiple)
        elif self.beliefs[voter] == max_rel_score:
            self.beliefs[votee] = min_rel_score


class LittleGirl(Villager):
    def __init__(self, n_agents, discovery_prob):
        super().__init__(n_agents)
        self.discovery_prob = discovery_prob
        self.known_werewolves = set()
        self.dont_vote = set()
    
    def look_overnight(self, werewolves):
        for werewolf in werewolves:
            if random.random() < self.discovery_prob:
                # print(f"Little girl spotted werewolf {werewolf.id} killing during the night")
                self.known_werewolves.add(werewolf.id)
                if werewolf.id in self.beliefs:
                    self.beliefs.pop(werewolf.id)

    def tie_known_werewolves(self, potential_votes):
        return random.choice(potential_votes)

    def vote(self):
        potential_votes = self.known_werewolves - self.dont_vote
        if potential_votes:
            return self.tie_known_werewolves(list(potential_votes))
        else:
            return self.tie_argmin(self.beliefs)

    def update_beliefs(self, voter, votee, n_werewolves):
        # little girl has spotted a werewolf
        num_spotted = len(self.known_werewolves)
        # little girl has not spotted all werewolves
        if n_werewolves > num_spotted:
            # There is another werewolf but we cannot gain knowledge about who it is
            if voter in self.known_werewolves and votee in self.known_werewolves:
                return
            # if viewer knows voter is werewolf, votee will be considered possible to be a villager
            elif voter in self.known_werewolves:
                self.beliefs[votee] += 1
            # if viewer knows votee is werewolf, voter will be considered possible to be a villager
            elif votee in self.known_werewolves:
                self.beliefs[voter] += 1
            
            # voter and votee are not spotted werewolves
            # if viewer trusts votee more than voter, voter will be considered possible to be a werewolf
            elif self.beliefs[votee] > self.beliefs[voter]:
                self.beliefs[voter] -= 1
            # if viewer trusts voter more than votee, votee will be considered possible to be a werewolf
            elif self.beliefs[voter] > self.beliefs[votee]:
                self.beliefs[votee] -= 1
