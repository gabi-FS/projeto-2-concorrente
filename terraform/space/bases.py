import threading
import globals
from threading import Thread, Lock
from space.rocket import Rocket
from random import choice
from time import sleep

lock_mine_acess = Lock()


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

    def base_rocket_resources(self, rocket_name, uranium_cargo=75, fuel_cargo=120):
        '''Testa se a base possui o que é necessário para lançar o foguete. Parâmetros opcionais uranium_cargo e fuel_cargo para foguetes de carga.

        Caso sim, remove os recursos da base e retorna True. Caso não, retorna False.'''
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
                if self.uranium > uranium_cargo:
                    if self.name == 'ALCANTARA':
                        if self.fuel >= (100 + fuel_cargo):
                            self.uranium = self.uranium - uranium_cargo
                            self.fuel = self.fuel - (100 + fuel_cargo)
                            return True
                    else:
                        if self.fuel >= (115 + fuel_cargo):
                            self.uranium = self.uranium - uranium_cargo
                            self.fuel = self.fuel - (115 + fuel_cargo)
                            return True
                return False
            case _:
                print("Invalid rocket name")
                return False

    def refuel_oil(self, lion_cargo=0):
        '''Se for base terrestre, adquire combustível a partir da mina de petroléo.
        Se for base lunar, reabastece com carga entregue.'''
        if self.name != 'MOON':
            lock_mine_acess.acquire()

            oil_mine = globals.get_mines_ref().get('oil_earth')
            if (oil_mine.unities < 100):
                sleep(0.05)

            filling = min(oil_mine.unities, (self.constraints[1] - self.fuel))
            globals.acquire_oil_unities()
            oil_mine.unities -= filling
            globals.release_oil_unities()
            self.fuel += filling

            lock_mine_acess.release()
        else:
            self.fuel += lion_cargo

    def refuel_uranium(self, lion_cargo=0):
        '''Se for base terrestre, adquire urânio a partir da mina de urânio.
        Se for base lunar, reabastece com carga entregue. '''
        if self.name != 'MOON':
            lock_mine_acess.acquire()

            uranium_mine = globals.get_mines_ref().get('uranium_earth')
            if (uranium_mine.unities < 35):
                sleep(0.05)

            filling = min(uranium_mine.unities,
                          (self.constraints[0] - self.uranium))
            globals.acquire_uranium_unities()
            uranium_mine.unities -= filling
            globals.release_uranium_unities()
            self.uranium += filling

            lock_mine_acess.release()
        else:
            self.uranium += lion_cargo

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        moon_controls = globals.get_moon_controls()
        while(globals.get_release_system() == False):
            pass

        while(globals.get_finish_system() == False):
            # checa se lua precisa de recursos
            if self.name != 'MOON':
                moon_controls.acquire_bool_mutex()
                if moon_controls.calling:
                    # leio quantidade de carga necessária na classe de controle
                    fuel_cargo = moon_controls.filling_fuel
                    uranium_cargo = moon_controls.filling_uranium
                    if (self.base_rocket_resources('LION', uranium_cargo, fuel_cargo)):
                        moon_controls.calling = False
                        moon_controls.release_bool_mutex()
                        rocket = Rocket('LION')
                        self.rockets += 1
                        rocket.fuel_cargo = fuel_cargo
                        rocket.uranium_cargo = uranium_cargo
                        rocket.launch_lion(self)
                        self.rockets -= 1
                    else:
                        # SEM RECURSOS PARA CHAMAR LION
                        moon_controls.release_bool_mutex()
                        self.refuel_oil()
                        self.refuel_uranium()

                        # continue garante que ele não vai gastar o que tem pra lançar outro foguete depois disso
                        continue
                else:
                    moon_controls.release_bool_mutex()

            # lançamento para atirar: foguete e planeta aleatórios
            foguete = choice(['DRAGON', 'FALCON'])
            planeta = choice(list(globals.get_planets_ref().keys()))
            control_planeta = globals.get_planet_controls(planeta)

            # protege leitura de dados do planeta (garante que só 1 base pode ler por vez)
            control_planeta.acquire_satelite()
            if globals.get_planets_ref()[planeta].terraform > 0:
                if (self.base_rocket_resources(foguete)):
                    control_planeta.release_satelite()  
                    rocket = Rocket(foguete)
                    self.rockets += 1
                    rocket.launch(self, globals.get_planets_ref()[planeta])
                    self.rockets -= 1
                else:
                    # SEM RECURSOS
                    control_planeta.release_satelite()
                    if self.name == 'MOON':
                        # Escreve quantidade necessária na classe de controle
                        moon_controls.filling_fuel = min(
                            120, (self.constraints[1] - self.fuel))
                        moon_controls.filling_uranium = min(
                            75, (self.constraints[0] - self.uranium))

                        # CHAMA POR OUTRAS THREADS
                        moon_controls.acquire_bool_mutex()
                        moon_controls.calling = True
                        moon_controls.release_bool_mutex()

                        # Espera post vindo do foguete que chega à base
                        moon_controls.wait_sem()
                    else:
                        # Base terrestre: adquire das minas
                        self.refuel_oil()
                        self.refuel_uranium()
            else:
                control_planeta.release_satelite()
