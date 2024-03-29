from threading import Thread, Lock, Semaphore, Condition, BoundedSemaphore
import globals


class Singleton(type):

    __instancias = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instancias:
            instancia = super().__call__(*args, **kwargs)
            cls.__instancias[cls] = instancia
        return cls.__instancias[cls]


class PlanetControls():
    '''Classe cujos atributos são ferramentas de controle referentes a um planeta'''
    def __init__(self) -> None:
        self.satelite = Lock()
        self.nuke_mutex = Lock()
        self.nuke_sem = Semaphore(0)
        self.sem_damage = Semaphore(1)
        self.polos = (Lock(), Lock())

    def acquire_nuke_mutex(self):
        self.nuke_mutex.acquire()

    def acquire_nuke_sem(self):
        self.nuke_sem.acquire()

    def acquire_sem_damage(self):
        '''Semáforo que permite ao foguete setar o damage no Planet'''
        self.sem_damage.acquire()

    def acquire_satelite(self):
        '''Acquire satélite do planeta para obter dados'''
        self.satelite.acquire()

    def acquire_mutex_polo(self, n: int):
        '''Acquire mutex que protege o polo desejado'''
        self.polos[n].acquire()

    def release_nuke_mutex(self):
        self.nuke_mutex.release()

    def release_nuke_sem(self):
        self.nuke_sem.release()

    def release_sem_damage(self):
        '''Libera para que outro foguete sete o damage no Planet'''
        self.sem_damage.release()

    def release_satelite(self):
        '''Release satélite do planeta para obter dados'''
        self.satelite.release()

    def release_mutex_polo(self, n: int):
        '''Release mutex que protege o polo desejado'''
        self.polos[n].release()


class MoonControls(metaclass=Singleton):
    '''Classe Singleton que possui informações sobre a neecessidade de recursos pra base lunar, tal qual mutexes e semáforos envolvidos. '''

    def __init__(self) -> None:
        self.__calling = False
        self.bool_mutex = Lock()
        self.waiting_sem = Semaphore(0)
        self.filling_fuel = 0
        self.filling_uranium = 0

    @property
    def calling(self):
        return self.__calling

    @calling.setter
    def calling(self, new_bool: bool):
        self.__calling = new_bool

    def acquire_bool_mutex(self):
        self.bool_mutex.acquire()

    def release_bool_mutex(self):
        self.bool_mutex.release()

    def wait_sem(self):
        """MOON espera Lion chegar"""
        self.waiting_sem.acquire()

    def post_sem(self):
        """Libera MOON para continuar seu funcionamento após refuels"""
        self.waiting_sem.release()


class Observer(Thread):
    '''Thread que espera join das threads de planetas para enfim avisar o resto do programa para finalizar '''

    def __init__(self):
        Thread.__init__(self, name='observer')

    def run(self):
        planetas = globals.get_planets_ref()
        for planeta in planetas.values():
            planeta.join()

        # todos planetas finalizaram
        globals.set_finish_system()
        globals.moon_controls.post_sem()  # libera lua terminar
        print(
            f'###### Simulation ended with {globals.get_simulation_time().current_time} years total ######')
