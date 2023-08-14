from hardware.WmiQuery import Query


def UUID() -> str:
    return Query("SELECT UUID FROM Win32_ComputerSystemProduct")[0].UUID
