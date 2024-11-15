class Registers(list):
    def __setitem__(self, key, value):
        if key == 0:
            super().__setitem__(key, 0)
        else:
            super().__setitem__(key, value)


class Processor:
    def __init__(self, pc=1, registers=None, mem=None):
        if registers is None:
            self.registers = Registers([0] * 16)
            self.registers[2] = 255
        else:
            self.registers = registers
        if mem is None:
            self.mem = [0] * 256
        else:
            self.mem = mem
        self.pc = pc
