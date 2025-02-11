import random
from getch1 import *
import sys

class Goblin:
    # The Goblin class defines the different Goblin types and their corresponding abilities
    def __init__(self):
        self.coordX = None
        self.coordY = None
        self.encountered = False # If the Goblin has been encountered, it's removed from the game

    def spawn_goblin(self, environment):
        # Spawn Goblin at a random point in the maze
        self.possible_spawns = []
        for x in range(17):
            for y in range(17):
                if environment[x][y] == 0:
                    self.possible_spawns.append((x, y))
        self.random_spawn = random.choice(self.possible_spawns)
        self.coordX = self.random_spawn[0]
        self.coordY = self.random_spawn[1]

class Wealth_Goblin(Goblin):
    # The Wealth Goblin can give coins to the Hero based on the game difficulty
    def __init__(self):
        super().__init__()
        self.name = "Wealth"
        self.coins_awarded = 10
        self.success_rate = 20
        self.ability = (self.coins_awarded, self.success_rate)

    def spawn_goblin(self, environment):
        super().spawn_goblin(environment)

    def reward(self, difficulty=1):
        # Calculating how much coins to award.
        coins_awarded = 10 * difficulty
        success_rate = 0.2 / difficulty
        return round(coins_awarded), round(success_rate)

class Health_Goblin(Goblin):
    # The Health Goblin can heal the Hero based on the game difficulty
    def __init__(self):
        super().__init__()
        self.name = "Health"
        self.health_recovered = 10
        self.success_rate = 20
        self.ability = (self.health_recovered, self.success_rate)
    
    def spawn_goblin(self, environment):
        super().spawn_goblin(environment)

    def heal(self, difficulty=1):
        # Calculating how much to heal.
        health_recovered = 10 * difficulty
        success_rate = 0.2 / difficulty
        return round(health_recovered), round(success_rate)

class Gamer_Goblin(Goblin):
    # The Gamer Goblin gives coins to the Hero, as well as heal them, based on the game difficulty
    def __init__(self):
        super().__init__()
        self.name = "Gamer"
        self.coins_awarded = 20
        self.health_recovered = 20
        self.ability = (self.coins_awarded, self.health_recovered)

    def spawn_goblin(self, environment):
        super().spawn_goblin(environment)

    def rps(self, difficulty=1):
        # The Hero gets the rewards only if they win a game of Rock, Paper, Scissors
        coins_awarded = 20 / difficulty
        health_recovered = 20 / difficulty    
        return round(coins_awarded), round(health_recovered)
    
if os.path.basename(sys.argv[0]) != "playgame.py":
    script_path = os.path.join(os.path.dirname(__file__), "playgame.py")
    print(f"Wrong file executed! Running '{script_path}' instead...")
    os.system(f'python "{script_path}"')
    sys.exit()