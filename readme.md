# VMU Save Splitter
Python script for taking Dreamcast VMU dumps (in the `.vmu` format) and splitting the contained save files out into individual VMCs, for use with modern VMU alternatives such as VMU Pro.

**WARNING: The script is still considered to be experimental, it has not been thoroughly tested. Use at your own risk and ensure you retain a back of up your existing VMU files.**

## Requirements
Script is written in Python 3 with no additional libraries required. Install Python 3 if you don't have it already.

## Basic Usage
1. Place your existing `.vmu` files in the `import` directory
2. Run the command `python vmu_splitter.py` in a terminal from within the project directory
3. Follow the on-screen instructions
4. Copy & paste the contents of the `export` directory to your VMU SD card

## Config
The project includes a `cfg.ini` file with the following options:
- `region`: Filling this in with a region makes the script require less user input. If you know all your saves are from the same region, enter it here and the script will automatically select games from that region when it finds a match. Main regions are `USA`, `Europe` and `Japan`. Some PAL versions also have more specific regions such as `Australia`, `France`, `Italy`, `Germany`, `UK`. You can place multiple entries in this setting, separated by a comma. The script will look for each region in order.
- `loader`: Depending on whether you are using an ODE or disc-based displayID matching the output vmu file/folder structure may vary. If you are using a GDEMU, putting `openMenu` here is recommended and ensure you are using a version of openMenu that supports sending GameID. MODE users select `MODE` and ensure you have the latest firmware. Otherwise, choose `disc` - this mode currently tries to use the same files that a VMU Pro would select when using DisplayID matching.
- `empty`: When this is set to `1`, the script will clear all files from the `export` directory before it runs. The script is designed in such a way that you put all your VMU files in the `import` dir and then run it once, and the `export` dir will contain your new files. However, if you wish to run the script in smaller batches then you can disable this option. Be aware that if this option is disabled and you run the script multiple times on the same import files, it will create duplicate files in the export dir on every run.

## Detailed Information
I have assembled a list of known save files and what games they belong to (`save-db.csv`), if an imported VMU contains a file in this list, it will match automatically to a single game. If you have not selected a default region, you will be asked to choose which region game it is (Some saves are region-specific, or for games only released in a single region - these will automatically match without user input). 

However, the save db is far from complete, and if a save file is not recognised you will instead be presented with the info extracted from the save and given the option to search for the game in the redump list (`game-db.csv`). This is a simple string search, so best to just type in a word from the title. If you are able to locate a matching game it will be sorted into its respective gameid vmu, and your selection will be recorded in a log file called `file_log_<current_time>.txt`. It is my hope that people will share these new matches with me so that the save db can grow over time! Feel free to raise an issue with any missing games you match, or find me on discord.