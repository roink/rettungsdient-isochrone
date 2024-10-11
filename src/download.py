import os
import requests
import zipfile
from requests.exceptions import RequestException


def download_file(url: str, download_dir: str) -> str:
    """
    Downloads a file from a given URL and saves it in the specified directory.
    Returns the path to the downloaded file.
    """
    filename = os.path.basename(url)
    filepath = os.path.join(download_dir, filename)

    if not os.path.exists(filepath):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(url, headers=headers, stream=True)
            response.raise_for_status()

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)

            print(f"Downloaded {filename}.")
        except RequestException as e:
            print(f"Failed to download {url}: {e}")
            raise
    else:
        print(f"{filename} already exists.")

    return filepath


def unzip_file(filepath: str, extract_to: str):
    """
    Unzips the given ZIP file to the specified directory.
    """
    if filepath.endswith('.zip'):
        try:
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            print(f"Unzipped {os.path.basename(filepath)}.")
        except zipfile.BadZipFile as e:
            print(f"Failed to unzip {filepath}: {e}")
            raise
    else:
        print(f"{os.path.basename(filepath)} is not a ZIP file, no extraction needed.")


def download_and_unzip(identifier: str, download_dir: str = None):
    """
    Downloads a file from the given URL or nickname and unzips it if it's a ZIP file.
    """
    if download_dir is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        download_dir = os.path.join(os.path.dirname(current_dir), "data", "raw")

    # Determine if the identifier is a URL or a nickname
    if identifier in DATASET_URLS:
        url = DATASET_URLS[identifier]
    else:
        url = identifier

    filepath = download_file(url, download_dir)
    unzip_file(filepath, download_dir)


DATASET_URLS = {
    "Wohnbezirke_Hagen": "https://www.hagen.de/web/media/files/fb/stadtplaene/wahlen_und_statistik/Wohnbezirke_Hagen.zip",
    "Statistische_Bezirke_Hagen": "https://www.hagen.de/web/media/files/fb/stadtplaene/wahlen_und_statistik/Statistische_Bezirke_Hagen.zip",
    "Stadtbezirke": "https://www.hagen.de/web/media/files/fb/stadtplaene/wahlen_und_statistik/Stadtbezirke.zip",
    "Hauskoordinaten": "http://www.stadtplan.hagen.de/StrVz/Hauskoordinaten.csv"
}


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    raw_data_dir = os.path.join(os.path.dirname(current_dir), "data", "raw")
    os.makedirs(raw_data_dir, exist_ok=True)

    for nickname in DATASET_URLS.keys():
        try:
            download_and_unzip(nickname, raw_data_dir)
        except Exception as e:
            print(f"Error processing {nickname}: {e}")


if __name__ == "__main__":
    main()