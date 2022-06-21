import argparse
from dotenv import load_dotenv


def main():
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--delay',
        help='Amount of hours to wait until next post',
        default=4
    )
    args = parser.parse_args()
    delay_hours: int = args.delay


if __name__ == "__main__":
    main()
