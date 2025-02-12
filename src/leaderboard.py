import pickle
import os
import sys

class Leaderboard:

    def __init__(self, file_name="pickle/leaderboard.pkl"):
        self.file_name = file_name
        self.leaderboard = {
            "EASY": [],
            "MEDIUM": [],
            "HARD" : [],
            "VERY HARD": []
        }

        # Ensure the directory exists
        self.ensure_directory()

        # Load the leaderboard data
        self.load_leaderboard()

    def ensure_directory(self):
        # Ensure the directory for the file exists
        directory = os.path.dirname(self.file_name)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def save_leaderboard(self):
        # Save leaderboard data to file
        with open(self.file_name, "wb") as file:
            pickle.dump(self.leaderboard, file)

    def load_leaderboard(self):
        # Load leaderboard data from file
        if os.path.exists(self.file_name):
            with open(self.file_name, "rb") as file:
                self.leaderboard = pickle.load(file)

    def add_new_score(self, difficulty, score):
        # Add a new score to the leaderboard only if it qualifies for the top 10
        if difficulty not in self.leaderboard:
            raise ValueError(f"Invalid difficulty: {difficulty}")   
        scores = self.leaderboard[difficulty]
        if len(scores) < 10:
            name = input("You have reached TOP 10 in the leaderboard! Enter your name: ").strip()
            while not name:
                print("Input cannot be blank.")
                name = input("You have reached TOP 10 in the leaderboard! Enter your name: ").strip()
            scores.append({"name": name, "score": score})
        else:
            # Check if the new score is higher than the lowest score in the top 10
            min_score = min(scores, key=lambda x: x["score"])["score"]
            if score > min_score:
                name = input("You have reached TOP 10 in the leaderboard! Enter your name: ").strip()
                while not name:
                    print("Input cannot be blank.")
                    name = input("You have reached TOP 10 in the leaderboard! Enter your name: ").strip()
                # Replace the lowest score with the new score
                scores.append({"name": name, "score": score})
                scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]
        # Update and save leaderboard
        self.leaderboard[difficulty] = scores
        self.save_leaderboard()  
        self.print_leaderboard(difficulty)
        input("")
        
    def print_leaderboard(self, difficulty):
        if difficulty not in self.leaderboard:
            raise ValueError(f"Invalid difficulty: {difficulty}")
        if not self.leaderboard[difficulty]:
            print(f"\n{difficulty.capitalize()} Leaderboard is empty.")
            return
        title = f" {difficulty.capitalize()} Leaderboard "
        border_length = max(len(title), 30)  # Ensure title border is wide enough

        print("+" + "-" * border_length + "+")
        print(f"|{title.center(border_length)}|")
        print("+" + "-" * border_length + "+")
        print("+----+------------+------------+")
        print("| #  | Name       | Score      |")
        print("+----+------------+------------+")

        # Ensure scores are sorted in descending order before printing
        sorted_scores = sorted(self.leaderboard[difficulty], key=lambda x: x["score"], reverse=True)

        for rank, entry in enumerate(sorted_scores, start=1):
            print(f"| {rank:<2} | {entry['name']:<10} | {entry['score']:>10} |")
        print("+----+------------+------------+")

if os.path.basename(sys.argv[0]) != "playgame.py":
    script_path = os.path.join(os.path.dirname(__file__), "playgame.py")
    print(f"Wrong file executed! Running '{script_path}' instead...")
    os.system(f'python "{script_path}"')
    sys.exit()


