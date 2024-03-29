from threading import Thread
from random import randint
from time import sleep

import globals


######################################################################
#                                                                    #
#              Não é permitida a alteração deste arquivo!            #
#                                                                    #
######################################################################

class StoreHouse(Thread):

    def __init__(self, unities, location, constraint):
        Thread.__init__(self)
        self.unities = unities
        self.location = location
        self.constraint = constraint

    def print_store_house(self):
        print(
            f"🔨 - [{self.location}] - {self.unities} uranium unities are produced.")

    def produce(self):
        if(self.unities < self.constraint):
            globals.acquire_uranium_unities()  # alteração permitida
            self.unities += 15
            globals.release_uranium_unities()

            self.print_store_house()
        sleep(0.001)

    def run(self):
        globals.acquire_print()
        self.print_store_house()
        globals.release_print()

        while(globals.get_release_system() == False):
            pass

        # alteração de while true para isso pois não consigo setar como daemo
        while(globals.get_finish_system() == False):
            self.produce()
