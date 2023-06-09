import agent_class
import random
import ascii_art

class Game:
    def __init__(self, number_werewolves, number_villagers, higher_order=False, dynamic_behavior=False):
        if dynamic_behavior and not higher_order:
            raise ValueError("Dynamic behavior can only be true if higher order is true")
        
        self.number_werewolves = number_werewolves
        self.number_villagers = number_villagers
        self.n_agents = self.number_werewolves + self.number_villagers +1
        self.werewolves = self.create_werewolves()
        self.little_girl = agent_class.LittleGirl(self.n_agents, 0.2)
        self.villagers = self.create_villagers()
        self.all_agents = self.werewolves + self.villagers
        self.votes = {}
        self.first = True
        self.round = 0
        self.higher_order = higher_order
        self.dynamic_behavior = dynamic_behavior
        self.correct_updates = 0
        self.incorrect_updates = 0

    def create_werewolves(self):
        werewolves = []
        for _ in range(self.number_werewolves):
            werewolves.append(agent_class.Werewolf(self.n_agents))
        
        for werewolf in werewolves:
            for other_werewolf in werewolves:
                if werewolf == other_werewolf:
                    continue
                werewolf.known_werewolves.add(other_werewolf.id)
                # Werewolves already know each other
                werewolf.beliefs.pop(other_werewolf.id)
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
    
    def update_common_knowledge(self, kill, score_update):
        """
        Works as follows: all the people who voted for a villager get their scores downgraded 
        by other agents by variable score_update. However all the agents who voted for agents
        who voted for a villager get their score upgraded by score_update/2, and so forth. 
        So opposite is true for werewolves. 
        """
        reward = score_update
        votes = self.votes
        target = [kill]

        for voter_id, voted in votes.items():
            if voted in target:
                voter = self.get_agent(voter_id)
                if voter is None:
                    continue

                voter_is_werewolf = isinstance(voter, agent_class.Werewolf)
                voter_is_villager = isinstance(voter, agent_class.Villager)

                if ((reward < 0) and voter_is_villager) or ((reward > 0) and voter_is_werewolf):
                    # Correct choice for agent role
                    choice = 'VILLAGER' if voter_is_werewolf else 'WEREWOLF'
                    correct = True
                
                else:
                    # Incorrect choice for agent role
                    choice = 'VILLAGER' if voter_is_villager else 'WEREWOLF'
                    correct = False

                for agent in self.all_agents:
                    if agent == voter:
                        agent.memory[choice] += 1
                        continue

                    if correct:
                        self.correct_updates += 1
                    else:
                        self.incorrect_updates += 1
                    
                    if isinstance(agent, agent_class.Werewolf) and voter_is_villager:
                        # print(f'agent {agent.id} updates beliefs about {voter} by {-reward}. This is {correct}')
                        agent.beliefs[voter_id] -= reward
                    elif isinstance(agent, agent_class.Villager) and not isinstance(agent, agent_class.LittleGirl):
                        # print(f'agent {agent.id} updates beliefs about {voter} by {-reward}. This is {correct}')
                        agent.beliefs[voter_id] -= reward
                    elif isinstance(agent, agent_class.LittleGirl) and not voter_id in agent.known_werewolves:
                        # print(f'agent {agent.id} updates beliefs about {voter} by {-reward}. This is {correct}')
                        agent.beliefs[voter_id] -= reward

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

        self.update_common_knowledge(kill, score_update=4)

        # If little girl is alive
        if self.little_girl in self.villagers:
            # Little girls spots wolves
            self.little_girl.look_overnight(self.werewolves)


        for a in self.all_agents:
            a.beliefs.pop(kill)
        print(f'The werewolves have killed {kill}')


    def day(self):
        print('\n~~~~~~~~~~The day has risen~~~~~~~~~~')

        for agent in self.all_agents:
           print(f'Agent {agent.id} beliefs: {agent.beliefs}')
        # Proceed to vote

        vote_cycle = self.all_agents
        random.shuffle(vote_cycle)
        self.votes = {}
        votes_count = {}
        epsilon = 0.1
        
        for agent in self.all_agents:
            votes_count[agent.id] = 0

        for voter in vote_cycle:
            votee = voter.vote()
            self.votes[voter.id] = votee
            votes_count[votee] += 1

            if self.higher_order:
                # Agents can have knowledge of other agents' beliefs
                if self.round > 0:
                    epsilon *= self.round
                    if epsilon > 1:
                        epsilon = 1
                for viewer in vote_cycle:
                    if viewer == voter:
                        continue
                    viewer_has_voted = viewer.id in self.votes
                    
                    if viewer.id == votee and self.dynamic_behavior:
                        max_votes = max(votes_count.values())
                        # Get the agents that currently have the most votes, get the agents with second most votes as well if round>0 and max_votes>1
                        if self.round == 0 or max_votes == 1:
                            cur_kicks = [k for k,v in votes_count.items() if v == max(votes_count.values())]
                        else:
                            cur_kicks = [k for k,v in votes_count.items() if v >= max(votes_count.values())-1]

                        if (isinstance(viewer, agent_class.LittleGirl) and viewer.memory['WEREWOLF'] > viewer.memory['VILLAGER'])\
                            or (isinstance(viewer, agent_class.Werewolf) and viewer.memory['VILLAGER'] > viewer.memory['WEREWOLF'])\
                            and not viewer_has_voted:
                            # If agent is little girl and knows the voter knows this or if agent is werewolf and knows the voter knows this
                            # adjust the reliability scores to not stand out
                            viewer.dynamic(current_top_vote=cur_kicks)

                        elif (isinstance(viewer, agent_class.Villager) or viewer_has_voted) and random.random() < epsilon:
                            # Villagers always try to retaliate with epsilon greedy, as well as all agents that have already voted
                            viewer.retaliate(voter.id)
                    
                    elif viewer.id == votee and not self.dynamic_behavior:
                        # If agent is the votee, try to retaliate with epsilon greedy
                        if random.random() < epsilon:
                            viewer.retaliate(voter.id)

                    else:
                        viewer.update_beliefs(voter.id, votee, self.number_werewolves)
        
        # Determine person with most votes. If tie, choose randomly
        max_votes = max(votes_count.values())
        elected = [villager for villager, vote_count in votes_count.items() if vote_count == max_votes]

        if len(elected) == 1:
            kill = elected[0]
        else:
            kill = random.choice(elected)

        kill_agent = self.get_agent(kill)
        self.all_agents.remove(kill_agent)

        # Determine if positive or negative reward based on instance
        if isinstance(kill_agent, agent_class.LittleGirl):
            print(f'{kill} has been voted off, they were a little girl \n')
            self.villagers.remove(kill_agent)
            score_update = 4
        elif isinstance(kill_agent, agent_class.Villager):
            print(f'{kill} has been voted off, they were a villager \n')
            score_update = 4
            self.villagers.remove(kill_agent)
        elif isinstance(kill_agent, agent_class.Werewolf):
            print(f'{kill} has been voted off, they were a werewolf \n')
            self.werewolves.remove(kill_agent)
            score_update = -4

        # Update knowledge that x has been killed
        self.update_common_knowledge(kill, score_update)
        
        for a in self.all_agents:
            if isinstance(a, agent_class.LittleGirl):
                if kill in a.known_werewolves:
                    a.known_werewolves.remove(kill)
            if kill in a.beliefs:
                a.beliefs.pop(kill)

    def run_game(self):
        round = 1
        while True:
            print(f'\n################### Day {round} ###################\n')
            self.night()
            if len(self.villagers) <= len(self.werewolves):
                print('Werewolves win')
                ascii_art.get_werewolf()
                agent_class.Agent.reset_iteration()
                return 0, self.correct_updates/(self.correct_updates + self.incorrect_updates), round
            self.day()
            if len(self.villagers) <= len(self.werewolves):
                print('Werewolves win')
                ascii_art.get_werewolf()
                agent_class.Agent.reset_iteration()
                return 0, self.correct_updates/(self.correct_updates + self.incorrect_updates), round
            if not self.werewolves:
                print('Villagers win, the village is safe')
                ascii_art.get_village()
                agent_class.Agent.reset_iteration()
                return 1, self.correct_updates/(self.correct_updates + self.incorrect_updates), round

            round += 1
            