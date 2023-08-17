from psutil import process_iter


def Processes():
    return process_iter()
