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

    def vote(self):
        pass

    def share_knowledge(self):
        pass


class Villager(Agent):

    def vote(self):
        pass


class LittleGirl(Agent):

    def vote(self):
        pass
