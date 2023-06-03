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
                print('Werewolves win')
                break
            kill = random.choice(self.villagers)
            self.villagers.remove(kill)
            self.all_agents.remove(kill)
            print(f'Werewolf {werewolf.id} has killed {kill.id}')

    def day(self):
        print('The day has risen')
        votes = []

        for villager in self.villagers:
            if isinstance(villager, agent.LittleGirl):
                votes.append(random.choice(self.werewolves))
            else:
                votes.append(random.choice(self.all_agents))

        for werewolf in self.werewolves:
            votes.append(random.choice(self.villagers))

        kill = max(set(votes), key=votes.count)
        self.all_agents.remove(kill)
        if kill in self.villagers:
            self.villagers.remove(kill)
            print(f'{kill.id} has been voted off, they were a villager')
        else:
            self.werewolves.remove(kill)
            print(f'{kill.id} has been voted off, they were a werewolf')
        
    def run_game(self):
        while True:
            self.night()
            self.day()
            if not self.werewolves:
                print('Villagers win')
                break
            elif not self.villagers:
                print('Werewolves win')
                break
