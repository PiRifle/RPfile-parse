import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn

progress = Progress()

def download(url):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get("content-length", 0))
    block_size = 524288
    progress_bar = progress.add_task(f"downloading {url}", total=total_size)
    with progress:
        with open(url.split("/")[-1], "wb") as file:
            for data in response.iter_content(block_size):
                progress.update(progress_bar, advance=len(data))
                file.write(data)
            progress.remove_task(progress_bar)




urls = [
    "http://192.168.8.182:3000/windows10_vm.img",
    "http://192.168.8.182:3000/ubuntu_server_2022.img",
    "http://192.168.8.182:3000/centos.iso",
    "http://192.168.8.182:3000/zip_10MB.zip",
]
for i in urls:
    download(i)