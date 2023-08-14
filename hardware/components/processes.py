from multiprocessing import active_children


def Processes():
    return active_children()
