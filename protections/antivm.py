from vms.vmware import VMWareDetect
from vms.virtualbox import VirtualBoxDetect
from vms.kvm import KVMQEMUDetect


class AntiVM:
    def __init__(self):
        self.VMWare: bool = VMWareDetect()
        self.VirtualBox: bool = VirtualBoxDetect()
        self.KVMQemu: bool = KVMQEMUDetect()
