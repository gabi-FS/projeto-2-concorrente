from random import randrange, random
from time import sleep
import globals
from stars.planet import Planet
from threading import Thread


class Rocket:

    ################################################
    # O CONSTRUTOR DA CLASSE NÃO PODE SER ALTERADO #
    ################################################
    def __init__(self, type):
        self.id = randrange(1000)
        self.name = type
        if(self.name == 'LION'):
            self.fuel_cargo = 0
            self.uranium_cargo = 0

    def nuke(self, planet: Planet):  # Permitida a alteração
        ''' Escolhe aleatóriamente um polo do planeta para bombardear e avisa o planeta do bombardeio (com seu dano causado)'''

        if planet.terraform == 0:
            return

        controle = globals.get_planet_controls(planet.name)
        polo = randrange(0, 2)
        controle.acquire_mutex_polo(polo)
        if polo == 0:
            print(
                f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on North Pole")
        else:
            print(
                f"[EXPLOSION] - The {self.name} ROCKET reached the planet {planet.name} on South Pole")
        planet.set_damage(self.damage())
        controle.release_nuke_sem()
        controle.release_mutex_polo(polo)

    def voyage_thread(self, planet: Planet):
        ''' Foguetes simulam tempo de viagem e testam para possíveis falhas

        Foguete explosivo: Bombardeia o planeta

        Foguete de carga: entrega cargas para a base lunar usar seu método de abastecimento
        '''
        if self.name != 'LION':
            self.simulation_time_voyage(planet)
            failure = self.do_we_have_a_problem()
            if (not failure):
                self.nuke(planet)  # só chega ao planeta se não houve falha
        else:
            moon_controls = globals.get_moon_controls()
            sleep(0.011)  # 4 dias -> simulation time voyage
            failure = self.do_we_have_a_problem()
            if (not failure):
                # chegou à base lunar
                moon_base = globals.get_bases_ref()['moon']
                moon_base.refuel_uranium(self.uranium_cargo)
                moon_base.refuel_oil(self.fuel_cargo)
                moon_controls.post_sem()
            else:
                # não deu certo. avisar que lua continua precisando de recursos
                moon_controls.acquire_bool_mutex()
                moon_controls.calling = True
                moon_controls.release_bool_mutex()

    def voyage(self, planet: Planet):  # Permitida a alteração (com ressalvas)
        # Chamadas de funções movidas para voyage_thread
        '''Inicia thread de viagem do foguete'''
        r = Thread(target=lambda: self.voyage_thread(planet))
        r.daemon = True
        r.start()

    def launch_lion(self, base):
        ''' Lança LION para a lua, caso não tenha sucesso, lua continua pedindo por recursos. '''

        moon_controls = globals.get_moon_controls()
        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")
            self.voyage(None)
        else:
            # não deu certo. avisar que lua continua precisando de recursos
            moon_controls.acquire_bool_mutex()
            moon_controls.calling = True
            moon_controls.release_bool_mutex()

    ####################################################
    #                   ATENÇÃO                        #
    #     AS FUNÇÕES ABAIXO NÃO PODEM SER ALTERADAS    #
    ###################################################

    def simulation_time_voyage(self, planet):
        if planet.name == 'MARS':
            # Marte tem uma distância aproximada de dois anos do planeta Terra.
            sleep(2)
        else:
            # IO, Europa e Ganimedes tem uma distância aproximada de cinco anos do planeta Terra.
            sleep(5)

    def do_we_have_a_problem(self):
        if(random() < 0.15):
            if(random() < 0.51):
                self.general_failure()
                return True
            else:
                self.meteor_collision()
                return True
        return False

    def general_failure(self):
        print(f"[GENERAL FAILURE] - {self.name} ROCKET id: {self.id}")

    def meteor_collision(self):
        print(f"[METEOR COLLISION] - {self.name} ROCKET id: {self.id}")

    def successfull_launch(self, base):
        if random() <= 0.1:
            print(
                f"[LAUNCH FAILED] - {self.name} ROCKET id:{self.id} on {base.name}")
            return False
        return True

    def damage(self):
        return random()

    def launch(self, base, planet):
        if(self.successfull_launch(base)):
            print(f"[{self.name} - {self.id}] launched.")
            self.voyage(planet)
