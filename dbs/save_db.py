import csv

save_db = "./save-db.csv"

class SaveDb:
    def __init__(self):
        self.save_names = []
        self.save_data = []
        with open(save_db, newline='', encoding="ISO-8859-1") as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)
            for row in reader:
                self.save_names.append(row[0])
                self.save_data.append({
                    "title": row[1],
                    "game_id": row[2],
                    "region": row[3],
                    "fmid": row[4],
                })
