from enum import Enum

SEQ = '\033['
SEP = ';'
N = '2'
END = 'm'
FG = '38'
BG = '48'
L = [FG, BG]
RESET = f'{SEQ}0{END}'
BACKSPACE = '\x08'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def fg(color):
    color = list(color)
    color[3] = FG
    return color


def bg(color):
    color = list(color)
    color[3] = BG
    return color


def rgb(text, color):
    return f"{SEQ}{color[3]};{N};{str(color[0])};{str(color[1])};{str(color[2])}m{text}"


def delete(text, n):
    return f"{text}{''.join([BACKSPACE for i in range(0, n)])}"


def reset(text):
    return f"{text}{RESET}"


class COLOR(Enum):
    RED = 'RED'
    BLUE = 'BLUE'
    GREEN = 'GREEN'
    YELLOW = 'YELLOW'
    PINK = 'PINK'
    ORANGE = 'ORANGE'
    PURPLE = 'PURPLE'
    GREY = 'GREY'
    BLACK = 'BLACK'
    WHITE = 'WHITE'

    def __str__(self):
        return self.value


class Color():

    def __init__(self, r, g, b, l=FG, name="custom"):
        super().__init__()
        self.name_ = name
        self.value_ = (r, g, b, l)

    def __str__(self):
        return f"{cl(self.name_, self)} {self['r']}:{self['g']}:{self['b']}"

    def __getitem__(self, key):
        if type(key) is int:
            return self.value_[key]

        if type(key) is str:
            if key == "r":
                return self.value_[0]
            if key == "g":
                return self.value_[1]
            if key == "b":
                return self.value_[2]
            if key == "l":
                return self.value_[3]

        return None


class Palette:
    def __init__(self, palette):
        self.palette_ = palette

    def __getitem__(self, key):
        if type(key) == str:
            key = eval(f"COLOR.{key}")
        return self.palette_[key]


class DefaultPalette(Palette):
    COLORS = {
        COLOR.RED: Color(255, 8, 8, name=COLOR.RED),
        COLOR.YELLOW: Color(255, 255, 51, name=COLOR.YELLOW),
        COLOR.BLUE: Color(30, 136, 229, name=COLOR.BLUE),
        COLOR.PINK: Color(233, 30, 99, name=COLOR.PINK),
        COLOR.ORANGE: Color(255, 87, 34, name=COLOR.ORANGE),
        COLOR.PURPLE: Color(171, 71, 188, name=COLOR.PURPLE),
        COLOR.GREY: Color(189, 189, 189, name=COLOR.GREY),
        COLOR.GREEN: Color(46, 204, 113, name=COLOR.GREEN),
        COLOR.BLACK: Color(0, 0, 0, name=COLOR.BLACK),
        COLOR.WHITE: Color(255, 255, 255, name=COLOR.WHITE)
    }

    def __init__(self):
        super().__init__(self.COLORS)


def cl(text, color, palette=DefaultPalette):
    return reset(rgb(text, palette()[color]))


if __name__ == "__main__":
    print(DefaultPalette()[COLOR.RED])
    print(DefaultPalette()['RED'])
