import re

from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE
from hardware.WmiQuery import Query
from typing import List


VBOX = re.compile("oracle|virtual|innotek|vbox")
REGISTRY = OpenKey(HKEY_LOCAL_MACHINE, "SYSTEM\\HardwareConfig\\Current")


def VirtualBoxDetect() -> bool:
    checks: List[bool] = []
    biosversion: List[str] = []
    biosManufacturer: List[str] = []
    for x in Query("SELECT SMBIOSBIOSVersion, Manufacturer FROM Win32_BIOS WHERE PrimaryBIOS = 'True'"):
        biosversion.append(x.SMBIOSBIOSVersion)
        biosManufacturer.append(x.Manufacturer)
    cdrom: List[str] = [x.DeviceID for x in Query("SELECT DeviceID from Win32_CDROMDrive WHERE DriveIntegrity = 'True'")]
    csManufacturer: List[str] = []
    csFamily: List[str] = []
    csModel: List[str] = []
    for x in Query("SELECT Manufacturer, Model, SystemFamily FROM Win32_ComputerSystem WHERE Status = 'Ok'"):
        csManufacturer.append(x.Manufacturer)
        csFamily.append(x.SystemFamily)
        csModel.append(x.Model)
    diskdrive: List[str] = [x.Model for x in Query("SELECT Model FROM Win32_DiskDrive WHERE Status = 'Ok'")]

    for i in ["BaseBoardManufacturer", "BaseBoardProduct", "SystemFamily", "BIOSVendor", "SystemManufacturer", "SystemProductName"]:
        value, _ = QueryValueEx(REGISTRY, i)
        checks.append(len(VBOX.findall(value)) > 0)

    for i in (biosversion + biosManufacturer + csManufacturer + csModel + csFamily + diskdrive):
        checks.append(any(VBOX.search(x.lower()) for x in i))

    return True in checks
