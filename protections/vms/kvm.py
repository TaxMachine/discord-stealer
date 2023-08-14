import re

from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE
from hardware.WmiQuery import Query
from typing import List

KVM = re.compile("linux|bsd|osx|qemu|seabios|bochs")
REGISTRY = OpenKey(HKEY_LOCAL_MACHINE, "SYSTEM\\HardwareConfig\\Current")


def KVMQEMUDetect() -> bool:
    checks: List[bool] = []
    bioshostdistro: List[str] = []
    biosmanufacturer: List[str] = []

    for x in Query("SELECT SMBIOSBIOSVersion, Manufacturer, PrimaryBIOS FROM Win32_BIOS WHERE PrimaryBIOS = 'True'"):
        bioshostdistro.append(x.SMBIOSBIOSVersion)
        biosmanufacturer.append(x.Manufacturer)

    physcomp: List[str] = [x.Manufacturer for x in Query("SELECT Manufacturer, DeviceLocator FROM CIM_PhysicalComponent WHERE DeviceLocator = 'DIMM 0'")]
    compsys: List[str] = [x.Manufacturer for x in Query("SELECT * FROM Win32_ComputerSystem")]

    for i in ["SystemManufacturer", "BIOSVendor", "SystemBiosVersion", "BIOSVersion"]:
        value, _ = QueryValueEx(REGISTRY, i)
        checks.append(len(KVM.findall(value)) > 0)

    for i in (bioshostdistro + biosmanufacturer + physcomp + compsys):
        checks.append(any(KVM.search(x.lower()) for x in i))

    return True in checks
