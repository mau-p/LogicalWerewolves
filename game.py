import agent
import numpy as np 

class Game:
    def __init__(self, number_werewolves, number_villagers):
        self.number_werewolves = number_werewolves
        self.number_villagers = number_villagers
        self.girl_vote_prob = 0.5 # Probability that girl has seen wolves kill during night
        self.werewolves = self.create_werewolves()
        self.little_girl = agent.LittleGirl(self.girl_vote_prob)
        self.villagers = self.create_villagers()
        self.all_agents = self.werewolves + self.villagers
        
    def get_rel_scores(self):
        return [a.get_reliability() for a in self.all_agents]    

    def create_werewolves(self):
        werewolves = []
        for _ in range(self.number_werewolves):
            werewolves.append(agent.Werewolf())
        return werewolves

    def create_villagers(self):
        villagers = []
        for _ in range(self.number_villagers):
            villagers.append(agent.Villager())
        villagers.append(self.little_girl)
        return villagers

    def night(self):
        print('The night has fallen')

        rel_scores = self.get_rel_scores()
        kill = self.villagers[np.argmax(rel_scores)]

        self.villagers.remove(kill)
        self.all_agents.remove(kill)

        print(f'The werewolves have killed {kill.id}')

    def shuffle_agents(self):
        np.random.shuffle(self.all_agents)

    def day(self):
        self.shuffle_agents() # Shuffle the agents to prevent bias when all scores are equal
        rel_scores = self.get_rel_scores()
        print(f'All agents:         {[a.id for a in self.all_agents]}')
        print(f'Werewolves:         {[a.id for a in self.werewolves]}')
        print(f'Reliability scores: {rel_scores}')
        print('The day has risen')
        votes = []

        for a in self.all_agents:
            votes.append(a.vote(rel_scores, self.all_agents, self.villagers, self.werewolves))
            print(f'{a.id} voted for {votes[len(votes)-1].id}')

        kill = max(set(votes), key=votes.count)
        for a in self.all_agents:
            a.update_rel(1 if votes[self.all_agents.index(a)] == kill and isinstance(kill, agent.Werewolf) else -1)

        self.all_agents.remove(kill)
        if kill in self.villagers:
            self.villagers.remove(kill)
            if isinstance(kill, agent.LittleGirl):
                print(f'{kill.id} has been voted off, they were the little girl')
            else:
                print(f'{kill.id} has been voted off, they were a villager')
        else:
            self.werewolves.remove(kill)
            print(f'{kill.id} has been voted off, they were a werewolf')
        
    def run_game(self):
        while True:
            self.night()
            if not self.villagers:
                print('Werewolves win')
                break
            self.day()
            if not self.werewolves:
                print('Villagers win')
                break
