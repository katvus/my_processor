import enum

from exception import MyProgramError


def load_reg(rd, const, proc):
    proc.registers[rd] = const
    proc.pc += 1


def jump(rd, const, proc):
    proc.registers[rd] = proc.pc + 1
    proc.pc += const


def cond_jump(rd, const, proc):
    if (proc.registers[rd]) >= 0:
        proc.pc += const
    else:
        proc.pc += 1


def store_mem(rd, rbase, const, proc):
    proc.registers[rd] = proc.mem[proc.registers[rbase] + const]
    proc.pc += 1


def load_mem(rs, rbase, const, proc):
    proc.mem[proc.registers[rbase] + const] = proc.registers[rs]
    proc.pc += 1


def reg_jump(rd, rbase, const, proc):
    proc.registers[rd] = proc.pc + 1
    proc.pc = proc.registers[rbase] + const


dict_t_op = {'изп': store_mem, 'вп': load_mem, 'опер': reg_jump}


dict_s_op = {'вр': load_reg, 'пер': jump, 'усл': cond_jump}


dict_f_op = {'сл': lambda a, b: a + b, 'выч': lambda a, b: a - b,
             'умн': lambda a, b: a * b, 'дел': lambda a, b: a / b,
             'и': lambda a, b: a & b, 'или': lambda a, b: a | b,
             'свл': lambda a, b: a << b, 'свп': lambda a, b: a >> b,
             'иили': lambda a, b: a ^ b}


def f_op_proc(data, proc):
    if data[0] in dict_f_op:
        proc.registers[register_number(data[1])] = dict_f_op[data[0]](
            proc.registers[register_number(data[2])], proc.registers[register_number(data[3])])
        proc.pc += 1
        return True
    return False


def s_op_proc(data, proc):
    if data[0] in dict_s_op:
        if isint(data[2]) and -128 <= int(data[2]) <= 127:
            dict_s_op[data[0]](register_number(data[1]), int(data[2]), proc)
        else:
            raise MyProgramError('не является числом в возможном диапазоне')
    else:
        raise MyProgramError('недопустимая операция')


def t_op_proc(data, proc):
    if data[0] in dict_t_op:
        if isint(data[3]) and -8 <= int(data[3]) <= 7:
            dict_t_op[data[0]](register_number(data[1]), register_number(data[2]),  int(data[3]), proc)
        else:
            raise MyProgramError('не является числом в возможном диапазоне')
    else:
        raise MyProgramError('недопустимая операция')


def register_number(data):
    if data[0] == 'р' and data[1:].isdigit():
        if 0 <= int(data[1:]) <= 15:
            return int(data[1:])
    raise MyProgramError('не является регистром')


def isint(data):
    if (data[0] == '-' and data[1:].isdigit()) or data.isdigit():
        return True
    return False


class SysCall(enum.Enum):
    exit = 0
    print = 1
    input = 2


def sys(proc):
    proc.pc += 1
    if proc.registers[4] == SysCall.print.value:
        print(proc.registers[5])
    elif proc.registers[4] == SysCall.input.value:
        proc.registers[5] = int(input())
    elif proc.registers[4] == SysCall.exit.value:
        exit()
    else:
        MyProgramError('недопустимый системный вызов')
