# Space Pictures Telegram Bot

A set of scripts for a Telegram bot that posts pictures of space

### How to install

Python3 should be already installed.
Download the [ZIP archive](https://github.com/Katsutami7moto/space-pictures-telegram-bot/archive/refs/heads/main.zip) of the code and unzip it.
Then open terminal form unzipped directory and use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```commandline
pip install -r requirements.txt
```
Before you run any of the scripts, you may need to configure environmental variables:

1. Go to the unzipped directory and create a file with the name `.env` (yes, it has only the extension).
It is the file to contain environmental variables that usually store data unique to each user, thus you will need to create your own.
2. Copy and paste this to `.env` file:
```dotenv
NASA_API_KEY='{nasa_key}'
TELEGRAM_API_TOKEN='{telegram_token}'
TELEGRAM_CHANNEL_ID='@{channel_id}'
IMAGES_DIR='{dir_path}'
```
3. Replace `{nasa_key}` with [NASA API](https://api.nasa.gov/) key you will receive when you sign up.
4. Replace `{telegram_token}` with API token for the Telegram bot you have created with the help of [BotFather](https://telegram.me/BotFather). This token will look something like this: `958423683:AAEAtJ5Lde5YYfkjergber`.
5. Replace `{channel_id}` with the identificator (as in the `https://t.me/{identificator}`) of the Telegram channel you have created.
6. Don't forget to appoint the bot as an administrator of the channel (in the channel settings) and give it rights to post in the channel (in `BotFather` menu, `Bot Settings` -> `Channel Admin Rights` -> `Post in the channel`).
7. Replace `{dir_path}` with the path to directory where you want to store downloaded images. It has default value - when you run one of the `fetch_***.py` scripts, the directory with the name `images` will be created in the unzipped directory. If you want to use the default value, simply delete `IMAGES_DIR='{dir_path}'` line from `.env` file.

### How to use

Download images by running either or all of `fetch_***.py` scripts, like this:
```commandline
python3 fetch_nasa_apod_images.py

python3 fetch_nasa_epic_images.py

python3 fetch_spacex_images.py
```

You can run `fetch_spacex_images.py` script with `--id` parameter, giving it the identificator of a particular SpaceX launch, like this:
```commandline
python3 fetch_spacex_images.py --id 5eb87d47ffd86e000604b38a
```
If an identificator wasn't given, this script will fetch photos from latest launch.

If a picture's size is too big to be published in a Telegram channel (more than 10 megabytes), it will be compressed automatically.

Then, you can publish just one image to your channel either of these ways:

- a random picture from `IMAGES_DIR`
```commandline
python3 telegram_bot_single.py
```

- a specific picture from `IMAGES_DIR`
```commandline
python3 telegram_bot_single.py --file file_in_images_dir.ext
```

Or, you can set a loop which will shuffle pictures in `IMAGES_DIR` and post one each `X` hours (integer number, optional argument, default value is `4`):
```commandline
python3 telegram_bot_loop.py --delay X
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
