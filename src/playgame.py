from hero import Hero
from monster import Monster, Thief_Monster, Fighter_Monster, Gamer_Monster
from goblin import Goblin, Wealth_Goblin, Health_Goblin, Gamer_Goblin
from leaderboard import Leaderboard
from gamedatabase import GameSaver
from maze_gen_recursive import make_maze_recursion
from copy import deepcopy
from getch1 import *
import random
import os

WALL_CHAR = "#"
SPACE_CHAR = "-"
HERO_CHAR = "H"
MONSTER_CHAR = "M"
GOBLIN_CHAR = "G"

# Difficulty variables
EASY = 1
MEDIUM = 1.5
HARD = 2
VERY_HARD = 2.5


class Environment:
    """Environment includes Maze+Monster+Goblin"""
    def __init__(self, maze):
        self.environment = deepcopy(maze)

    def set_coord(self, x, y, val):
        self.environment[x][y] = val

    def get_coord(self, x, y):
        return self.environment[x][y]


    def print_environment(self):
        """print out the environment in the terminal"""
        for row in self.environment:
            row_str = str(row)
            row_str = row_str.replace("1", WALL_CHAR)  # replace the wall character
            row_str = row_str.replace("0", SPACE_CHAR)  # replace the space character
            row_str = row_str.replace("2", HERO_CHAR)  # replace the hero character
            row_str = row_str.replace("3", MONSTER_CHAR) # replace the thief monster
            row_str = row_str.replace("4", MONSTER_CHAR) # replace the fighter monster
            row_str = row_str.replace("5", MONSTER_CHAR) # replace the gamer monster
            row_str = row_str.replace("6", GOBLIN_CHAR) # replace the wealth goblin
            row_str = row_str.replace("7", GOBLIN_CHAR) # replace the health goblin
            row_str = row_str.replace("8", GOBLIN_CHAR) # replace the gamer goblin
            print("".join(row_str))


class Game:

    _count = 0

    def __init__(self, difficulty, load_data=None):
        self.gamesaver = GameSaver()

        if load_data:
            self.__dict__.update(load_data) # Restore saved attributes
        else:
            self.difficulty = difficulty
            self.maze = make_maze_recursion(17, 17)
            self.monsters = []
            self.goblins = []
            self.myHero = Hero(self.difficulty)
            self.myHero.spawn(self.maze)
            self.maze[self.myHero.coordX][self.myHero.coordY] = 2
            self.spawn_monsters(5)
            self.spawn_goblins(5)
            self.MyEnvironment = Environment(self.maze)  # initial environment is the maze itself
            self.count = 0
            self.leaderboard = Leaderboard()

    def spawn_monsters(self, number):

        monster_types = (Thief_Monster, Fighter_Monster, Gamer_Monster)

        self.monsters.append(Thief_Monster())
        self.monsters.append(Fighter_Monster())
        self.monsters.append(Gamer_Monster())

        if number > 3:
            for _ in range(number - 3):
                random_type = random.choice(monster_types)
                self.monsters.append(random_type())

        for monster in self.monsters:
            Monster.spawn_monster(monster, self.maze)
            if monster.name == "Thief":
                self.maze[monster.coordX][monster.coordY] = 3
            elif monster.name == "Fighter":
                self.maze[monster.coordX][monster.coordY] = 4
            elif monster.name == "Gamer":
                self.maze[monster.coordX][monster.coordY] = 5

    def spawn_goblins(self, number):

        goblin_types = (Wealth_Goblin, Health_Goblin, Gamer_Goblin)

        self.goblins.append(Wealth_Goblin())
        self.goblins.append(Health_Goblin())
        self.goblins.append(Gamer_Goblin())

        if number > 3:
            for _ in range(number - 3):
                random_type = random.choice(goblin_types)
                self.goblins.append(random_type())

        for goblin in self.goblins:
            Goblin.spawn_goblin(goblin, self.maze)
            if goblin.name == "Wealth":
                self.maze[goblin.coordX][goblin.coordY] = 6
            elif goblin.name == "Health":
                self.maze[goblin.coordX][goblin.coordY] = 7
            elif goblin.name == "Gamer":
                self.maze[goblin.coordX][goblin.coordY] = 8

    def check_win_condition(self):
        for monster in self.monsters:
            if monster.encountered == False:
                return False
        return True
    
    def check_lose_condition(self):
        return self.myHero.health <= 0

    
    def display_locations(self):

        # Prints the coordinates of the hero
        print("")
        print("=============================HERO==============================")
        print(f"coordinates: {self.myHero.coordX, self.myHero.coordY} | You start with 100 health and 100 coins!")
        print("")
        
        # Prints the coordinates and the ability of all monsters, currently in the maze
        print("===========================MONSTERS============================")
        monsters_left = []
        for monster in self.monsters:
            if not monster.encountered:
                monsters_left.append(monster)

        print(f"There are {len(monsters_left)} monsters left to encounter:")
        for monster in monsters_left:
            print(f"{monster.name} Monster at coordinates {monster.coordX, monster.coordY} with ability of {monster.ability}")
        print("")

        # Prints the coordinates and the ability of all goblins, currently in the maze

        print("===========================GOBLINS=============================")
        print(f"There are {len(self.goblins)} goblins left to encounter:")
        for goblin in self.goblins:
            print(f"{goblin.name} Goblin at coordinates {goblin.coordX, goblin.coordY} with ability of {goblin.ability}")

    @staticmethod
    def load_game():
        # Loads a saved game as a new instance.
        saver = GameSaver()
        saved_data = saver.load_game()
        if saved_data:
            return Game(None, saved_data)  # Restore game state into a new object
        return None

    def play(self):
        os.system('cls')
        print("===================================================")
        print("==============Welcome=to=MAZE=CRAWLER==============")
        print("===================================================")
        print("In this game, you navigate your hero(H) through")
        print("a maze, filled with monsters(M), who are your ")
        print("enemies, and goblins(G), who are your friends.")
        print("The goal of the game is to encounter all monsters")
        print("at least once, and survive. If you do, you will")
        print("be asked to input your name, and based on your")
        print("score(coins left) and difficulty, you will be")
        print("placed in a leaderboard of the TOP 10 players.")
        print("===================================================")
        self.MyEnvironment.print_environment()
        self.print_environment_frame()
        

        while True:

            ch2 = getch()

            if ch2 == b'h':
                # Prints the game manual with all the controls when you press h
                print("\n===============MOVEMENT==============")
                print("LEFT arrow key == go left \n" +
                      "RIGHT arrow key == go right \n" +
                      "UP arrow key == go up \n" +
                      "DOWN arrow key == go down\n")
                print("=========ROCK=PAPER=SCISSORS=========")
                print("R key == choose ROCK \n" +
                      "P key == choose PAPER \n" +
                      "X key == choose SCISSORS \n")
                print("============MISCELLANEOUS============")
                print("M key == display the location of the characters")
                print("Y key == display the leaderboard for the current difficulty")
                print("================SYSTEM===============\n")
                print("S key == save your game")
                print("L key == load game from saved file")
                print("Q key == quit the game")
                continue

            if ch2 == b'm':
                self.display_locations()
                continue

            if ch2 == b'y':
                self.leaderboard.print_leaderboard(self.difficulty)
                continue

            if ch2 == b's':
                self.gamesaver.save_game(self)
                continue

            if ch2 == b'l':
                self.gamesaver.load_midgame(self)
                continue

            if self.myHero.move(self.MyEnvironment, self.monsters, self.goblins):
                os.system('cls')
                #if self.myHero.move_debug(self.MyEnvironment):  #this works in debug mode
                print("===================================================")
                self.MyEnvironment.print_environment()
                self.count += 1
                self.print_environment_frame()
                
                

            if self.check_win_condition():
                input("All monsters have been defeated. YOU WIN!")
                self.myHero.coins += self.myHero.health
                self.leaderboard.add_new_score(self.difficulty, self.myHero.coins)
                break
            
            if self.check_lose_condition():
                input("Health reached 0. YOU LOSE!")
                self.leaderboard.add_new_score(self.difficulty, self.myHero.coins)
                break

    def print_environment_frame(self):
        print("===================================================", self._count)
        print("Health: ", self.myHero.health, " Coins: ", self.myHero.coins, end = "   ||   ")
        print("Press h for HELP!")
        print("===================================================")
                          

if __name__ == "__main__":
    os.system('cls')
    # The beginning screen of the game which lets the player choosel
    # whether to start a new game or load a previous game
    print("========================MAZE=CRAWLER========================")
    print("")
    print("Press N to start a new game! | Press L to load a saved game!")
    print("")
    print("============================================================")
    print("\t\tCreated by: Ivan Gavanozov")
    start_choice = getch()
    os.system('cls')
    if start_choice == b'n':
        # After choosing a new game the player is required to choose
        # a difficulty which affects the abilities of the monsters and goblins
        print("===================Choose=your=difficulty===================")
        print("")
        print("    | 1 - Easy | 2 - Medium | 3 - Hard | 4 - Very Hard |    ")
        print("")
        print("============================================================")
        difficulty = 0
        difficulty_choice = getch()
        if difficulty_choice == b'1':
            difficulty = "EASY"
        elif difficulty_choice == b'2':
            difficulty = "MEDIUM"
        elif difficulty_choice == b'3':
            difficulty = "HARD"
        elif difficulty_choice == b'4':
            difficulty = "VERY HARD"
        myGame = Game(difficulty)
        myGame.play()
    elif start_choice == b'l':
        myGame = Game.load_game()
        if myGame:
            myGame.play()
        else:
            print("No saved game found. Starting a lnew game.")
            myGame = Game("EASY")
            myGame.play()


    #myGame = Game("EASY")
    #myGame.play()
    