import time
import sys
import itertools
import threading

from cli_decorator.Palette import *
from cli_decorator.Logger import *


class Animation(threading.Thread):
    def __init__(self, logger, name, ongoing_msg, end_message_ok, end_message_failure):
        super().__init__()
        self.name_ = name
        self.logger_ = logger
        self.ongoing_msg_ = ongoing_msg
        self.end_message_ok_ = end_message_ok
        self.end_message_failure_ = end_message_failure
        self.ok_ = True
        self.t_start_ = None
        self.t_end_ = None

    def update(self, msg):
        self.msg_ = msg

    def run(self):
        self.t_start_ = datetime.datetime.now()
        self.end_ = False
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.end_:
                break
            sys.stdout.write(
                f'\r[{cl(c, COLOR.BLUE)}] {ColorHandler(self.name_).get_msg("ONGOING", self.ongoing_msg_)}')
            sys.stdout.flush()
            time.sleep(0.1)

        self.t_end_ = datetime.datetime.now()
        sys.stdout.write(f'\r')
        if self.ok_:
            self.logger_.info(
                f'[{self.t_end_ - self.t_start_}] {self.end_message_ok_}')
        else:
            self.logger_.error(
                f'[{self.t_end_ - self.t_start_}] {self.end_message_failure_}')

    def through(self, msg):
        sys.stdout.write(f'\r')
        self.logger_.info(f'{msg}')

    def end(self, ok=True):
        self.end_ = True
        self.ok_ = ok
        self.join()
