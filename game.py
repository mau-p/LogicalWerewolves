import agent_class
import numpy as np
import random

class Game:
    def __init__(self, order_knowledge, number_werewolves, number_villagers):
        self.number_werewolves = number_werewolves
        self.number_villagers = number_villagers
        self.n_agents = self.number_werewolves + self.number_villagers +1
        self.werewolves = self.create_werewolves()
        self.little_girl = agent_class.LittleGirl(self.n_agents, 0.2)
        print(f"little girl: {self.little_girl.id}")
        self.villagers = self.create_villagers()
        self.all_agents = self.werewolves + self.villagers
        self.votes = {}
        self.first = True
        self.round = 0

    def create_werewolves(self):
        werewolves = []
        for _ in range(self.number_werewolves):
            werewolves.append(agent_class.Werewolf(self.n_agents))
        
        for werewolf in werewolves:
            for other_werewolf in werewolves:
                if werewolf == other_werewolf:
                    continue
                werewolf.beliefs[other_werewolf.id] = -1000000
        return werewolves


    def create_villagers(self):
        villagers = []
        for _ in range(self.number_villagers):
            villagers.append(agent_class.Villager(self.n_agents))
        villagers.append(self.little_girl)
        return villagers
    
    def get_agent(self, id):
        for agent in self.all_agents:
            if agent.id == id:
                return agent
        return None
    
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


        kill_agent = self.get_agent(kill)
        self.villagers.remove(kill_agent)
        self.all_agents.remove(kill_agent)

        if not self.first:
            for voter, voted in self.votes.items():
                if voted == kill:
                    for agent in self.all_agents:
                        if agent == self.get_agent(voter):
                            continue
                        agent.beliefs[voter] -= 1

        # If little girl is alive
        if self.little_girl in self.villagers:

            # Little girls spots wolves
            self.little_girl.look_overnight(self.werewolves)
            
            # Wolves spot little girl
            if random.random() < 0.1:
                print('LITTLE GIRL DISCOVERED')
                for werewolf in self.werewolves:
                    werewolf.beliefs[self.little_girl.id] = 10000


        for a in self.all_agents:
            a.beliefs.pop(kill)
        print(f'The werewolves have killed {kill}')


    def day(self):
        print(f'All agents:         {[a.id for a in self.all_agents]}')
        print(f'Werewolves:         {[a.id for a in self.werewolves]}')
        print('The day has risen')

        for agent in self.all_agents:
            print(f'Agent {agent.id} beliefs: {agent.beliefs}')
        # Proceed to vote

        vote_cycle = self.all_agents
        random.shuffle(vote_cycle)
        self.votes = {}
        votes_count = {}  # Dictionary to store the vote count for each village
        
        for agent in self.all_agents:
            votes_count[agent.id] = 0

        for voter in vote_cycle:
            votee = voter.vote()
            self.votes[voter.id] = votee
            votes_count[votee] += 1

            for viewer in vote_cycle:
                if viewer != voter:
                    trust_votee = viewer.beliefs[votee]
                    trust_voter = viewer.beliefs[voter.id]

                    if trust_votee > trust_voter:
                        viewer.beliefs[voter.id] -= 3
                    
                    if trust_votee < trust_voter:
                        viewer.beliefs[votee] -= 3

        max_votes = max(votes_count.values())
        elected = [villager for villager, vote_count in votes_count.items() if vote_count == max_votes]

        if len(elected) == 1:
            kill = elected[0]
        else:
            kill = random.choice(elected)

        kill_agent = self.get_agent(kill)
        self.all_agents.remove(kill_agent)

        if isinstance(kill_agent, agent_class.LittleGirl):
            print(f'{kill} has been voted of, they were a little girl')
            self.villagers.remove(kill_agent)
            score_update = 3
        elif isinstance(kill_agent, agent_class.Villager):
            print(f'{kill} has been voted of, they were a villager')
            score_update = 3
            self.villagers.remove(kill_agent)
        elif isinstance(kill_agent, agent_class.Werewolf):
            print(f'{kill} has been voted of, they were a werewolf')
            self.werewolves.remove(kill_agent)
            score_update = -3

        # Update knowledge that x has been killed

        for voter, voted in self.votes.items():
            if voted == kill:
                for agent in self.all_agents:
                    if agent == self.get_agent(voter):
                        continue
                    if not voter == kill:
                        agent.beliefs[voter] -= score_update
        
        for a in self.all_agents:
            a.beliefs.pop(kill)   
        
    def run_game(self):
        while True:
            self.night()
            if len(self.villagers) <= len(self.werewolves):
                print('Werewolves win')
                break
            self.day()
            if len(self.villagers) <= len(self.werewolves):
                print('Werewolves win')
                break
            if not self.werewolves:
                print('Villagers win')
                break
            