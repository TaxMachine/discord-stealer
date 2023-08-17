from hardware.components.cpu import CPU
from hardware.components.gpu import GPU, GPUDetails
from hardware.components.disks import Disks, Disk
from hardware.components.uuid import UUID
from hardware.components.motherboard import MOTHERBOARD, MotherBoard
from hardware.components.antiviruses import AntiViruses
from hardware.components.activationkey import ActivationKey
from hardware.components.PublicIP import PublicIP
from hardware.components.LocalIP import LocalIP
from hardware.components.MACAddress import MACAddress

from typing import List


class Hardware:
    def __init__(self):
        self.ActivationKey = ActivationKey()
        self.AntiViruses = AntiViruses()
        self.MotherBoard: MotherBoard = MOTHERBOARD()
        self.UUID = UUID()
        self.Disks: List[Disk] = Disks()
        self.GPU: List[GPUDetails] = GPU()
        self.CPU = CPU()
        self.PublicIP = PublicIP()
        self.PrivateIP = LocalIP()
        self.MAC = MACAddress()
