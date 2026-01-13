import json, gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MainWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="CyrusModManager")
        self.set_default_size(400, 300)
        
        button = Gtk.Button(label="Test")
        button.connect("clicked", self.onTest)
        self.add(button)

    def onTest(self, widget):
        print("Test")





# Open config file when application starts.
    # If config is found, open it. If config is not found, then create a new file and try to open it. (TODO: make it fill blank fields)
config = None
while not config:
    try:
        config = open("cfg.json", "r")
    except(FileNotFoundError):
        config = open('cfg.json', 'w')

window = MainWindow()
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()