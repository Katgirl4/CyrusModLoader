import json, gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Open config file when application starts.
    # If config is found, open it. If config is not found, then create a new file and try to open it. (TODO: make it fill blank fields)
config = None
boilerplateJSON = {
    "gameDirectory": "./",
    "disableDirectory" : "./Disabled"
    }
while not config:
    try:
        config = open("cfg.json", 'r')
        try:
            cfg = json.load(config)
        except(json.JSONDecodeError):
            config.close()
            config = open('cfg.json', 'w')
            json.dump({"None" : "None"}, config)
            config.close()
            config = open("cfg.json", 'r')
            cfg = json.load(config)
    except(FileNotFoundError):
        config = open('cfg.json', 'w')
        json.dump({"None" : "None"}, config)
        config.close()

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
        gameDirectoryLabel.set_text("Game Directory Configuration")
        gameDirectoryLabel.set_justify(Gtk.Justification.LEFT)
        directoryBox.pack_start(gameDirectoryLabel, True, True, 0)

        gameDirectorySelection = Gtk.FileChooserButton()
        gameDirectorySelection.set_homogeneous(False)
        modsBox.pack_start(gameDirectorySelection, True, True, 0)

        modsListLabel = Gtk.Label()
        modsListLabel.set_text("Mods List (TODO)")
        gameDirectoryLabel.set_justify(Gtk.Justification.LEFT)
        modsBox.pack_start(modsListLabel, True, True, 0)

        self.add(outerBox)
        

    def onTest(self, widget):
        print("Test")







window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()