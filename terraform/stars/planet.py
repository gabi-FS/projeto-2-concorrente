from threading import Thread
import globals
from singleton import PlanetControls

class Planet(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform,name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    def nuke_detected(self, damage):
        # while(self.terraform > 0):
        #while(before_percentage == self.terraform):
        #pass
        controle = globals.get_planet_controls(self.name)
        controle.acquire_nuke_mutex()
        if self.terraform > 0:
            before_percentage = self.terraform 
            self.terraform = before_percentage - damage
        print(f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")
        controle.release_nuke_mutex()

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def run(self):
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        #while(True):
            #self.nuke_detected()