import argparse

import requests

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
    if flickr_links:
        return flickr_links


if __name__ == "__main__":
    # Get pictures from SpaceX api
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', help='ID of launch to get images of')
    args = parser.parse_args()
    if args.id:
        args_id: str = args.id
        args_id = args_id.strip()
    else:
        args_id = ''
    download_pictures_to_dir(
        fetch_spacex_last_launch(launch_id=args_id),
        'spacex'
    )
