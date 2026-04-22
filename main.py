import pygame
import pygame_gui
import threading
import os, sys
from importlib import import_module

global nil
nil = None

class Game:
    def __init__(self):
        self.DeltaTime = 0,
        self.Running = True,
        self.CurrentlyChanging = False,

        self.Settings = {
            "Width" : 1900,
            "Height" : 1200,
        }

        self.Background = None

        self.Threads = {}
        self.Screen = None
        self.UIManager = None
        self.RunService = {}

class Player:
    def __init__(self):
        self.Username = None
        self.DisplayName = None

        self.Coins = 0
        self.UIs = None
        self.Mouse = pygame.mouse

class UI:
    def __init__(self):
        self.Texts = {}
        self.UIs = {}

LocalGame = Game()
player = Player()
player.UIs = UI()

string = str


global Modules
Modules = None

def import_via_syspath(module_path: str):
    module_dir = os.path.dirname(module_path)
    module_name = os.path.splitext(os.path.basename(module_path))[0]

    sys.path.append(module_dir)
    try:
        return import_module(module_name)
    finally:
        sys.path.pop()

def init():
    class ModulesClass:
        def __init__(self):
            self.ui = {}

            for filename in os.listdir("modules/ui"):
                file_path = os.path.join("modules/ui", filename)

                if os.path.isfile(file_path):
                    self.ui[filename] = import_via_syspath(file_path)

                    if hasattr(self.ui[filename], "moon_start"):
                        self.ui[filename].moon_start()


    global Modules
    Modules = ModulesClass()

    LocalGame.UIManager.add_font_paths('conflict3040', "data/Conflict 3040.otf")
    LocalGame.UIManager.preload_fonts([{'name': 'conflict3040', 'point_size': 18, 'style': 'regular'},
                                       ])
    
def updateRunService():
    for Name, Item in LocalGame.RunService.items():
        if callable(Item["Function"]):
            if "Arguments" in Item:
                Thread = threading.Thread(Item["Function"], args=Item["Arguments"])
                Thread.start()
            else:
                Thread = threading.Thread(Item["Function"])
                Thread.start()


Listeners = []

def listenforevent(event_type, item, function):
    Listeners.append({'Item' : item, 'Type' : event_type, 'Function': function})

def disconnectlistenforevent(item):
    if not item in Listeners: return

    print(item, "Removed")

    Listeners.remove(item)

def manageevents(DeltaTime : float):
    for event in pygame.event.get():
            LocalGame.UIManager.process_events(event)

            if event.type == pygame.QUIT:
                LocalGame.Running = False

            for Data in Listeners:
                if event.type == Data["Type"] and Data["Item"] == event.ui_element:
                    Data["Function"]()



def closeallUI():
    for item, module in Modules.ui.items():
        if hasattr(module, "closeUI"):
            module.closeUI()
