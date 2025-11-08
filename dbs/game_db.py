import csv
import fnmatch

game_db = "./game-db.csv"

class GameDb:
    def __init__(self):
        self.games = []
        with open(game_db, newline='', encoding="ISO-8859-1") as csv_file:
            reader = csv.reader(csv_file, delimiter=";")
            next(reader, None)
            next(reader, None)
            for row in reader:
                self.games.append({
                    "title": row[0],
                    "game_id": row[1],
                    "version": row[2],
                    "edition": row[3],
                    "date": row[4],
                    "region": row[5],
                    "languages": row[6],
                })

    def find_games(self, search:str):
        matched_games = []
        for game in self.games:
            if fnmatch.fnmatch(game["title"].lower(), f"*{search.lower()}*"):
                matched_games.append(game)

        return matched_games
