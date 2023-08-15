from concurrent.futures import ThreadPoolExecutor

from hardware.components.cpu import CPU
from hardware.components.gpu import GPU, GPUDetails
from hardware.components.disks import Disks, Disk
from hardware.components.uuid import UUID
from hardware.components.motherboard import MOTHERBOARD, MotherBoard
from hardware.components.antiviruses import AntiViruses
from hardware.components.activationkey import ActivationKey

from typing import List, Dict, Callable


class Hardware:
    def __init__(self):
        self.results = {}
        self.ActivationKey = None
        self.AntiViruses = None
        self.MotherBoard = None
        self.UUID = None
        self.Disks = None
        self.GPU = None
        self.CPU = None
        self.SpawnHardwareThread()

    def SpawnHardwareThread(self):
        def run_function(func):
            res = func()
            self.results[func.__name__] = res

        with ThreadPoolExecutor() as executor:
            executor.submit(run_function, CPU)
            executor.submit(run_function, GPU)
            executor.submit(run_function, Disks)
            executor.submit(run_function, UUID)
            executor.submit(run_function, MOTHERBOARD)
            executor.submit(run_function, AntiViruses)
            executor.submit(run_function, ActivationKey)

        print(self.results)

        self.CPU = self.results["CPU"]
        self.GPU = self.results["GPU"]
        self.Disks = self.results["Disks"]
        self.UUID = self.results["UUID"]
        self.MotherBoard = self.results["MOTHERBOARD"]
        self.AntiViruses = self.results["AntiViruses"]
        self.ActivationKey = self.results["ActivationKey"]
