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

    def acquire_mutex_polo(self, n:int):
        self.polos[n].acquire()

    def release_nuke_mutex(self):
        self.nuke_mutex.release()

    def release_satelite(self):
        self.satelite.release()

    def release_mutex_polo(self, n:int):
        self.polos[n].release()