import threading
import globals
from threading import Thread, Lock
from space.rocket import Rocket
from random import choice
from time import sleep

'''O sincronismo de acesso das bases a essa reserva é tal que apenas uma base consegue acesso a mina de urânio e a reserva de petróleo por vez.'''

lock_mine_acess = Lock()  # global e usar em produce também? idk


class SpaceBase(Thread):

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, name, fuel, uranium, rockets):  # alteração no construtor autorizada
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
                if self.uranium > 35:
                    if self.name == 'ALCANTARA':
                        if self.fuel >= 70:
                            self.uranium = self.uranium - 35
                            self.fuel = self.fuel - 70
                            return True
                    elif self.name == 'MOON':
                        if self.fuel >= 50:
                            self.uranium = self.uranium - 35
                            self.fuel = self.fuel - 50
                            return True
                    else:
                        if self.fuel >= 100:
                            self.uranium = self.uranium - 35
                            self.fuel = self.fuel - 100
                            return True
                return False
            case 'FALCON':
                if self.uranium > 35:
                    if self.name == 'ALCANTARA':
                        if self.fuel >= 100:
                            self.uranium = self.uranium - 35
                            self.fuel = self.fuel - 100
                            return True
                    elif self.name == 'MOON':
                        if self.fuel >= 90:
                            self.uranium = self.uranium - 35
                            self.fuel = self.fuel - 90
                            return True
                    else:
                        if self.fuel >= 120:
                            self.uranium = self.uranium - 35
                            self.fuel = self.fuel - 120
                            return True
                return False
            case 'LION':
                # estarei contando launch + uso da carga máxima! avaliar se necessário
                if self.uranium > 75:
                    if self.name == 'ALCANTARA':
                        if self.fuel >= 220:
                            self.uranium = self.uranium - 75
                            self.fuel = self.fuel - 220
                            return True
                    else:
                        if self.fuel >= 235:
                            self.uranium = self.uranium - 75
                            self.fuel = self.fuel - 115
                            return True
                return False
            case _:
                print("Invalid rocket name")

    def refuel_oil(self):
        '''Se for base terrestre, adquire combustível a partir da mina de petroléo'''
        if self.name != 'MOON':
            lock_mine_acess.acquire()

            oil_mine = globals.get_mines_ref().get('oil_earth')
            if (oil_mine.unities < 100):
                sleep(0.05)

            filling = min(oil_mine.unities, (self.constraints[1] - self.fuel))
            oil_mine.unities -= filling  # CONDIÇÃO DE CORRIDA
            self.fuel += filling

            lock_mine_acess.release()
        else:
            '''Em uma viagem, o Lion consegue carregar com segurança 75 unidades de urânio e 120 unidades de combustível para a base lunar'''
            filling = min(120, (self.constraints[1] - self.fuel))
            self.fuel += filling

    def refuel_uranium(self):
        '''Se for base terrestre, adquire urânio a partir da mina de urânio'''
        if self.name != 'MOON':
            lock_mine_acess.acquire()

            uranium_mine = globals.get_mines_ref().get('uranium_earth')
            if (uranium_mine.unities < 35):
                sleep(0.05)

            filling = min(uranium_mine.unities,
                          (self.constraints[0] - self.uranium))
            uranium_mine.unities -= filling
            self.uranium += filling

            lock_mine_acess.release()
        else:
            # lua -> recebe através do foguete LION
            filling = min(75, (self.constraints[0] - self.uranium))
            self.uranium += filling

    def prepare_launch(self, rocket:Rocket, destino):
        if destino == 'MOON':
            r = Thread(target=lambda:rocket.launch_lion(self))
            r.start()
        else:
            r = Thread(target=lambda:rocket.launch(self, globals.get_planets_ref()[destino]), )
            r.start()
            

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        moon_controls = globals.get_moon_controls()
        while(globals.get_release_system() == False):
            pass

        while(True):

            # checa se lua precisa de recursos
            if self.name != 'MOON':
                moon_controls.acquire_bool_mutex()
                if moon_controls.calling:
                    if (self.base_rocket_resources('LION')):
                        # FALTA: checar questão da carga de lion.
                        # tiro suficiente pra carga em base_rockets
                        # não estou usando atributos de carga
                        moon_controls.calling = False
                        moon_controls.release_bool_mutex()
                        rocket = Rocket('LION')
                        #rocket.launch_lion(self)
                        self.prepare_launch(rocket, 'MOON')
                    else:
                        # SEM RECURSOS PARA CHAMAR LION
                        moon_controls.release_bool_mutex()
                        self.refuel_oil()
                        self.refuel_uranium()
                else:
                    moon_controls.release_bool_mutex()

            # lançamento para atirar (p.s: ter cuidado com a diretiva)
            # "um lançamento por vez"
            foguete = choice(['DRAGON', 'FALCON'])  # foguete aleatório
            # planeta aleatório
            planeta = choice(list(globals.get_planets_ref().keys()))
            control_planeta = globals.get_planet_controls(planeta)
            control_planeta.acquire_satelite()
            if globals.get_planets_ref()[planeta].terraform > 0:
                if (self.base_rocket_resources(foguete)):
                    rocket = Rocket(foguete)
                    #rocket.launch(self, globals.get_planets_ref()[planeta])
                    control_planeta.release_satelite()
                    self.prepare_launch(rocket, planeta)
                else:
                    # SEM RECURSOS
                    # dúvida: a função base_rocket_resources cobre todos os casos necessários
                    control_planeta.release_satelite()  # pra não dar deadlock
                    if self.name == 'MOON':
                        # CHAMA POR OUTRAS THREADS
                        moon_controls.acquire_bool_mutex()
                        moon_controls.calling = True
                        moon_controls.release_bool_mutex()
                        moon_controls.wait_sem()

                    self.refuel_oil()
                    self.refuel_uranium()
            else:
                control_planeta.release_satelite()
