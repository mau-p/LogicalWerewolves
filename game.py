import agent_class
import numpy as np
import random
import ascii_art

class Game:
    def __init__(self, knowledge_order, number_werewolves, number_villagers):
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
        self.knowledge_order = knowledge_order

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
    

    def update_knowledge(self, kill, score_update):
        reward = score_update
        votes = self.votes
        target = [kill]

        for _ in range(self.knowledge_order):
            next_target = []
            
            # Update beliefs for target
            for voter, voted in votes.items():
                if voted in target:
                    for agent in self.all_agents:
                        if agent == self.get_agent(voter):
                            continue
                        if voter not in next_target:
                            next_target.append(voter)

                        if voter in self.all_agents:
                            agent.beliefs[voter] -= reward
            
            target = next_target
            reward /= -2

    
    def night(self):
        print('\n~~~~~~~~~~The night has fallen~~~~~~~~~~')

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

        self.update_knowledge(kill, score_update=4)


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
        print('\n~~~~~~~~~~The day has risen~~~~~~~~~~')
        print(f'Villagers:         {[a.id for a in self.villagers]}')
        print(f'Werewolves:         {[a.id for a in self.werewolves]}')


        #for agent in self.all_agents:
        #    print(f'Agent {agent.id} beliefs: {agent.beliefs}')
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
            print(f'{kill} has been voted off, they were a little girl')
            self.villagers.remove(kill_agent)
            score_update = 4
        elif isinstance(kill_agent, agent_class.Villager):
            print(f'{kill} has been voted off, they were a villager')
            score_update = 4
            self.villagers.remove(kill_agent)
        elif isinstance(kill_agent, agent_class.Werewolf):
            print(f'{kill} has been voted off, they were a werewolf')
            self.werewolves.remove(kill_agent)
            score_update = -4


        # Update knowledge that x has been killed
        self.update_knowledge(kill, score_update)
        
        for a in self.all_agents:
            a.beliefs.pop(kill)   
        
    def run_game(self):
        round = 1
        while True:
            print(f'\n################### Day {round} ###################\n')
            self.night()
            if len(self.villagers) <= len(self.werewolves):
                print('Werewolves win')
                ascii_art.get_werewolf()
                break
            self.day()
            if len(self.villagers) <= len(self.werewolves):
                print('Werewolves win')
                ascii_art.get_werewolf()
                break
            if not self.werewolves:
                print('Villagers win, the village is safe')
                ascii_art.get_village()
                break

            round += 1