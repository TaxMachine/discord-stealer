import os
import glob
from os.path import join, isfile, sep
from typing import Dict

MAX_DEPTH = 3


def GetAppDataPaths(env):
    datapaths = []
    envloc = os.getenv(env)

    pattern = join(envloc, "**", "Local State")

    for files in glob.glob(pattern, recursive=True):
        datapaths.append(sep.join(files.split(sep)[:-1]))

    return datapaths


def json_to_obj(data: Dict, class_type):
    obj = class_type()
    for k, v in data.items():
        obj.__setattr__(k, v)
    return obj
