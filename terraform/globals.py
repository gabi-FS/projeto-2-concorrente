from threading import Lock, Semaphore
from controls import PlanetControls, MoonControls

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


def acquire_print():
    global mutex_print
    mutex_print.acquire()


def release_print():
    global mutex_print
    mutex_print.release()


def set_planets_ref(all_planets):
    global planets
    planets = all_planets
    global dados_planeta  # cria um dicionário de mutexes pra pegar os dados dos planetas
    for planet in all_planets.keys():  # (já que não pode mudar o construtor)
        controles_planeta[planet] = PlanetControls()


def get_planets_ref():
    global planets
    return planets


def set_bases_ref(all_bases):
    global bases
    bases = all_bases


def get_bases_ref():
    global bases
    return bases


def set_mines_ref(all_mines):
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


def get_planet_controls(nome_planeta: str):
    '''Retorna um objeto referente ao planeta informado, de uma classe cujos 
    atributos são ferramentas de controle'''
    return controles_planeta[nome_planeta.lower()]


def get_moon_controls():
    global moon_controls
    return moon_controls
