from threading import Thread
import globals
from controls import PlanetControls


class Planet(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, terraform, name):
        Thread.__init__(self)
        self.terraform = terraform
        self.name = name

    def nuke_detected(self):
        self.controle.acquire_nuke_mutex()
        if self.terraform > 0:
            before_percentage = self.terraform
            if before_percentage < self.damage:
                self.terraform = 0
            else:
                self.terraform = before_percentage - self.damage
            print(
                f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")

        self.controle.release_sem_damage()
        self.controle.release_nuke_mutex()

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def set_damage(self, damage):
        self.controle.acquire_sem_damage()
        self.damage = damage

    def run(self):
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()
        self.damage = 0

        while(globals.get_release_system() == False):
            pass

        self.controle = globals.get_planet_controls(self.name)

        while(True):
            self.controle.acquire_nuke_sem()
            self.nuke_detected()

            if self.terraform == 0:
                break
