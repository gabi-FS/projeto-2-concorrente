from threading import Lock
from controls import PlanetControls, MoonControls, Observer
from space.bases import SpaceBase

#  A total alteração deste arquivo é permitida.
#  Lembre-se de que algumas variáveis globais são setadas no arquivo simulation.py
#  Portanto, ao alterá-las aqui, tenha cuidado de não modificá-las.
#  Você pode criar variáveis globais no código fora deste arquivo, contudo, agrupá-las em
#  um arquivo como este é considerado uma boa prática de programação. Frameworks como o Redux,
#  muito utilizado em frontend em libraries como o React, utilizam a filosofia de um store
#  global de estados da aplicação e está presente em sistemas robustos pelo mundo.

release_system = False
mutex_print = Lock()
planets = {}
bases = {}
mines = {}
simulation_time = None
controles_planeta = {}  # dicionário de objetos PlanetControls
moon_controls = MoonControls()
oil_unities_lock = Lock()
uranium_unities_lock = Lock()
finish_system = False
observer = Observer()


def acquire_print():
    global mutex_print
    mutex_print.acquire()


def release_print():
    global mutex_print
    mutex_print.release()


def set_planets_ref(all_planets):
    global planets
    planets = all_planets
    for planet in all_planets.keys():  # cria um dicionário de objetos de controle dos planetas
        controles_planeta[planet] = PlanetControls()
    observer.start()


def get_planets_ref():
    global planets
    return planets


def set_bases_ref(all_bases):
    global bases
    bases = all_bases


def get_bases_ref() -> dict[str, SpaceBase]:
    global bases
    return bases


def set_mines_ref(all_mines: dict):
    global mines
    mines = all_mines


def get_mines_ref():
    global mines
    return mines


def set_release_system():
    global release_system
    release_system = True


def get_release_system():
    global release_system
    return release_system


def set_simulation_time(time):
    global simulation_time
    simulation_time = time


def get_simulation_time():
    global simulation_time
    return simulation_time


def get_planet_controls(nome_planeta: str) -> PlanetControls:
    '''Retorna um objeto de controle referente ao planeta informado'''
    return controles_planeta[nome_planeta.lower()]


def get_moon_controls() -> MoonControls:
    '''Adquire a classe de controle da base lunar'''
    global moon_controls
    return moon_controls


def acquire_oil_unities():
    '''Acquire no lock que protege unities da mina Pipeline'''
    global oil_unities_lock
    oil_unities_lock.acquire()


def release_oil_unities():
    '''Release no lock que protege unities da mina Pipeline'''
    global oil_unities_lock
    oil_unities_lock.release()


def acquire_uranium_unities():
    '''Acquire no lock que protege unities da mina StoreHouse'''
    global uranium_unities_lock
    uranium_unities_lock.acquire()


def release_uranium_unities():
    '''Release no lock que protege unities da mina StoreHouse'''
    global uranium_unities_lock
    uranium_unities_lock.release()


def get_finish_system():
    ''' Adquire variável de finalização do sistema '''
    global finish_system
    return finish_system


def set_finish_system():
    ''' Deixa em TRUE variável de finalização do sistema '''
    global finish_system
    finish_system = True
