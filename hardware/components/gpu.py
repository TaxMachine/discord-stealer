from hardware.WmiQuery import Query
from typing import List


class GPUDetails:
    def __init__(self, Name: str, VideoProcessor: str, AdapterRAM: int):
        self.Name: str = Name
        self.VideoProcessor: str = VideoProcessor
        self.AdapterRAM: int = AdapterRAM


def GPU() -> List[GPUDetails]:
    gpus: List[GPUDetails] = []
    for gpu in Query("SELECT Name, VideoProcessor, AdapterRAM FROM Win32_VideoController"):
        gpus.append(GPUDetails(gpu.Name, gpu.VideoProcessor, gpu.AdapterRAM))
    return gpus