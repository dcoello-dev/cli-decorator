import sys
import argparse

from cli_decorator.Palette import *
from cli_decorator.Logger import *


def get_text(args):
    text = ""
    if not sys.stdin.isatty():
        text = args.stdin.read()[:-1]
    text += f"{' '.join(args.text)}"
    return text


def color_text():
    parser = argparse.ArgumentParser(
        description="colorize text")

    parser.add_argument('text', nargs=argparse.REMAINDER)
    parser.add_argument('stdin', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-c', '--color', default=COLOR.WHITE,
                        type=COLOR, choices=list(COLOR))

    args = parser.parse_args()
    print(cl(get_text(args), args.color))


def log_text():
    parser = argparse.ArgumentParser(
        description="log text")

    parser.add_argument('text', nargs=argparse.REMAINDER)
    parser.add_argument('stdin', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-n', '--name', default="cll")
    parser.add_argument(
        '-l', '--log_level',
        default='info', choices=['error', 'warning', 'info', 'debug', 'verbose'],
        help="app log level")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(eval(f"logging.{args.log_level.upper()}"))
    logger.addHandler(ColorHandler(context=args.name))
    text = get_text(args)
    eval(f"logger.{args.log_level}('{text}')")


if __name__ == "__main__":
    main()
