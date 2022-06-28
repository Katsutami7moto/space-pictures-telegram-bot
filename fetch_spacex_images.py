import argparse

import requests
from environs import Env

from download_images import download_pictures_to_dir


def fetch_spacex_last_launch(launch_id: str) -> list:
    api_url = 'https://api.spacexdata.com/v4/launches'
    api_response = requests.get(url=api_url)
    api_response.raise_for_status()
    spacex_response: list = api_response.json()
    if launch_id:
        check = lambda x: x['id'] == launch_id
    else:
        check = lambda x: x['links']['flickr']['original']
    launch: dict = list(filter(check, spacex_response))[0]
    flickr_links: list = launch['links']['flickr']['original']
    return flickr_links


if __name__ == "__main__":
    env = Env()
    env.read_env()
    images_dir: str = env('IMAGES_DIR', default='images')
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', help='ID of launch to get images of')
    args = parser.parse_args()
    if args.id:
        args_id: str = args.id
        args_id = args_id.strip()
    else:
        args_id = ''
    spacex_images = fetch_spacex_last_launch(launch_id=args_id)
    if spacex_images:
        download_pictures_to_dir(images_dir, spacex_images, prefix='spacex')
    else:
        print(f'The launch with id "{args_id}" has no photos.')
