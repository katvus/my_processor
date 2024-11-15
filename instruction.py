import enum

from exception import MyProgramError


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


class Execution:
    __dict_f_op = {'сл': lambda a, b: a + b, 'выч': lambda a, b: a - b,
                   'умн': lambda a, b: a * b, 'дел': lambda a, b: a / b,
                   'и': lambda a, b: a & b, 'или': lambda a, b: a | b,
                   'свл': lambda a, b: a << b, 'свп': lambda a, b: a >> b,
                   'иили': lambda a, b: a ^ b}
    __dict_s_op = {'вр': Operation.load_reg, 'пер': Operation.jump, 'усл': Operation.cond_jump}
    __dict_t_op = {'изп': Operation.store_mem, 'вп': Operation.load_mem, 'опер': Operation.reg_jump}

    def __init__(self, processor, data):
        self.proc = processor
        self.data = data

    def f_op(self):
        if self.data[0] in self.__dict_f_op:
            self.proc.registers[register_number(self.data[1])] = self.__dict_f_op[self.data[0]](
                self.proc.registers[register_number(self.data[2])], self.proc.registers[register_number(self.data[3])])
            self.proc.pc += 1
            return True
        return False

    def s_op(self):
        if self.data[0] in self.__dict_s_op:
            if isint(self.data[2]) and -128 <= int(self.data[2]) <= 127:
                self.__dict_s_op[self.data[0]](register_number(self.data[1]), int(self.data[2]), self.proc)
            else:
                raise MyProgramError('не является числом в возможном диапазоне')
        else:
            raise MyProgramError('недопустимая операция')

    def t_op(self):
        if self.data[0] in self.__dict_t_op:
            if isint(self.data[3]) and -8 <= int(self.data[3]) <= 7:
                self.__dict_t_op[self.data[0]](register_number(self.data[1]), register_number(self.data[2]),  int(self.data[3]), self.proc)
            else:
                raise MyProgramError('не является числом в возможном диапазоне')
        else:
            raise MyProgramError('недопустимая операция')

    def sys(self):
        self.proc.pc += 1
        if self.proc.registers[4] == SysCall.print.value:
            print(self.proc.registers[5])
        elif self.proc.registers[4] == SysCall.input.value:
            self.proc.registers[5] = int(input())
        elif self.proc.registers[4] == SysCall.exit.value:
            exit()
        else:
            MyProgramError('недопустимый системный вызов')


class SysCall(enum.Enum):
    exit = 0
    print = 1
    input = 2


def register_number(data):
    if data[0] == 'р' and data[1:].isdigit():
        if 0 <= int(data[1:]) <= 15:
            return int(data[1:])
    raise MyProgramError('не является регистром')


def isint(data):
    if (data[0] == '-' and data[1:].isdigit()) or data.isdigit():
        return True
    return False
