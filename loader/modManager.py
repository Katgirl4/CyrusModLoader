import json, gi, sys, os, subprocess, re, requests, string, time, threading
from bs4 import *

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Open config file when application starts.
    # If config is found, open it. If config is not found, then create a new file and try to open it. (TODO: make it fill blank fields)
def resetConfig(): # Function for resetting the config if it has an error or creating it if it does  not exist.
    try:
        os.remove("cfg.json")
        config = open("cfg.json", 'w')
    except(FileNotFoundError):
        config = open("cfg.json", 'w')
    
    json.dump({
    'gameDirectoryString' : '~/',
    'disableDirectoryString' : '~/Disabled/'}, config, indent=4)
    config.close()

# Dict of error messages for the error popup
global errorMessages
errorMessages = {
    "executableNotFound":"Cannot find \"Contract Rush DX.exe\" in provided game directory! Install of BepInEx aborted.",
    "bpxNotInstalled":"BepInEx does not appear to be installed in provided game directory.",
    "directoryNotFound":"That directory does not exist! Please input a valid directory. Maybe you forgot an ending \"/\" or a capitalization?",
    "regexFailure":"RegEx that should always match failed to match!",
    "cannotFindBPXRepo":"GET request to github.com failed!"
}

global infoMessages
infoMessages = {
    "automaticInstallComplete":"All automated install steps possible have been completed. Some manual configuration is required."
}

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


# Main (and only) window (probably).
class MainWindow(Gtk.Window):
    
    def __init__(self):
        
        super().__init__(title="CyrusModManager")
        self.set_border_width(5)
        self.set_default_size(400,300)

        self.outerBox = Gtk.HBox(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    
        self.directoryBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.directoryBox.set_homogeneous(False)

        self.modsBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.modsBox.set_homogeneous(False)

        self.add(self.outerBox)
        
        self.outerBox.pack_start(self.directoryBox, True, True, 0)
        self.outerBox.pack_start(self.modsBox, True, True, 0)

        self.gameDirectoryLabel = Gtk.Label()
        self.gameDirectoryLabel.set_text(f"Full path to game directory: {cfg['gameDirectoryString']}")
        self.gameDirectoryLabel.set_justify(Gtk.Justification.LEFT)
        self.directoryBox.pack_start(self.gameDirectoryLabel, True, True, 0)

        self.gameDirectorySelection = Gtk.Entry()
        self.directoryBox.pack_start(self.gameDirectorySelection, True, True, 0)

        self.gameDirectoryEntryButton = Gtk.Button(label='Set game directory')
        self.gameDirectoryEntryButton.connect("clicked", self.setGameDirectory)
        self.directoryBox.pack_start(self.gameDirectoryEntryButton, True, True, 0)

        self.installScriptButton = Gtk.Button(label='Download & install BepInEx')
        self.installScriptButton.connect("clicked", self.startInstall)
        self.modsBox.pack_start(self.installScriptButton, True, True, 0)

        self.installThread = threading.Thread(target=self.installBepInEx)
        self.installThread.daemon = True

        self.modsListLabel = Gtk.Label()
        self.modsListLabel.set_text("Mods List (TODO)")
        self.gameDirectoryLabel.set_justify(Gtk.Justification.LEFT)
        self.modsBox.pack_start(self.modsListLabel, True, True, 0)

    def setGameDirectory(self, widget):
        if os.path.isdir(self.gameDirectorySelection.get_text()):
            cfg['gameDirectoryString'] = self.gameDirectorySelection.get_text()
            config = open('cfg.json', 'w')
            json.dump(cfg, config)
            config.close()
        else:
            error = ErrorDialog(self, 'directoryNotFound')
            errorRun = error.run()
            error.destroy()
        
        self.gameDirectoryLabel.set_text(f"Full path to game directory: {cfg['gameDirectoryString']}")
        self.show_all()

    def startInstall(self, widget):
        self.installThread.start()

    def installBepInEx(self):
        # TODO: IMPLEMENT A PROGRESS BAR HERE
        if os.path.isfile(f"{cfg['gameDirectoryString']}Contract Rush DX.exe"): # If the file exists continue, otherwise spawn an error dialog and skip the rest.
                print("file exists test")
                result = requests.get("https://github.com/BepInEx/BepInEx/")

                soup = BeautifulSoup(result.content, 'html.parser')
                latestRelease = soup.find_all('span', class_='css-truncate css-truncate-target text-bold mr-2')
                if latestRelease:
                    for item in latestRelease:
                        # print(f"Latest release: {item.get_text()}")

                        # Now, use that to find the latest release of BepinEx and download it.
                        versionData_A = re.search(r"((?:[0-9]+\.)+[0-9]+)", item.get_text())
                        if versionData_A:

                            downloadURL = f"https://github.com/BepinEx/BepinEx/releases/download/{"v" + str(versionData_A.group(1))}/BepinEx_win_x64_{str(versionData_A.group(1))}.zip"
                            # print(f"Download URL: {downloadURL}")

                            # print("Downloading latest release. This might take a moment.")
                            download = requests.get(downloadURL, stream=True)

                            with open("bepinex_latest.zip", "wb") as bpxZip:
                                for chunk in download.iter_content(chunk_size=8192):
                                    if chunk:
                                        bpxZip.write(chunk)
                            
                            print("Download complete. File saved as bepinex_latest.zip.")

                            # TODO: move file and extract it

                            manualConfig = ManualDialog(self)
                            manualConfigRun = manualConfig.run()
                            manualConfig.destroy()

                        else:
                            # print("Error! Regex Fail.")
                            error = ErrorDialog(self, 'regexFailure')
                            errorRun = error.run()
                            error.destroy()
                            
                else:
                    # print("Error! Could not find github repo for BepinEx. Something is going horribly wrong.")
                    error = ErrorDialog(self, 'cannotFindBPXRepo')
                    errorRun = error.run()
                    error.destroy()
        else:
            error = ErrorDialog(self, 'executableNotFound')
            errorRun = error.run()
            error.destroy()

class ManualDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Manual Configuration Required", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(200, 100)
        self.errorLabel = Gtk.Label(label='todo')
        self.errorLabel.set_line_wrap(True)
        self.errorLabel.set_max_width_chars(64)
        self.errorBox = self.get_content_area()
        self.errorBox.add(self.errorLabel)
        self.show_all()
         
class InfoDialog(Gtk.Dialog):
    def __init__(self, parent, infoType):
        super().__init__(title="INFORMATION", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(200, 100)
        self.errorLabel = Gtk.Label(label=errorMessages[infoType])
        self.errorLabel.set_line_wrap(True)
        self.errorLabel.set_max_width_chars(64)
        self.errorBox = self.get_content_area()
        self.errorBox.add(self.errorLabel)
        self.show_all()

# Dialog for displaying errors to user. Pass it an error type from errorMessages dict and it will display it.
class ErrorDialog(Gtk.Dialog):
    def __init__(self, parent, errorType):
        super().__init__(title="ERROR", transient_for=parent, flags=0)
        self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(200, 100)
        self.errorLabel = Gtk.Label(label=errorMessages[errorType])
        self.errorLabel.set_line_wrap(True)
        self.errorLabel.set_max_width_chars(64)
        self.errorBox = self.get_content_area()
        self.errorBox.add(self.errorLabel)
        self.show_all()

window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()


# TODO list
# implement mod disable enable system and scanning mod folders every time a change is made, along with a manual rescan mods button
# implement system that checks if the game executable and bepinex exists when the game directory is set, and displays an error popup if it is not
# implement installer button that downloads and installs the installer script and then runs it, providing further instructions to user in the terminal