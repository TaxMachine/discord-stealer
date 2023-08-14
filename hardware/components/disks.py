from hardware.WmiQuery import Query
from typing import List


class Disk:
    def __init__(self, name: str, filesystem: str, freespace: float, size: float, volumename: str):
        self.Name: str = name
        self.FileSystem: str = filesystem
        self.FreeSpace: float = freespace
        self.Size: float = size
        self.VolumeName: str = volumename


def Disks() -> List[Disk]:
    disks: List[Disk] = []
    for disk in Query("SELECT Name, FileSystem, FreeSpace, Size, VolumeName FROM Win32_LogicalDisk WHERE DriveType = 3"):
        disks.append(Disk(
            disk.Name,
            disk.FileSystem,
            disk.FreeSpace,
            disk.Size,
            disk.VolumeName
        ))
    return disks
