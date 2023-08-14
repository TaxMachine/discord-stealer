import re

from winreg import OpenKey, QueryValueEx, HKEY_LOCAL_MACHINE
from hardware.WmiQuery import Query
from typing import List

VMW = re.compile("vmw|vmware")
REGISTRY = OpenKey(HKEY_LOCAL_MACHINE, "SYSTEM\\HardwareConfig\\Current")


def VMWareDetect() -> bool:
    checks: List[bool] = []
    biosversion = []
    biosmanufacturer = []
    for x in Query("SELECT SMBIOSBIOSVersion, Manufacturer FROM Win32_BIOS WHERE PrimaryBIOS = 'True'"):
        biosversion.append(x.SMBIOSBIOSVersion)
        biosmanufacturer.append(x.Manufacturer)
    diskdrive = [x.Model for x in Query("SELECT Model FROM Win32_DiskDrive WHERE Status = 'Ok'")]
    displayconfig = [x.DeviceName for x in Query("SELECT DeviceName FROM Win32_DisplayConfiguration")]
    compsys = [x.Vendor for x in Query("SELECT Vendor FROM Win32_ComputerSystemProduct")]
    physicmem = [x.Manufacturer for x in Query("SELECT Manufacturer FROM CIM_Chip")]

    for i in ["BIOSVendor", "BIOSVersion", "SystemManufacturer", "SystemProductName"]:
        value, _ = QueryValueEx(REGISTRY, i)
        checks.append(len(VMW.findall(value)) > 0)

    for i in (biosversion + biosmanufacturer + diskdrive + displayconfig + compsys + physicmem):
        checks.append(any(VMW.search(x.lower()) for x in i))

    return True in checks
