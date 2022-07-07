import globals
from threading import Thread, Lock
from space.rocket import Rocket
from random import choice

'''O sincronismo de acesso das bases a essa reserva é tal que apenas uma base consegue acesso a mina de urânio e a reserva de petróleo por vez.'''
# duvida se é um lock pras duas ou um pra cada
lock_oil = Lock()
lock_uranium = Lock()


class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, fuel, uranium, rockets): # alteração no construtor autorizada
        Thread.__init__(self)
        self.name = name
        self.uranium = 0
        self.fuel = 0
        self.rockets = 0
        self.constraints = [uranium, fuel, rockets]

    def print_space_base_info(self):
        print(f"🔭 - [{self.name}] → 🪨  {self.uranium}/{self.constraints[0]} URANIUM  ⛽ {self.fuel}/{self.constraints[1]}  🚀 {self.rockets}/{self.constraints[2]}")

    def base_rocket_resources(self, rocket_name):
        match rocket_name:
            case 'DRAGON':
                if self.uranium > 35 and self.fuel > 50:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 70
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 50
                    else:
                        self.fuel = self.fuel - 100
            case 'FALCON':
                if self.uranium > 35 and self.fuel > 90:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 90
                    else:
                        self.fuel = self.fuel - 120
            case 'LION':
                if self.uranium > 35 and self.fuel > 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    else:
                        self.fuel = self.fuel - 115
            case _:
                print("Invalid rocket name")

    def refuel_oil(self):
        '''Se for base terrestre, adquire combustível a partir da mina de petroléo'''
        if self.name != 'MOON':
            lock_oil.acquire()
            oil_mine = globals.get_mines_ref().get('oil_earth')
            # não chequei se não tem essa quant -> ou se devo add o máximo
            oil_mine.unities -= self.constraints[1]
            self.fuel = self.constraints[1]
            lock_oil.release()
        else:
            # lua -> recebe através do foguete
            # avaliar se espera por ele, mas aqui já adiciono quantidades
            '''Em uma viagem, o Lion consegue carregar com segurança 75 unidades de urânio e 120 unidades de combustível para a base lunar'''
            if 120 > self.constraints[1]:
                self.fuel = self.constraints[1]
            else:
                self.fuel = 120

    def refuel_uranium(self):
        '''Se for base terrestre, adquire urânio a partir da mina de urânio'''
        if self.name != 'MOON':
            lock_uranium.acquire()
            uranium_mine = globals.get_mines_ref().get('uranium_earth')
            # não chequei se não tem essa quant na mina -> ou se devo add o máximo
            uranium_mine.unities -= self.constraints[0]
            self.uranium = self.constraints[0]
            lock_uranium.release()
        else:
            # lua -> recebe através do foguete LION
            if 75 > self.constraints[0]:
                self.fuel = self.constraints[0]
            else:
                self.uranium = 75
                # p.s: estou substituindo valores considerando que chamo as funções quando chega a 0,, por isso não somo as unidades

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):
            foguete = choice(['DRAGON', 'FALCON'])  # foguete aleatório
            # planeta aleatório
            planeta = choice(list(globals.get_planets_ref().keys()))
            globals.acquire_satelite(planeta)
            if globals.get_planets_ref()[planeta].terraform > 0:
                # to do: verificar se tem combustível e urânio
                self.base_rocket_resources(foguete)
                rocket = Rocket(foguete)
                rocket.launch(self, planeta)
            globals.release_satelite(planeta)  # talvez mover p/ cima
            pass
