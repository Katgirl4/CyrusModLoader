import json, gi, sys, os, subprocess, re, requests

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
    "directoryNotFound":"That directory does not exist! Please input a valid directory. Maybe you forgot an ending \"/\" or a capitalization?"
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
        self.installScriptButton.connect("clicked", self.installBepInEx)
        self.modsBox.pack_start(self.installScriptButton, True, True, 0)

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

    def installBepInEx(self, widget):
        install = False
        while install is False: # need this here so break can happen if an error occurs before the dialog should be created

            # Error Checks. Each one will have an if true for development that can be removed later.

            if os.path.isfile(f"{cfg['gameDirectoryString']}Contract Rush DX.exe"): # If the file exists continue, otherwise spawn an error dialog and skip the rest.
                print("file exists test")
            else:
                error = ErrorDialog(self, 'executableNotFound')
                errorRun = error.run()
                error.destroy()
                break # Skip the install and the function ends






            installerDialog = InstallerDialog(self)
            runner = installerDialog.run()
            installerDialog.destroy()
            install = True

class InstallerDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="BepInEx Semi-Automated Installer", transient_for=parent, flags=0)
        # self.add_buttons(Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)
        self.inlabel = Gtk.Label(label="todo")
        self.inbox = self.get_content_area()
        self.inbox.add(self.inlabel)
        self.show_all()
        self.install(self)

    def install(self):
        print("THIS IS A PLACEHOLDER TEST")


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