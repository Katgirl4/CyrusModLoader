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

        outerBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
    
        directoryBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        directoryBox.set_homogeneous(False)

        modsBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        modsBox.set_homogeneous(False)
        
        outerBox.pack_start(directoryBox, True, True, 0)
        outerBox.pack_start(modsBox, True, True, 0)

        gameDirectoryLabel = Gtk.Label()
        gameDirectoryLabel.set_text(f"Game directory: {cfg['gameDirectoryString']}")
        gameDirectoryLabel.set_justify(Gtk.Justification.LEFT)
        directoryBox.pack_start(gameDirectoryLabel, True, True, 0)

        gameDirectorySelection = Gtk.Entry()
        directoryBox.pack_start(gameDirectorySelection, True, True, 0)

        gameDirectoryEntryButton = Gtk.Button(label='Button')
        gameDirectoryEntryButton.connect("clicked", lambda widget: self.setGameDirectory(gameDirectorySelection.get_text()))
        directoryBox.pack_start(gameDirectoryEntryButton, True, True, 0)
        
        modsListLabel = Gtk.Label()
        modsListLabel.set_text("Mods List (TODO)")
        gameDirectoryLabel.set_justify(Gtk.Justification.LEFT)
        modsBox.pack_start(modsListLabel, True, True, 0)

        self.add(outerBox)
    
    def setGameDirectory(self, widget):
        cfg['gameDirectoryString'] = widget
        config = open('cfg.json', 'w')
        json.dump(cfg, config)
        config.close()
    
    
    







window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()