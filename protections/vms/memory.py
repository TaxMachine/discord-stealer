from hardware.WmiQuery import Query


def MemoryCheck() -> bool:
    return len(Query("SELECT Name FROM Win32_CacheMemory")) < 0
