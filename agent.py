import random


class Agent:
    def __init__(self):
        self.beliefs = None
        self.known_villagers = []
        self.known_werewolves = []
        self.known_little_girl = []

    def share_knowledge(self):
        pass


class Werewolf(Agent):
    def __init__(self):
        super().__init__()

    def vote(self):
        pass

    def share_knowledge(self):
        pass


class Villager(Agent):
    def __init__(self):
        super().__init__()

    def vote(self):
        pass


class LittleGirl(Agent):
    def __init__(self):
        super().__init__()

    def vote(self):
        pass
