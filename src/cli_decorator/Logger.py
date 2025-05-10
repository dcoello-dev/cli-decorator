import logging
import datetime

from cli_decorator.Palette import *


class ColorHandler(logging.Handler):
    C_DIS = dict(VERBOSE=COLOR.GREY, DEBUG=COLOR.GREY, INFO=COLOR.GREEN,
                 WARNING=COLOR.ORANGE, ERROR=COLOR.RED, ONGOING=COLOR.YELLOW)

    def __init__(self, context="Main", enable_color=True):
        super().__init__()
        self.context_ = context
        self.enable_color_ = enable_color

    def cl(self, text, color, palette=DefaultPalette):
        if self.enable_color_:
            return reset(rgb(text, palette()[color]))
        return text

    def emit(self, record):
        print(self.get_msg(record.levelname, record.getMessage()))

    def get_msg(self, level_log, msg):
        level = "%(level)-7s" % {"level": level_log}
        return f"[{datetime.datetime.now().time()}] [{self.cl(self.context_, COLOR.BLUE)}] [{self.cl(level, self.C_DIS[level_log])}]: {msg}"
