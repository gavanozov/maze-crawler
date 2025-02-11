from getch1 import *
import random
import os
import sys

class Hero:
    # The Hero class defines how most of the game works
    def __init__(self, difficulty):
        # The base Hero attributes are initialised here
        self.difficulty = difficulty
        self.coordX = None
        self.coordY = None
        self.health = 100
        self.coins = 100  # Gold coins the hero has
        self.gem = 3 # Score multiplier?
        
    def spawn(self, environment):
        # Spawn the Hero at a random point in the maze
        self.possible_spawns = []
        for x in range(17):
            for y in range(17):
                if environment[x][y] == 0:
                    self.possible_spawns.append((x, y))
        self.random_spawn = random.choice(self.possible_spawns)
        self.coordX = self.random_spawn[0]
        self.coordY = self.random_spawn[1]

    def move(self, environment, monsters, goblins):
        # The most complicated method in the program, which deals with the Hero moving through
        # the maze in different directions and interacting with different characters
        monster_chars = [3, 4, 5]
        goblin_chars = [6, 7, 8]
        ch2 = getch() # We initialize a getch instance which reads single key inputs from the keyboard

        # UP
        if (ch2 == b'H' or ch2 == "A") and (environment.get_coord((self.coordX - 1), self.coordY) == 0):
            # If the UP arrow key is pressed and the cell above the Hero is unoccupied, the Hero moves there
            os.system('cls')
            environment.set_coord(self.coordX, self.coordY, 0) # Set the current cell to unoccupied
            environment.set_coord((self.coordX - 1), self.coordY, 2) # Set the cell above as occupied by the Hero
            self.coordX -= 1 # The Hero's coordinates change
            self.health -= 1 # The Hero loses one health point after each step
            self.reset_monsters(monsters, environment) # Refresh the environment to show monsters
            return True
            
        elif (environment.get_coord((self.coordX - 1), self.coordY) in monster_chars) and (ch2 == b'H' or ch2 == "A"):
            # If the UP arrow key is pressed and the cell above the Hero is occupied by a Monster, the Hero begins interaction
            for monster in monsters:
                # Check which monster from the list has been encountered
                if monster.coordX == (self.coordX - 1) and monster.coordY == self.coordY:
                    encountered_monster = monster
                    encountered_monster.encountered = True
                    break
            print(f"The Hero is about to encounter a {encountered_monster.name} Monster with the ability of {encountered_monster.ability}")
            input("Press Enter to continue.")
            self.monster_encounter(encountered_monster) # The encounter function initiates the different types of interaction
            environment.set_coord(self.coordX, self.coordY, 0)
            environment.set_coord((self.coordX - 1), self.coordY, 2)
            self.coordX -= 1
            return True                          

        elif (environment.get_coord((self.coordX - 1), self.coordY) in goblin_chars) and (ch2 == b'H' or ch2 == "A"):
            # If the UP arrow key is pressed and the cell above the Hero is occupied by a Goblin, the Hero begins interaction
            for goblin in goblins:
                # Check which goblin from the list has been encountered
                if goblin.coordX == (self.coordX - 1) and goblin.coordY == self.coordY:
                    encountered_goblin = goblin
                    encountered_goblin.encountered = True
                    break
            print(f"The Hero is about to encounter a {encountered_goblin.name} Goblin with the ability of {encountered_goblin.ability}")
            input("Press Enter to continue.")
            self.goblin_encounter(encountered_goblin, goblins)
            self.remove_goblin(goblin, goblins) # Goblins are removed from the game after interaction
            environment.set_coord(self.coordX, self.coordY, 0)
            environment.set_coord((self.coordX - 1), self.coordY, 2)
            self.coordX -= 1
            self.reset_monsters(monsters, environment)
            return True      

        # DOWN
        elif (ch2 == b'P' or ch2 == "B") and (environment.get_coord((self.coordX + 1), self.coordY) == 0):
            # If the DOWN arrow key is pressed and the cell under the Hero is unoccupied, the Hero moves there
            os.system('cls')
            print("down key pressed")
            environment.set_coord(self.coordX, self.coordY, 0)
            environment.set_coord((self.coordX + 1), self.coordY, 2)
            self.coordX += 1
            self.health -= 1
            self.reset_monsters(monsters, environment)
            return True
        
        elif (ch2 == b'P' or ch2 == "B") and (environment.get_coord((self.coordX + 1), self.coordY) in monster_chars):
            # If the DOWN arrow key is pressed and the cell under the Hero is occupied by a Monster, the Hero begins interaction
            for monster in monsters:
                if monster.coordX == (self.coordX + 1) and monster.coordY == self.coordY:
                    encountered_monster = monster
                    encountered_monster.encountered = True
                    break
            print(f"The Hero is about to encounter a {encountered_monster.name} Monster with the ability of {encountered_monster.ability}")
            input("Press Enter to continue.")
            self.monster_encounter(encountered_monster)
            environment.set_coord(self.coordX, self.coordY, 0)
            environment.set_coord((self.coordX + 1), self.coordY, 2)
            self.coordX += 1
            return True      

        elif (ch2 == b'P' or ch2 == "B") and (environment.get_coord((self.coordX + 1), self.coordY) in goblin_chars):
            # If the DOWN arrow key is pressed and the cell under the Hero is occupied by a Goblin, the Hero begins interaction
            for goblin in goblins:
                if goblin.coordX == (self.coordX + 1) and goblin.coordY == self.coordY:
                    encountered_goblin = goblin
                    encountered_goblin.encountered = True
                    break
            print(f"The Hero is about to encounter a {encountered_goblin.name} Goblin with the ability of {encountered_goblin.ability}")
            input("Press Enter to continue.")
            self.goblin_encounter(encountered_goblin, goblins)
            self.remove_goblin(goblin, goblins)
            environment.set_coord(self.coordX, self.coordY, 0)
            environment.set_coord((self.coordX + 1), self.coordY, 2)
            self.coordX += 1
            self.reset_monsters(monsters, environment)
            return True      

        # LEFT
        elif (ch2 == b'K' or ch2 == "D") and (environment.get_coord(self.coordX, (self.coordY - 1)) == 0):
            # If the LEFT arrow key is pressed and the cell to the left of the Hero is unoccupied, the Hero moves there
            os.system('cls')
            print("left key pressed")
            environment.set_coord(self.coordX, self.coordY, 0)
            environment.set_coord(self.coordX, (self.coordY - 1), 2)
            self.coordY -= 1
            self.health -= 1
            self.reset_monsters(monsters, environment)
            return True
        
        elif (ch2 == b'K' or ch2 == "D") and (environment.get_coord(self.coordX, (self.coordY - 1)) in monster_chars):
            # If the LEFT arrow key is pressed and the cell to the left of the Hero is occupied by a Monster, the Hero begins interaction
            for monster in monsters:
                if monster.coordX == self.coordX and monster.coordY == (self.coordY - 1):
                    encountered_monster = monster
                    encountered_monster.encountered = True
                    break
            print(f"The Hero is about to encounter a {encountered_monster.name} Monster with the ability of {encountered_monster.ability}")
            input("Press Enter to continue.")
            self.monster_encounter(encountered_monster)
            environment.set_coord(self.coordX, self.coordY, 0)
            environment.set_coord(self.coordX , (self.coordY - 1), 2)
            self.coordY -= 1
            return True      

        elif (ch2 == b'K' or ch2 == "D") and (environment.get_coord(self.coordX, (self.coordY - 1)) in goblin_chars):
            # If the LEFT arrow key is pressed and the cell to the left of the Hero is occupied by a Goblin, the Hero begins interaction
            for goblin in goblins:
                if goblin.coordX == self.coordX and goblin.coordY == (self.coordY - 1):
                    encountered_goblin = goblin
                    encountered_goblin.encountered = True
                    break
            print(f"The Hero is about to encounter a {encountered_goblin.name} Goblin with the ability of {encountered_goblin.ability}")
            input("Press Enter to continue.")
            self.goblin_encounter(encountered_goblin, goblins)
            self.remove_goblin(goblin, goblins)
            environment.set_coord(self.coordX, self.coordY, 0)
            environment.set_coord(self.coordX, (self.coordY - 1), 2)
            self.coordY -= 1
            self.reset_monsters(monsters, environment)
            return True

        # RIGHT
        elif (ch2 == b'M' or ch2 == "C") and (environment.get_coord(self.coordX, (self.coordY + 1)) == 0):
            # If the RIGHT arrow key is pressed and the cell to the right of the Hero is unoccupied, the Hero moves there          
            os.system('cls')
            print("right key pressed")
            environment.set_coord(self.coordX, self.coordY, 0)
            environment.set_coord(self.coordX, (self.coordY + 1), 2)
            self.coordY += 1
            self.health -= 1
            self.reset_monsters(monsters, environment)
            return True
        
        elif (ch2 == b'M' or ch2 == "C") and (environment.get_coord(self.coordX, (self.coordY + 1)) in monster_chars):
            # If the RIGHT arrow key is pressed and the cell to the right of the Hero is occupied by a Monster, the Hero begins interaction
            for monster in monsters:
                if monster.coordX == self.coordX and monster.coordY == (self.coordY + 1):
                    encountered_monster = monster
                    encountered_monster.encountered = True
                    break
            print(f"The Hero is about to encounter a {encountered_monster.name} Monster with the ability of {encountered_monster.ability}")
            input("Press Enter to continue.")
            self.monster_encounter(encountered_monster)
            environment.set_coord(self.coordX, self.coordY, 0)
            environment.set_coord(self.coordX , (self.coordY + 1), 2)
            self.coordY += 1
            return True     

        elif (ch2 == b'M' or ch2 == "C") and (environment.get_coord(self.coordX, (self.coordY + 1)) in goblin_chars):
            # If the RIGHT arrow key is pressed and the cell to the right of the Hero is occupied by a Goblin, the Hero begins interaction
            for goblin in goblins:
                if goblin.coordX == self.coordX and goblin.coordY == (self.coordY + 1):
                    encountered_goblin = goblin
                    encountered_goblin.encountered = True
                    break
            print(f"The Hero is about to encounter a {encountered_goblin.name} Goblin with the ability of {encountered_goblin.ability}")
            input("Press Enter to continue.")
            self.goblin_encounter(encountered_goblin, goblins)
            self.remove_goblin(goblin, goblins)
            environment.set_coord(self.coordX, self.coordY, 0)
            environment.set_coord(self.coordX, (self.coordY + 1), 2)
            self.coordY += 1
            self.reset_monsters(monsters, environment)
            return True      

    def monster_encounter(self, monster):
        if monster.name == "Thief":
            # If the Monster is of type Thief, run the steal function
            stolen_amount, success_rate = monster.steal(self.get_difficulty(self.difficulty))
            if random.random() < success_rate:
                self.coins -= stolen_amount
                input(f"The Monster outsmarted the hero and stole {stolen_amount} coins!")
            else:
                input("The Hero bested the Monster and didn't lose any coins!")
        elif monster.name == "Fighter":
            # If the Monster is of type Fighter, run the fight function
            damage_dealt, success_rate = monster.fight(self.get_difficulty(self.difficulty))
            if random.random() < success_rate:
                self.health -= damage_dealt
                input(f"The Monster manages to wound the Hero! (-{damage_dealt} health)")
            else:
                input("The Hero defeated the monster and got away unscathed!")
        elif monster.name == "Gamer":
            # If the Monster is of type Gamer, run the Rock Paper Scissors function
            print("Press R for Rock, P for Paper, or X for Scissors")
            stolen_amount, damage_dealt = monster.rps(self.get_difficulty(self.difficulty))
            rps_options = ["Rock", "Paper", "Scissors"]
            monster_hand = random.choice(rps_options)
            hero_hand = getch()            
            if (hero_hand == b'r' and monster_hand == "Scissors") or (hero_hand == b'p' and monster_hand == "Rock") or (hero_hand == b'x' and monster_hand == "Paper"):
                input("The Hero wins the game and is free to go!")
            elif (hero_hand == b'r' and monster_hand == "Rock") or (hero_hand == b'p' and monster_hand == "Paper") or (hero_hand == b'x' and monster_hand == "Scissors"):
                input("Draw. Try again!")
                self.monster_encounter(monster)           
            elif (hero_hand == b'r' and monster_hand == "Paper") or (hero_hand == b'p' and monster_hand == "Scissors") or (hero_hand == b'x' and monster_hand == "Rock"):
                self.coins -= stolen_amount
                self.health -= damage_dealt
                input(f"The Hero loses the game and has to part with {stolen_amount} coins and suffer {damage_dealt} health points worth of damage!")
            else:
                input("Hand not recognised")
                self.monster_encounter(monster)

    def goblin_encounter(self, goblin, goblins):
        if goblin.name == "Wealth":
            # If the Goblin is of type Wealth, run the reward function
            coins_awarded, success_rate = goblin.reward(self.get_difficulty(self.difficulty))
            if random.random() < success_rate:
                self.coins += coins_awarded
                input(f"The Hero befriended the Goblin and received {coins_awarded} coins!")
            else:
                input("The Goblin found the Hero untrustworthy and left!")
        elif goblin.name == "Health":
            # If the Goblin is of type Health, run the heal function
            health_recovered, success_rate = goblin.heal(self.get_difficulty(self.difficulty))
            if random.random() < success_rate:
                self.health += health_recovered
                input(f"The Hero won the Goblin's trust, who in turn bandaged their wounds! (+{health_recovered} health)")
            else:
                input("The Goblin was suspicious of the Hero and decided not to help them!")
        elif goblin.name == "Gamer":
            # If the Goblin is of type Gamer, run the Rock Paper Scissors function
            print("Press R for Rock, P for Paper, or X for Scissors")
            coins_awarded, health_recovered = goblin.rps(self.get_difficulty(self.difficulty))
            rps_options = ["Rock", "Paper", "Scissors"]
            goblin_hand = random.choice(rps_options)
            hero_hand = getch()
            if (hero_hand == b'r' and goblin_hand == "Scissors") or (hero_hand == b'p' and goblin_hand == "Rock") or (hero_hand == b'x' and goblin_hand == "Paper"):
                self.coins += coins_awarded
                self.health += health_recovered
                input(f"The Hero wins the game and is awarded {coins_awarded} coins and healed for {health_recovered} health points!")
            elif (hero_hand == b'r' and goblin_hand == "Rock") or (hero_hand == b'p' and goblin_hand == "Paper") or (hero_hand == b'x' and goblin_hand == "Scissors"):
                input("Draw. Try again!")
                self.goblin_encounter(goblin, goblins)           
            elif (hero_hand == b'r' and goblin_hand == "Paper") or (hero_hand == b'p' and goblin_hand == "Scissors") or (hero_hand == b'x' and goblin_hand == "Rock"):
                input("The Hero loses the game and continues their journey with empty hands!")
            else:
                input("Hand not recognised")
                self.goblin_encounter(goblin, goblins)

    def reset_monsters(self, monsters, environment):
        # After each turn, the monsters are reset on the map as they never disappear
        for monster in monsters:
            monster.reset_monster(monster, environment)

    def remove_goblin(self, goblin, goblins):
        # When a goblin is encountered, it is removed from the game
        for goblin in goblins:
            if goblin.encountered == True:
                goblins.remove(goblin)

    def get_difficulty(self, difficulty):
        # Get the difficulty multipliers
        if difficulty == "EASY":
            return 1
        elif difficulty == "MEDIUM":
            return 1.5
        elif difficulty == "HARD":
            return 2
        elif difficulty == "VERY HARD":
            return 2.5
        
if os.path.basename(sys.argv[0]) != "playgame.py":
    script_path = os.path.join(os.path.dirname(__file__), "playgame.py")
    print(f"Wrong file executed! Running '{script_path}' instead...")
    os.system(f'python "{script_path}"')
    sys.exit()