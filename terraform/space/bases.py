import globals
from threading import Thread, Lock
from space.rocket import Rocket
from random import choice

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
                if self.uranium > 35 and self.fuel > 50:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 70
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 50
                    else:
                        self.fuel = self.fuel - 100
                    return True
                return False
            case 'FALCON':
                if self.uranium > 35 and self.fuel > 90:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    elif self.name == 'MOON':
                        self.fuel = self.fuel - 90
                    else:
                        self.fuel = self.fuel - 12
                    return True
                return False
            case 'LION':
                if self.uranium > 35 and self.fuel > 100:
                    self.uranium = self.uranium - 35
                    if self.name == 'ALCANTARA':
                        self.fuel = self.fuel - 100
                    else:
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
            while (oil_mine.unities < 100):
                # ESPERA OCUPADA POR ENQUANTO PRA ESPERAR PRODUÇÃO MINIMA NECESSÁRIA
                pass

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
            while (uranium_mine.unities < 35):
                # ESPERA OCUPADA POR ENQUANTO PRA ESPERAR PRODUÇÃO MINIMA NECESSÁRIA
                pass
            filling = min(uranium_mine.unities,
                          (self.constraints[0] - self.uranium))
            uranium_mine.unities -= filling
            self.uranium += filling

            lock_mine_acess.release()
        else:
            # lua -> recebe através do foguete LION
            filling = min(75, (self.constraints[0] - self.uranium))
            self.uranium += filling

    def run(self):
        globals.acquire_print()
        self.print_space_base_info()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        while(True):

            # checa se lua precisa de recursos
            if self.name != 'MOON':
                globals.get_lock_bool().acquire()
                if globals.get_moon_call() == True:
                    if (self.base_rocket_resources('LION')):
                        # não estou usando fuel cargo do foguete ainda, avaliar
                        rocket = Rocket('LION')
                        # dúvida se funções de foguete estão apropriadas para Lion Launch
                        # rocket.launch() -> fazer alternativa pra LION
                        # preferivel dentro de funções do foguete
                        # já que só ele tem certeza se launch teve sucesso
                        globals.set_moon_call(False)
                        globals.get_lock_moon().release()
                        globals.get_lock_bool().release()

                    else:
                        # SEM RECURSOS PARA CHAMAR LION
                        globals.get_lock_bool().release()
                        self.refuel_oil()
                        self.refuel_uranium()
                else:
                    globals.get_lock_bool().release()

            # lançameto para atirar
            foguete = choice(['DRAGON', 'FALCON'])  # foguete aleatório
            # planeta aleatório
            planeta = choice(list(globals.get_planets_ref().keys()))
            control_planeta = globals.get_planet_controls(planeta)
            control_planeta.acquire_satelite()
            if globals.get_planets_ref()[planeta].terraform > 0:
                if (self.base_rocket_resources(foguete)):
                    rocket = Rocket(foguete)
                    rocket.launch(self, globals.get_planets_ref()[planeta])
                    control_planeta.release_satelite()
                else:
                    # SEM RECURSOS
                    # dúvida: a função base_rocket_resources cobre todos os casos necessários
                    control_planeta.release_satelite()  # pra não dar deadlock
                    if self.name == 'MOON':
                        # CHAMA POR OUTRAS THREADS
                        globals.get_lock_bool().acquire()
                        globals.set_moon_call(True)
                        globals.get_lock_bool().release()
                        globals.get_lock_moon().acquire()  # espera lion chegar

                    self.refuel_oil()
                    self.refuel_uranium()
