import random
from getch1 import *
import sys

class Monster:
    # The Monster class defines the different Monster types and their corresponding abilities
    def __init__(self):
        self.coordX = None
        self.coordY = None
        self.encountered = False

    def spawn_monster(self, environment):
        # Spawn Monster at a random point in the maze
        self.possible_spawns = []
        for x in range(17):
            for y in range(17):
                if environment[x][y] == 0:
                    self.possible_spawns.append((x, y))
        self.random_spawn = random.choice(self.possible_spawns)
        self.coordX = self.random_spawn[0]
        self.coordY = self.random_spawn[1]

    def monster_type_check(self, monster):
        if monster.name == "Thief":
            return 3
        if monster.name == "Fighter":
            return 4
        if monster.name == "Gamer":
            return 5
        else:
            return 3 # fix

    def reset_monster(self, monster, environment):
        # Monsters need to be reset every turn as they don't disappear even after interacting with the Hero
        monster_type = self.monster_type_check(monster)
        environment.set_coord(monster.coordX, monster.coordY, monster_type)

class Thief_Monster(Monster):
    # The Thief Monster can steal coins from the Hero based on the game difficulty
    def __init__(self):
        super().__init__()
        self.name = "Thief"
        self.stolen_amount = 10
        self.success_rate = 20
        self.ability = (self.stolen_amount, self.success_rate)

    def spawn_monster(self, environment):
        super().spawn_monster(environment)

    def monster_type_check(self, monster):
        return super().monster_type_check(monster)
    
    def reset_monster(self, monster, environment):
        return super().reset_monster(monster, environment)

    def steal(self, difficulty=1):
        # Calculating how many coins to steal
        stolen_amount = 10 * difficulty
        success_rate = 0.2 * difficulty
        return round(stolen_amount), round(success_rate)
        
class Fighter_Monster(Monster):
    # The Fighter Monster can deal damage to the Hero based on the game difficulty
    def __init__(self):
        super().__init__()
        self.name = "Fighter"
        self.damage_dealt = 10
        self.success_rate = 20
        self.ability = (self.damage_dealt, self.success_rate)
    
    def spawn_monster(self, environment):
        super().spawn_monster(environment)

    def monster_type_check(self, monster):
        return super().monster_type_check(monster)
    
    def reset_monster(self, monster, environment):
        return super().reset_monster(monster, environment)

    def fight(self, difficulty=1):
        # Calculating how much damage to deal
        damage_dealt = 10 * difficulty
        success_rate = 0.2 * difficulty
        return round(damage_dealt), round(success_rate)

class Gamer_Monster(Monster):
    # The Gamer Monster can steal coins from the Hero, as well as deal damage based on the game difficulty
    def __init__(self):
        super().__init__()
        self.name = "Gamer"
        self.stolen_amount = 10
        self.damage_dealt = 10
        self.ability = (self.stolen_amount, self.damage_dealt)

    def spawn_monster(self, environment):
        super().spawn_monster(environment)

    def monster_type_check(self, monster):
        return super().monster_type_check(monster)
    
    def reset_monster(self, monster, environment):
        return super().reset_monster(monster, environment)

    def rps(self, difficulty=1):
        # The Hero loses health and coins only after losing to a game of Rock Paper Scissors
        stolen_amount = 10 * difficulty
        damage_dealt = 10 * difficulty
        return round(stolen_amount), round(damage_dealt)

if os.path.basename(sys.argv[0]) != "playgame.py":
    script_path = os.path.join(os.path.dirname(__file__), "playgame.py")
    print(f"Wrong file executed! Running '{script_path}' instead...")
    os.system(f'python "{script_path}"')
    sys.exit()
