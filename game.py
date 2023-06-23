import agent
import numpy as np
import itertools
import random

class Game:
    def __init__(self, order_knowledge, number_werewolves, number_villagers):
        self.number_werewolves = number_werewolves
        self.number_villagers = number_villagers
        self.n_agents = self.number_werewolves + self.number_villagers +1
        self.girl_vote_prob = 0.3 # Probability that girl has seen wolves kill during night
        self.werewolves = self.create_werewolves()
        self.little_girl = agent.LittleGirl(self.n_agents, self.girl_vote_prob)
        self.villagers = self.create_villagers()
        
        self.all_agents = self.werewolves + self.villagers
        self.start_vote_agent = itertools.count()
        self.first = Truee = [i for i in range(0, self.n_agents)]
        self.round = 0

    def create_werewolves(self):
        werewolves = []
        for _ in range(self.number_werewolves):
            werewolves.append(agent.Werewolf(self.n_agents))
        return werewolves


    def create_villagers(self):
        villagers = []
        for _ in range(self.number_villagers):
            villagers.append(agent.Villager(self.n_agents))
        villagers.append(self.little_girl)
        return villagers
    
    def get_agent(self, id):
        for agent in self.all_agents:
            if agent.id == id:
                return agent
        return None
    
    def get_next_vote_cycle(self):
        current_cycle = self.vote_cycle
        for i in range(len(current_cycle)):
            next_cycle = current_cycle[i:] + current_cycle[:i]

        self.vote_cycle = next_cycle


    def night(self):
        print('The night has fallen')

        votes = {}  # Dictionary to store the vote count for each villager
        for villager in self.villagers:
            votes[villager.id] = 0

        # Each werewolf votes for a villager
        for werewolf in self.werewolves:
            vote = werewolf.vote()
            if vote in votes:
                votes[vote] += 1

        max_votes = max(votes.values())
        elected = [villager for villager, vote_count in votes.items() if vote_count == max_votes]

        if len(elected) == 1:
            kill = elected[0]
        else:
            kill = random.choice(elected)


        kill = self.get_agent(kill)
        self.villagers.remove(kill)
        self.all_agents.remove(kill)
        

        print(f'The werewolves have killed {kill.id}')


    def day(self):
        print(f'All agents:         {[a.id for a in self.all_agents]}')
        print(f'Werewolves:         {[a.id for a in self.werewolves]}')
        print('The day has risen')

        # Update knowledge about killed person

not self.Firstfirst                    if self.round != 0:
            


        # Proceed to vote



        # Update knowledge that x has been killed


        
    def run_game(self):
        while True:
            self.night()
            self.day()
            if len(self.villagers) < len(self.werewolves):
                print('Werewolves win')
                break
            
            self.get_next_vote_cycle()