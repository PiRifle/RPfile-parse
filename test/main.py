from rpfile_parse import RPFileParser
from utils import parse_arguments
import argparse
from urllib import parse
import rich
from asyncio import wait
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from os.path import abspath
import os
import uuid
progress = Progress()

def download(url):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 524288
    progress_bar = progress.add_task(f"downloading {url}", total=total_size)
    with open(url.split("/")[-1], "wb") as file:
        for data in response.iter_content(block_size):
            progress.update(progress_bar, advance=len(data))
            file.write(data)
        progress.remove_task(progress_bar)
    return abspath(url.split("/")[-1])

def download_command(command):
    return {"path": download(command["url"]), **command}

def parallel_download_commands(links):
    with progress:
        with ThreadPoolExecutor(4) as executor:
            futures = [executor.submit(download_command, i) for i in links]
            for out in as_completed(futures):
                yield out.result()


def _deploy(_from, _to):
    pass

def _copy(_from, _to):
    pass

def _unpack(_from, _to):
    pass

def _pull(_from, _to):
    pass
def _ignore(*args):
    print(f"IGNORING {', '.join(args)}")

INSTRUCTIONS = {
    "DEPLOY": _deploy,
    "COPY": _copy,
    "PULL": _pull,
    "UNPACK": _unpack
}

def _parse_download_commands(rp: RPFileParser):
    config_url = parse.urlparse(os.environ["server"]) 
    for step in rp.structure:
        if step["instruction"] in ["COPY", "UNPACK"]:
            url: parse.ParseResult = parse.urlparse(parse_arguments(step["value"])[0])
            if not url.scheme:
                url = url._replace(scheme=config_url.scheme)
            if not url.netloc:
                url = url._replace(netloc=config_url.netloc)
            # if url.scheme in ["http", "https"]:
            step["url"] = url.geturl()
            yield step

rp_file = RPFileParser("./")

OPTIONS = {"server": rp_file.args.get("SERVER", "http://server.pingus/")}
for option in OPTIONS:
    os.environ[option] = OPTIONS[option]

for command in parallel_download_commands(_parse_download_commands(rp_file)):
    INSTRUCTIONS.get(command["instruction"], _ignore)(command["path"],parse_arguments(command["value"])[-1])

# for step in rp_file.structure:

    # print(parser.parse_args())

# print(rp_file.args)
