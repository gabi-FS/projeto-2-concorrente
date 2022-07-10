from threading import Lock
from singleton import PlanetControls

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
dados_planeta = {} # dicionário de mutexes (alguma ideia melhor?)
controles_planeta = {}


def acquire_print():
    global mutex_print
    mutex_print.acquire()

def release_print():
    global mutex_print
    mutex_print.release()

def set_planets_ref(all_planets):
    global planets
    planets = all_planets
    global dados_planeta # cria um dicionário de mutexes pra pegar os dados dos planetas
    for planet in all_planets.keys(): # (já que não pode mudar o construtor)
        #dados_planeta[planet] = Lock()planeta
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


def acquire_satelite(planeta):
    '''pega o lock para obter informações do planeta correspondente'''
    global dados_planeta
    dados_planeta[planeta].acquire()

def release_satelite(planeta):
    '''libera o lock para obter informações do planeta correspondente'''
    global dados_planeta
    dados_planeta[planeta].release()

def get_planet_controls(nome_planeta:str):
    return controles_planeta[nome_planeta.lower()]