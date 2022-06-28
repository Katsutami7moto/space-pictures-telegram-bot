import requests
from environs import Env
from pathlib import Path

from download_images import download_pictures_to_dir, compress_image


def fetch_nasa_apod_pics(api_key: str, count: int) -> list:
    api_url = 'https://api.nasa.gov/planetary/apod'
    params = {
        'api_key': api_key,
        'count': count,
    }
    api_response = requests.get(url=api_url, params=params)
    api_response.raise_for_status()
    apod_response: list = api_response.json()
    apods = filter(lambda x: 'hdurl' in x, apod_response)
    return [apod['hdurl'] for apod in apods]


def main():
    env = Env()
    env.read_env()
    nasa_api_key: str = env('NASA_API_KEY')
    images_dir: str = env('IMAGES_DIR', default='images')
    images_path = Path(images_dir)
    images_path.mkdir(parents=True, exist_ok=True)
    downloaded_pictures = download_pictures_to_dir(
        images_path,
        fetch_nasa_apod_pics(nasa_api_key, count=10),
        prefix='nasa_apod'
    )
    for picture in downloaded_pictures:
        compress_image(picture)


if __name__ == "__main__":
    main()
