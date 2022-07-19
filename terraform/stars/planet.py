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
        '''Função que decrementa o atributo self.terraform de acordo com o valor setado na função self.set_damage()'''
        self.controle.acquire_nuke_mutex() # mutex que protege o decremento da variável self.terraform
        if self.terraform > 0: # só bombardeia se planeta ainda não está terraformado
            before_percentage = self.terraform
            if before_percentage < self.damage:
                self.terraform = 0
            else:
                self.terraform = before_percentage - self.damage
            print(
                f"[NUKE DETECTION] - The planet {self.name} was bombed. {self.terraform}% UNHABITABLE")

        self.controle.release_sem_damage() # libera para que outro foguete possa rodar "set_damage"
        self.controle.release_nuke_mutex()

    def print_planet_info(self):
        print(f"🪐 - [{self.name}] → {self.terraform}% UNINHABITABLE")

    def set_damage(self, damage):
        '''Função de que seta self.damage com o valor fornecido e "acorda" a run do planeta'''
        self.controle.acquire_sem_damage() 
        # semáforo que garante que apenas 1 foguete por vez altera os atributos do planeta
        self.damage = damage
        self.controle.release_nuke_sem()
        # libera o semáforo que faz self.run rodar

    def run(self):
        globals.acquire_print()
        self.print_planet_info()
        globals.release_print()
        self.damage = 0

        while(globals.get_release_system() == False):
            pass

        self.controle = globals.get_planet_controls(self.name)

        while(True):
            # Espera um bombardeio ser detectado
            self.controle.acquire_nuke_sem()
            self.nuke_detected()

            # Se foi terraformado com sucesso, thread do planeta é finalizada.
            if self.terraform == 0:
                break
