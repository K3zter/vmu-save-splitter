from vmu.vmu import Vmu;
from vmu.vmu_file import VmuFile;
from file_log import FileLog
from dbs.save_db import SaveDb;
from dbs.game_db import GameDb;
import configparser
import fnmatch
import os
from pathlib import Path
import shutil

config = configparser.ConfigParser()

try:
     with open('./cfg.ini') as f:
          config.read_file(f)
except IOError:
     raise Exception("cfg.ini missing")

import_dir = "./import/"
export_dir = "./export/"

if (not "Options" in config):
     raise Exception("cfg.ini invalid")

if (not "loader" in config["Options"]):
     raise Exception("'loader' option missing from config.")

regions = config["Options"]["region"].split(",") if "region" in config["Options"] else []
loader = config["Options"]["loader"]

save_db = SaveDb()
game_db = GameDb()
file_log = FileLog()

def empty_export_folder():
    export_folder = Path(export_dir)
    if(export_folder.is_dir()):
        shutil.rmtree(export_dir)
        
    Path(export_dir).mkdir()
         

def match_game(matches, file_name):
    matched_game = None
    if(loader == "disc"):
        fmids = []
        for match in matches:
              fmids.append(match["fmid"])
        if(len(set(fmids)) == 1):
             return matches[0]

    for region in regions:
        for match in matches:
            if match["region"] == region:
                matched_game = match

    if (matched_game):
            return matched_game
            
    print(f"\n{len(matches)} matches for {file_name}:")
    for index, match in enumerate(matches):
            title = match["title"]
            region = match["region"]
            print(f"   [{index + 1}] {title} ({region})")

    selection = input("Select the matching game from the list above (Leave blank to skip):\n")
    if selection and matches[int(selection)-1]:
            match = matches[int(selection)-1]
            matched_game = match
    else:
            print("Skipping...\n")

    return matched_game

def format_game_id(game_id: str):
    if (loader == "openMenu"):
        if(game_id.find(" ") > -1):
            return game_id[:game_id.find(" ")].replace("-","").replace(" ", "").strip()
    # if (loader == "MODE"):
    #     if(game_id.rfind(" ") > -1):
    #         return game_id[:game_id.rfind(" ")].replace("-","").replace(" ", "").strip()
        
    return game_id.replace("-","").replace(" ", "").strip()

def split_files(vmu: Vmu):
    new_vmus = {}
    for file in vmu.directory.files():
        if (file.file_name == "ICONDATA_VMS"):
             continue
        matches = []
        for index,save_name in enumerate(save_db.save_names):
            if fnmatch.fnmatch(file.file_name, save_name):
                matches.append(save_db.save_data[index])
            
        matched_game = None
        if(len(matches) == 0):
            print(f"No matches for {file.file_name}")
            if(loader != "disc"):
                current_file = vmu.get_file(file.index)
                result = find_game(file.file_name, current_file)
                if(result):
                    matched_game = {
                        "title": result["title"],
                        "game_id": result["game_id"],
                        "region": result["region"],
                        "fmid": ""
                    }

        elif(len(matches) == 1):
                matched_game = matches[0]
        else:
            matched_game = match_game(matches, file.file_name)

        if (matched_game):
            game_id = matched_game["fmid"] if loader == "disc" else format_game_id(matched_game["game_id"])
            print(f'Matched {matched_game["title"]} ({matched_game["region"]}): {game_id}')
            current_file = vmu.get_file(file.index)
            new_vmu: Vmu = new_vmus[game_id] if game_id in new_vmus else Vmu("./blank.vmu")

            new_vmu.add_file(current_file)
            new_vmus[game_id] = new_vmu
    
    for game_id, new_vmu in new_vmus.items():
        game_dir = Path(export_dir + game_id)
        if(not game_dir.is_dir()):
             game_dir.mkdir()

        i = 1
        while i <= 8:
            file_path = f"{export_dir}{game_id}/{game_id}-{i}.vmu"
            if Path(file_path).is_file():
                i += 1
            else:
                new_vmu.save_vmu(file_path)
                break

def find_game(file_name: str, file: VmuFile):
    print(f"File Data:")
    print(f"{file_name}")
    print(f"{file.desc}")
    print(f"{file.desc_long}")
    if(input("Search for matching game? (y/N):\n") == "y"):
        try_again = True
        while (try_again == True):
            try_again = False

            search = input("Type a string to search for:\n")
            results = game_db.find_games(search)

            print(f"\n{len(results)} matches for \"{search}\":")

            if(len(results) == 0):
                try_again = True if input("Try again? (y/N):\n") == "y" else False
                continue

            for index, result in enumerate(results):
                title = result["title"]
                region = result["region"]
                game_id = result["game_id"]
                edition = result["edition"]
                print(f"   [{index + 1}] {title} ({region}) [{game_id.strip()}] Edition: {edition}")

            selection = input("Select the matching game from the list above (Leave blank to abort):\n")
            if selection and results[int(selection)-1]:
                result = results[int(selection)-1]
                chosen_game = result
                title = result["title"]
                region = result["region"]
                game_id = result["game_id"]
                edition = result["edition"]
                file_log.write_line(f"[{file_name}] matched to {title} ({region}) [{game_id}] Edition: {edition}")
                return chosen_game
    
    file_log.write_line(f"[{file_name}] - no match found")
    return None
           


empty_export_folder()

vmuList =Path(import_dir).glob("*.vmu")

for vmu in vmuList:
    currentVmu = Vmu(str(vmu))
    currentVmu.list()
    split_files(currentVmu)