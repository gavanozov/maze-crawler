#  Author: CS1527 Course Team
#  Date: 9 January 2020
#  Version: 1.0

import random
from getch1 import *

class Monster:
    """define your monster class here"""
    def __init__(self):
        self.coordX = None
        self.coordY = None
        self.encountered = False

    def spawn_monster(self, environment):
        # Spawn monster at a random point in the maze
        self.possible_spawns = []
        for x in range(17):
            for y in range(17):
                if environment[x][y] == 0:
                    self.possible_spawns.append((x, y))
        self.random_spawn = random.choice(self.possible_spawns)

        self.coordX = self.random_spawn[0]
        self.coordY = self.random_spawn[1]
        #return Monster(random.randint(1, 3))

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
        monster_type = self.monster_type_check(monster)
        environment.set_coord(monster.coordX, monster.coordY, monster_type)

class Thief_Monster(Monster):
    
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
        
        stolen_amount = 10 * difficulty
        success_rate = 0.2 * difficulty

        return stolen_amount, success_rate
        



class Fighter_Monster(Monster):
    
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
        
        damage_dealt = 10 * difficulty
        success_rate = 0.2 * difficulty

        return damage_dealt, success_rate


class Gamer_Monster(Monster):
    
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

        stolen_amount = 10 * difficulty
        damage_dealt = 10 * difficulty

        return stolen_amount, damage_dealt




