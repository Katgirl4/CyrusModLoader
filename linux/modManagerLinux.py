import json, gi, sys, os, subprocess

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

config = None
cfg = {}
while not cfg:
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
        self.gameDirectoryLabel.set_text(f"Game directory: {cfg['gameDirectoryString']}")
        self.gameDirectoryLabel.set_justify(Gtk.Justification.LEFT)
        self.directoryBox.pack_start(self.gameDirectoryLabel, True, True, 0)

        self.gameDirectorySelection = Gtk.Entry()
        self.directoryBox.pack_start(self.gameDirectorySelection, True, True, 0)

        self.gameDirectoryEntryButton = Gtk.Button(label='Set Game directory')
        self.gameDirectoryEntryButton.connect("clicked", self.setGameDirectory)
        self.directoryBox.pack_start(self.gameDirectoryEntryButton, True, True, 0)

        self.installScriptButton = Gtk.Button(label='Download & Install BepInEx')
        self.installScriptButton.connect("clicked", self.installBepInEx)
        self.modsBox.pack_start(self.installScriptButton, True, True, 0)

        self.modsListLabel = Gtk.Label()
        self.modsListLabel.set_text("Mods List (TODO)")
        self.gameDirectoryLabel.set_justify(Gtk.Justification.LEFT)
        self.modsBox.pack_start(self.modsListLabel, True, True, 0)

    def setGameDirectory(self, widget):
        cfg['gameDirectoryString'] = self.gameDirectorySelection.get_text()
        config = open('cfg.json', 'w')
        json.dump(cfg, config)
        config.close()
        
        self.gameDirectoryLabel.set_text(f"Game directory: {cfg['gameDirectoryString']}")
        self.show_all()

    def installBepInEx(self, widget):
        installerDialog = InstallerDialog(self)
        runner = installerDialog.run()
        if runner is Gtk.ResponseType.OK:
            print("ok")
        elif runner is Gtk.ResponseType.CANCEL:
            print("cancel")
        installerDialog.destroy()

class InstallerDialog(Gtk.Dialog):
     def __init__(self, parent):
        super().__init__(title="BepInEx Semi-Automated Installer", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(150, 100)
        self.inlabel = Gtk.Label(label="todo")
        self.inbox = self.get_content_area()
        self.inbox.add(self.inlabel)
        self.show_all()




window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()


# TODO list
# implement mod disable enable system and scanning mod folders every time a change is made, along with a manual rescan mods button
# implement system that checks if the game executable and bepinex exists when the game directory is set, and displays an error popup if it is not
# implement installer button that downloads and installs the installer script and then runs it, providing further instructions to user in the terminal