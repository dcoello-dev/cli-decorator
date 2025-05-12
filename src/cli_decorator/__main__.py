import sys
import argparse
import subprocess

from cli_decorator.Palette import *
from cli_decorator.Logger import *
from cli_decorator.Animation import *


def _ex_subprocess(cmd: str, shell=True, forward_stdout=None) -> tuple:
    p = subprocess.Popen(
        f"unbuffer {cmd}", shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        executable='/bin/bash')
    if forward_stdout is not None:
        while True:
            line = p.stdout.readline()
            if not line:
                break
            forward_stdout.through(line.rstrip())
    output, error = p.communicate()
    return (p.returncode, output, error)


def sink(args, send):
    if not sys.stdin.isatty():
        for line in args.stdin:
            line = line.replace('\n', '')
            send(cl(line, args.color))
    else:
        lines = f"{' '.join(args.text)}".split('\n')
        for line in lines:
            send(cl(line, args.color))


def color_text():
    parser = argparse.ArgumentParser(
        description="colorize text")

    parser.add_argument('text', nargs=argparse.REMAINDER)
    parser.add_argument('stdin', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-c', '--color', default=COLOR.WHITE,
                        type=COLOR, choices=list(COLOR))

    args = parser.parse_args()
    sink(args, print)


def log_text():
    parser = argparse.ArgumentParser(
        description="log text")

    parser.add_argument('text', nargs=argparse.REMAINDER)
    parser.add_argument('stdin', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-n', '--name', default="cll")
    parser.add_argument('-c', '--color', default=COLOR.WHITE,
                        type=COLOR, choices=list(COLOR))
    parser.add_argument(
        '-l', '--log_level',
        default='info', choices=['error', 'warning', 'info', 'debug', 'verbose'],
        help="app log level")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(eval(f"logging.{args.log_level.upper()}"))
    logger.addHandler(ColorHandler(context=args.name))
    sink(args, eval(f"logger.{args.log_level}"))


def void(_):
    pass


def progress_command():
    parser = argparse.ArgumentParser(
        description="log text")

    parser.add_argument('command', nargs=argparse.REMAINDER)
    parser.add_argument('stdin', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        default=False,
        help="forward command stdout")
    parser.add_argument('-c', '--color', default=COLOR.WHITE,
                        type=COLOR, choices=list(COLOR))
    parser.add_argument('-n', '--name', default="cll")
    parser.add_argument(
        '-l', '--log_level',
        default='info', choices=['error', 'warning', 'info', 'debug', 'verbose'],
        help="app log level")
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(eval(f"logging.{args.log_level.upper()}"))
    logger.addHandler(ColorHandler(context=args.name))

    command = ' '.join(args.command)
    a = Animation(logger, args.name,  f"executing {cl(command, COLOR.YELLOW)}",
                  f"{command} {cl('OK!', COLOR.GREEN)}", f"{command} {cl('ERROR!', COLOR.RED)}")
    try:
        if len(args.command) > 0:
            a.start()
            f = None
            if args.verbose:
                f = a
            a.end(_ex_subprocess(command, forward_stdout=f)[0] == 0)
        else:
            a.start()
            sink(args, a.through if args.verbose else void)
            a.end()
    except KeyboardInterrupt:
        a.end()
