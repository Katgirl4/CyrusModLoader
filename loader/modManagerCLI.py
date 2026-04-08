import json, sys, os, subprocess, re, requests, string, time, threading
from colorama import *
from bs4 import *

# Open config file when application starts.
    # If config is found, open it. If config is not found, then create a new file and try to open it. (TODO: make it fill blank fields)
def resetConfig(): # Function for resetting the config if it has an error or creating it if it does  not exist.
    try:
        os.remove("cfg.json")
        config = open("cfg.json", 'w')
    except(FileNotFoundError):
        config = open("cfg.json", 'w')
    
    json.dump({
    'gameDirectoryString' : '/dev/null',
    }, config, indent=4)
    config.close()

# Dict of error messages for the error popup

config = None
cfg = {}
while not cfg: # Get the config file and reset it if it has errors
    try:
        config = open("cfg.json", 'r')
        try:
            cfg = json.load(config)
            config.close()
        except(json.JSONDecodeError):
            resetConfig()
            config = open("cfg.json", 'r')
            cfg = json.load(config)
            config.close()
    except(FileNotFoundError):
        resetConfig()
        config = open("cfg.json", 'r')
        cfg = json.load(config)
        config.close()


def printMessage(text, style):
    match(style):
        case "err":
            print(Fore.RED + "ERROR " + Fore.WHITE + f"{text}")
        case "warn":
            print(Fore.YELLOW + "WARN " + Fore.WHITE + f"{text}")
        case "info":
            print(Fore.BLUE + "INFO " + Fore.WHITE + f"{text}")
        case "log":
            print(Fore.GREEN + "LOG " + Fore.WHITE + f"{text}")
        case _:
            sys.exit()



def checkGameExists():
    if os.path.isfile(f"{cfg['gameDirectoryString']}Contract Rush DX.exe"):
        printMessage(f"Game found at {cfg['gameDirectoryString']}Contract Rush DX.exe", "LOG")
        return True
    else:
        printMessage(f"Contract Rush DX.exe not found in game directory {cfg['gameDirectoryString']}/.", "warn")
        return False

def checkFolderModsExist():
    if os.path.isfile(f"{cfg['gameDirectoryString']}/Mods"):
        printMessage(f"Game found at {cfg['gameDirectoryString']}Contract Rush DX.exe", "LOG")
        return True
    else:
        printMessage(f"Mods folder not found at {cfg['gameDirectoryString']}/. Have you run the \'setup\' command?", "warn")
        return False

def checkFolderDisabledExist():
    if os.path.isfile(f"{cfg['gameDirectoryString']}/DisabledMods"):
        printMessage(f"DisabledMods folder found at {cfg['gameDirectoryString']}/DisabledMods/", "LOG")
        return True
    else:
        printMessage(f"DisabledMods folder not found at {cfg['gameDirectoryString']}/. Have you run the \'setup\' command?", "warn")
        return False

def checkBepInExExist():
    pass

def listMods(): # Get list of files, put mods into dir, problem solved
    print("test mod list")

def toggleMod(modName):
    pass

def setup():
    pass

def install():
    pass

def main():
    printMessage("CyrusModLoader command line tool release NULL", "info")
    printMessage("Type \"help\" for a list of commands.", "info")
    checkGameExists()
    checkFolderModsExist()
    checkFolderDisabledExist()

    validCommandsWithArgs = ['toggle', 'gamedir']
    while True:
        userInput = input(Fore.CYAN + "CML" "> " + Fore.WHITE)

        # Intercept single word commands
        if userInput == "exit":
            sys.exit()
        elif userInput == "list":
            listMods()
        elif userInput == "help":
            print("help text todo later")
        elif userInput == "install":
            print("bepinex automated installer placeholder")
        elif userInput == "setup":
            print("setup folders")

        # Else, pass on to regex parser
        else:
            re.search(r"", userInput) # Pull the command and argument out

main()

