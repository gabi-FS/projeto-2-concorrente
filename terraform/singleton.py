from threading import Thread, Lock, Semaphore, Condition, BoundedSemaphore


class Singleton(type):

    __instancias = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instancias:
            instancia = super().__call__(*args, **kwargs)
            cls.__instancias[cls] = instancia
        return cls.__instancias[cls]


class PlanetControls(metaclass=Singleton):
    def __init__(self) -> None:
        self.satelite = Lock()
        self.nuke_mutex = Lock()
        self.polos = (Lock(), Lock())

    def acquire_nuke_mutex(self):
        self.nuke_mutex.acquire()

    def acquire_satelite(self):
        self.satelite.acquire()

    def acquire_mutex_polo(self, n: int):
        self.polos[n].acquire()

    def release_nuke_mutex(self):
        self.nuke_mutex.release()

    def release_satelite(self):
        self.satelite.release()

    def release_mutex_polo(self, n: int):
        self.polos[n].release()


class MoonControls(metaclass=Singleton):
    def __init__(self) -> None:
        self.__calling = False
        self.bool_mutex = Lock()
        self.waiting_sem = Semaphore(0)

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
        """Libera MOON para refuel, visto que LION chegou """
        self.waiting_sem.release()
