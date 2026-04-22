import json, sys, os, subprocess, re, requests, string, time, threading, climage
from colorama import *
from bs4 import *



global config
global cfg
cfg = {}
config = None

def getConfig():
    global config
    global cfg
    while not config: # Get the config file and reset it if it has errors
        # Todo rewrite this to be included in main, need to have malformed config checks
        try:
            config = open("cfg.json", 'r')
            try:
                cfg = json.load(config)
                config.close()
                return config, cfg
            except(json.JSONDecodeError):
                resetConfig()
                config = open("cfg.json", 'r')
                cfg = json.load(config)
                config.close()
                return config, cfg
        except(FileNotFoundError):
            resetConfig()
            config = open("cfg.json", 'r')
            cfg = json.load(config)
            config.close()
            return config, cfg

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

def printMessage(text, style):
    match(style):
        case "err":
            print(Fore.RED + "ERROR\t" + Fore.WHITE + f"{text}")
        case "warn":
            print(Fore.YELLOW + "WARN\t" + Fore.WHITE + f"{text}")
        case "info":
            print(Fore.BLUE + "INFO\t" + Fore.WHITE + f"{text}")
        case "log":
            print(Fore.GREEN + "LOG\t" + Fore.WHITE + f"{text}")
        case _:
            sys.exit()

def checkGameExists():
    if os.path.isfile(f"{cfg['gameDirectoryString']}Contract Rush DX.exe"):
        printMessage(f"Game found at {cfg['gameDirectoryString']}Contract Rush DX.exe", "log")
        return True
    else:
        printMessage(f"Contract Rush DX.exe not found in game directory {cfg['gameDirectoryString']}.", "warn")
        return False

def checkFolderModsExist():
    if os.path.isfile(f"{cfg['gameDirectoryString']}/Mods"):
        printMessage(f"Mods folder found in game directory.", "log")
        return True
    else:
        printMessage(f"Mods folder not found in game directory. Have you run the \'setup\' command?", "warn")
        return False

def checkFolderDisabledExist():
    if os.path.isfile(f"{cfg['gameDirectoryString']}/DisabledMods"):
        printMessage(f"DisabledMods folder found in game directory.", "log")
        return True
    else:
        printMessage(f"DisabledMods folder not found in game directory. Have you run the \'setup\' command?", "warn")
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
    print(climage.convert('../assets/loader/CMLLogo.png', width=40))
    printMessage("CyrusModLoader command line tool release NULL", "info")
    printMessage("Type \"help\" for a list of commands.", "info")

    # Open config file when application starts.
    # If config is found, open it. If config is not found, then create a new file and try to open it. 
    # (TODO: make it fill blank fields, add messages to notify user of malformed or missing config and if the script reset them)
    global config
    global cfg
    config, cfg = getConfig()

    checkGameExists()
    checkFolderModsExist()
    checkFolderDisabledExist()

    while True:
        userInput = input(Fore.CYAN + "\nCML" "> " + Fore.WHITE)

        # Intercept single word commands
        match (userInput):
            case "exit":
                sys.exit()
            case "list":
                listMods()
            case "help":
                print("help text todo later")
            case "install":
                print("bepinex automated installer placeholder")
            case "setup":
                print("setup folders")
                if os.path.isfile(f"{cfg['gameDirectoryString']}Contract Rush DX.exe"):
                    printMessage(f"Game found at {cfg['gameDirectoryString']}Contract Rush DX.exe", "log")
                    gameExists = True
                else:
                    gameExists = False
                    printMessage(f"Contract Rush DX.exe not found in game directory {cfg['gameDirectoryString']}.", "warn")
                
                # ALSO NEED TO ADD A CHECK TO FIND IF BEPINEX EXISTS, idk if this is correct yet, need to check for if installed
                if os.path.isfile(f"{cfg['gameDirectoryString']}BepInEx"):
                    printMessage(f"BepInEx found in game directory.", "log")
                    bpxExists = True
                else:
                    printMessage(f"BepInEx not found in game directory.", 'warn')
                    bpxExists = False
                
                if ((bpxExists == True) and (gameExists == True)):
                    print("placeholder for executing setup")
                else:
                    printMessage(f"Contract Rush DX.exe is not found in game directory, and/or BepInEx is not installed. Cannot continue with setup.", 'err')

            case "info":
                print("Variable\t\tValue")
                print("--------\t\t-----")
                print(f"Game Directory\t\t{cfg['gameDirectoryString']}")


            case _: #If the command has input argument it will get directed to the regex to parse that out
                    cmd = re.search(r"([a-z]+)\s((?:[^\s]|.*\/)+)(?:\s([^\s]+))*", userInput)
                    if cmd:
                        match(cmd.group(1)): # Match the commands out and execute them
                            case 'gamedir':
                                printMessage("Reminder that you should fully declare your file path at the end with a slash, such as /example/game/dir/ . The script can't understand a partial directory, like /example/game/dir . If you are having issues with the script but you think your directory path is otherwise correct, this might be why.", 'warn')
                                # Check to make sure directory stuff is consistent
                                if not re.search(r".*\/$", cmd.group(2)): 
                                    arg1 = cmd.group(2) + "/"
                                else:
                                    arg1 = cmd.group(2)
                                
                                # Check if input directory exists
                                if os.path.exists(arg1):
                                    printMessage(f"Game directory set to {arg1}.", 'info')
                                    checkGameExists()
                                    checkFolderModsExist()
                                    checkFolderDisabledExist()
                                    cfg['gameDirectoryString'] = arg1
                                    config = open('cfg.json', 'w')
                                    json.dump(cfg, config)
                                    config.close()
                                    printMessage("Changes written to cfg.json.", 'info')
                                else:
                                    printMessage(f"Directory \'{cmd.group(2)}\' does not exist!", 'err')
                            case _:
                                printMessage(f"Command \'{cmd.group(1)}\' does not exist!", 'err')
                    else:
                        printMessage(f"Command \'{userInput}\' does not exist!", 'err')

main()

