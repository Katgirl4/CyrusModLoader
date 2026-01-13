import json, gi, sys, os

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

        self.outerBox = Gtk.HBox(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    
        self.directoryBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.directoryBox.set_homogeneous(False)

        modsBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        modsBox.set_homogeneous(False)

        self.add(self.outerBox)
        
        self.outerBox.pack_start(self.directoryBox, True, True, 0)
        self.outerBox.pack_start(modsBox, True, True, 0)

        self.gameDirectoryLabel = Gtk.Label()
        self.gameDirectoryLabel.set_text(f"Game directory: {cfg['gameDirectoryString']}")
        self.gameDirectoryLabel.set_justify(Gtk.Justification.LEFT)
        self.directoryBox.pack_start(self.gameDirectoryLabel, True, True, 0)

        self.gameDirectorySelection = Gtk.Entry()
        self.directoryBox.pack_start(self.gameDirectorySelection, True, True, 0)

        self.gameDirectoryEntryButton = Gtk.Button(label='Set Game directory')
        self.gameDirectoryEntryButton.connect("clicked", self.setGameDirectory)
        self.directoryBox.pack_start(self.gameDirectoryEntryButton, True, True, 0)
        
        
        modsListLabel = Gtk.Label()
        modsListLabel.set_text("Mods List (TODO)")
        self.gameDirectoryLabel.set_justify(Gtk.Justification.LEFT)
        modsBox.pack_start(modsListLabel, True, True, 0)

    
    def setGameDirectory(self, widget):
        cfg['gameDirectoryString'] = self.gameDirectorySelection.get_text()
        config = open('cfg.json', 'w')
        json.dump(cfg, config)
        config.close()
        
        self.gameDirectoryLabel.set_text(f"Game directory: {cfg['gameDirectoryString']}")
        self.show_all()

window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()