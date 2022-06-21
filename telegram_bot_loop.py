from configargparse import ArgParser
from dotenv import load_dotenv


def main():
    load_dotenv()
    parser = ArgParser()
    parser.add_argument(
        '-d', '--delay',
        help='Amount of hours to wait until next post',
        env_var='DELAY',
        default=4
    )
    options = parser.parse_args()
    delay_hours: int = options.delay


if __name__ == "__main__":
    main()
