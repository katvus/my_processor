class Registers(list):
    def __setitem__(self, key, value):
        if key == 0:
            super().__setitem__(key, 0)
        else:
            super().__setitem__(key, value)


class Processor:
    registers = Registers([0] * 16)
    mem = [0] * 256
    registers[2] = 255
    pc = 1
