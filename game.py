import agent
import random

class Game:
    def __init__(self, number_werewolves, number_villagers):
        self.number_werewolves = number_werewolves
        self.number_villagers = number_villagers
        self.werewolves = self.create_werewolves()
        self.little_girl = agent.LittleGirl()
        self.villagers = self.create_villagers()
        self.all_agents = self.werewolves + self.villagers
        self.girl_vote_prob = 0.7
        
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
        for werewolf in self.werewolves:
            if not self.villagers:
                break
            kill = random.choice(self.villagers)
            self.villagers.remove(kill)
            self.all_agents.remove(kill)
            print(f'Werewolf {werewolf.id} has killed {kill.id}')

    def day(self):
        print('The day has risen')
        votes = []

        for a in self.all_agents:
            vote = None
            if isinstance(a, agent.LittleGirl):
                if random.rand() > self.girl_vote_prob:
                    vote = random.choice(self.werewolves)
                else:
                    vote = random.choice(self.all_agents)
            elif isinstance(a, agent.Werewolf):
                vote = random.choice(self.villagers)
            else:
                vote = random.choice(self.all_agents)

            votes.append(vote)
            
        kill = max(set(votes), key=votes.count)
        for a in self.all_agents:
            #TODO: even deze logic checken, ik weet niet zeker of dit klopt
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
