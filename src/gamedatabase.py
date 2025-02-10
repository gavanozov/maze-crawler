import pickle
import os

class GameSaver:
    # This class deals with saving and loading the game to and from a pickle file.
    def __init__(self, save_file="pickle/gamesave.pkl"):
        self.save_file = save_file

    def save_game(self, game):
        # Saves the current game state to a file
        with open(self.save_file, "wb") as file:
            pickle.dump(game.__dict__, file)
        print("Game saved successfully!")

    def load_game(self):
        # Loads a saved game as a new instance of Game
        if not os.path.exists(self.save_file):
            print("No saved game found!")
            return None

        with open(self.save_file, "rb") as file:
            saved_data = pickle.load(file)
            print("Game loaded successfully!")
            return saved_data  # Returns the dictionary of saved attributes
        
    def load_midgame(self, game):
        # Loads a saved game into an already running game instance
        os.system('cls')
        saved_data = self.load_game()
        if saved_data:
            game.__dict__.update(saved_data)  # Overwrite the current game state
            print("===================================================")
            game.MyEnvironment.print_environment()  # Refresh display
            game.print_environment_frame() 
        else:
            print("No saved game found!") 