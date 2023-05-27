import agent


class Game:
    def __init__(self, number_werewolves, number_villagers):
        self.number_werewolves = number_werewolves
        self.number_villagers = number_villagers
        self.werewolves = self.create_werewolves()
        self.villagers = self.create_villagers()
        self.little_girl = agent.LittleGirl()

    def create_werewolves(self):
        werewolves = []
        for _ in range(self.number_werewolves):
            werewolves.append(agent.Werewolf())
        return werewolves

    def create_villagers(self):
        villagers = []
        for _ in range(self.number_villagers):
            villagers.append(agent.Villager())
        return villagers

    def night(self):
        print('The night has fallen')

    def day(self):
        print('The day has risen')

    def run_game(self):
        while self.number_werewolves != 0 and self.number_villagers != 0:
            self.night()
            self.day()
