from hardware.components.cpu import CPU
from hardware.components.gpu import GPU, GPUDetails
from hardware.components.disks import Disks, Disk
from hardware.components.uuid import UUID
from hardware.components.motherboard import MOTHERBOARD, MotherBoard
from hardware.components.antiviruses import AntiViruses
from hardware.components.activationkey import ActivationKey

from typing import List


class Hardware:
    def __init__(self):
        self.CPU: str = CPU()
        self.GPU: List[GPUDetails] = GPU()
        self.Disks: List[Disk] = Disks()
        self.UUID: str = UUID()
        self.MotherBoard: MotherBoard = MOTHERBOARD()
        self.AntiViruses: List[str] = AntiViruses()
        self.ActivationKey: str = ActivationKey()

