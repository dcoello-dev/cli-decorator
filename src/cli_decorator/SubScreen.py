
class SubScreen:
    def __init__(self, n):
        self.resize(n)

    def size(self):
        return self.n_

    def resize(self, n):
        self.n_ = n
        [print() for _ in range(0, n)]
        self.last_ = ''.join(['\n' for _ in range(0, self.n_ - 1)])

    def clean(self, n=None):
        if n is None:
            n = self.n_
        t = ''.join(['\n' for _ in range(0, n - 1)])
        print(f"\033[{n}A\033[J{t}")

    def rewrite(self, lines):
        t = '\n'.join(lines)
        print(f"\033[{len(lines)}A\033[J{t}")

    def draw(self, text, save=True):
        self.clean()
        lines = text.split("\n")
        l = len(lines)
        if save:
            self.last_ = "\n".join(lines[0 if l <= self.n_ else l - self.n_:])
        if l > self.n_:
            [print() for _ in range(0, l - self.n_)]
        self.rewrite(lines)

    def through(self, text):
        text += ''.join(['\n' for _ in range(0, self.n_)])
        self.clean(self.n_)
        self.draw(text, save=False)
        self.draw(self.last_)
