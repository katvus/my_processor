import enum
from abc import ABC, abstractmethod

from exception import TranslationError


class Operation:
    @staticmethod
    def load_reg(rd, const, proc):
        proc.registers[rd] = const
        proc.pc += 1

    @staticmethod
    def jump(rd, const, proc):
        proc.registers[rd] = proc.pc + 1
        proc.pc += const

    @staticmethod
    def cond_jump(rd, const, proc):
        if (proc.registers[rd]) >= 0:
            proc.pc += const
        else:
            proc.pc += 1

    @staticmethod
    def store_mem(rd, rbase, const, proc):
        proc.registers[rd] = proc.mem[proc.registers[rbase] + const]
        proc.pc += 1

    @staticmethod
    def load_mem(rs, rbase, const, proc):
        proc.mem[proc.registers[rbase] + const] = proc.registers[rs]
        proc.pc += 1

    @staticmethod
    def reg_jump(rd, rbase, const, proc):
        proc.registers[rd] = proc.pc + 1
        proc.pc = proc.registers[rbase] + const


class Instruction(ABC):
    @property
    @abstractmethod
    def dict_tr(self):
        """Имя операции - двоичный код"""
    @property
    @abstractmethod
    def dict_op(self):
        """Двоичный код - операция"""

    @staticmethod
    @abstractmethod
    def translate(line):
        """Трансляция в машинный код"""

    @staticmethod
    @abstractmethod
    def execute(data, proc):
        """Исполнение команды"""


class FirstInstruction(Instruction):
    dict_tr = {'сл': '0010', 'выч': '0011', 'умн': '0100', 'дел': '0101',
               'и': '1001', 'или': '1010', 'свл': '0111', 'свп': '0110', 'иили': '1011'}
    dict_op = {'0010': lambda a, b: a + b, '0011': lambda a, b: a - b,
               '0100': lambda a, b: a * b, '0101': lambda a, b: a / b,
               '1001': lambda a, b: a & b, '1010': lambda a, b: a | b,
               '0111': lambda a, b: a << b, '0110': lambda a, b: a >> b,
               '1011': lambda a, b: a ^ b}

    @staticmethod
    def translate(line):
        if line[0] in FirstInstruction.dict_tr and len(line) == 4:
            return FirstInstruction.dict_tr[line[0]] + register_bin(line[1]) + register_bin(line[2]) + register_bin(line[3])
        return 'null'

    @staticmethod
    def execute(data, proc):
        if data[0] in FirstInstruction.dict_op:
            proc.registers[int(data[1], 2)] = FirstInstruction.dict_op[data[0]](
                proc.registers[int(data[2], 2)], proc.registers[int(data[3], 2)])
            proc.pc += 1
            return True
        return False


class SecondInstruction(Instruction):
    dict_tr = {'вр': '1000', 'пер': '1101', 'усл': '1100'}
    dict_op = {'1000': Operation.load_reg, '1101': Operation.jump, '1100': Operation.cond_jump}

    @staticmethod
    def translate(line):
        if line[0] in SecondInstruction.dict_tr and len(line) == 3:
            return SecondInstruction.dict_tr[line[0]] + register_bin(line[1]) + int_bin(line[2], 8)
        return 'null'

    @staticmethod
    def execute(data, proc):
        if data[0] in SecondInstruction.dict_op:
            SecondInstruction.dict_op[data[0]](int(data[1], 2), from_bin(data[2] + data[3]), proc)
            return True
        return False


class ThirdInstruction(Instruction):
    dict_tr = {'изп': '0000', 'вп': '0001', 'опер': '1110'}
    dict_op = {'0000': Operation.store_mem, '0001': Operation.load_mem, '1110': Operation.reg_jump}

    @staticmethod
    def translate(line):
        if line[0] in ThirdInstruction.dict_tr and len(line) == 4:
            return ThirdInstruction.dict_tr[line[0]] + register_bin(line[1]) + register_bin(line[2]) + int_bin(line[3], 4)
        return 'null'

    @staticmethod
    def execute(data, proc):
        if data[0] in ThirdInstruction.dict_op:
            ThirdInstruction.dict_op[data[0]](int(data[1], 2), int(data[2], 2), from_bin(data[3]), proc)
            return True
        return False


class SysCall(enum.Enum):
    exit = 0
    print = 1
    input = 2


class SysInstruction(Instruction):
    dict_tr = {'сис': '1111'}
    dict_op = {'1111': SysCall}

    @staticmethod
    def translate(line):
        if line == ['сис']:
            return '1111000000000000'
        return 'null'

    @staticmethod
    def execute(data, proc):
        proc.pc += 1
        if proc.registers[4] == SysCall.print.value:
            print(proc.registers[5])
        elif proc.registers[4] == SysCall.input.value:
            proc.registers[5] = int(input())
        elif proc.registers[4] == SysCall.exit.value:
            exit()
        else:
            return False
        return True


def from_bin(data):
    if data[0] == '0':
        return int(data[1:], 2)
    else:
        count = len(data) - 1
        return int(data[1:], 2) - 2**count


def register_bin(data):
    if data[0] == 'р' and data[1:].isdigit():
        if 0 <= int(data[1:]) <= 15:
            return format(int(data[1:]), '04b')
    raise TranslationError('не является регистром')


def int_bin(data, count):
    if data.isdigit() and 0 <= int(data) < 2**(count - 1):
        return format(int(data), f'0{count}b')
    elif data[0] == '-' and data[1:].isdigit() and -2**(count - 1) <= int(data) < 0:
        return bin(((1 << count) - 1) & int(data))[2:]
    else:
        raise TranslationError('не является числом в возможном диапазоне')
