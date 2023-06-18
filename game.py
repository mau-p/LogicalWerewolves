import agent
import numpy as np
import itertools 

class Game:
    def __init__(self, order_knowledge, number_werewolves, number_villagers):
        self.number_werewolves = number_werewolves
        self.number_villagers = number_villagers
        self.n_agents = self.number_werewolves + self.number_villagers +1
        self.girl_vote_prob = 0.3 # Probability that girl has seen wolves kill during night
        self.werewolves = self.create_werewolves()
        self.villagers = self.create_villagers()
        self.little_girl = [agent.LittleGirl(self.n_agents, self.girl_vote_prob)]
        self.all_agents = self.werewolves + self.villagers + self.little_girl

        self.start_vote_agent = itertools.count()
        self.vote_cycle = [i for i in range(0, self.n_agents)]

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
                return id
        return None
    
    def get_next_vote_cycle(self, current_cycle):
        for i in range(len(current_cycle)):
            next_cycle = current_cycle[i:] + current_cycle[:i]

        self.vote_cycle = next_cycle


    def night(self):
        print('The night has fallen')

        votes = [0] * self.n_agents
        for werewolf in self.werewolves:
            votes[werewolf.vote()] += 1

        kill = self.get_agent(self.tie_argmax(votes))

        self.villagers.remove(kill)
        self.all_agents.remove(kill)

        print(f'The werewolves have killed {kill.id}')


    def day(self, vote_cycle):
        print(f'All agents:         {[a.id for a in self.all_agents]}')
        print(f'Werewolves:         {[a.id for a in self.werewolves]}')
        print('The day has risen')

        # Update knowledge that x has been killed
     


        # Proceed to vote




        # Update knowledge that x has been killed


        for agent in vote_cycle:
            vote = agent.vote()


        
    def run_game(self):
        while True:
            self.night()
            self.day(self.vote_cycle)
            if len(self.villagers) < len(self.werewolves):
                print('Werewolves win')
                break
            
            print('Villagers win')
            self.get_next_vote_cycle(self.vote_cycle)