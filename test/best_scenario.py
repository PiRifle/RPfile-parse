from asyncio import wait
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from os.path import abspath
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


def parallel_download(links):
    with ThreadPoolExecutor(4) as executor:
        futures = [executor.submit(download, i) for i in links]
        wait(futures)
        for out in as_completed(futures):
            yield out.result()

urls = [
    "http://localhost:3000/testfile100mb.bin",
    "http://localhost:3000/testfile10mb.bin",
    # "http://localhost:3000/testfile1gb.bin",
]
with progress:
    print(list(parallel_download(urls)))