from hardware.WmiQuery import Security

from typing import List


def AntiViruses() -> List[str]:
    avs: List[str] = []
    for av in Security("SELECT displayName FROM AntiVirusProduct"):
        avs.append(av.displayName)
    return avs
