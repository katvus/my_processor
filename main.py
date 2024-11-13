import instruction
from exception import MyProgramError
from processor import Processor


my_proc = Processor()
with open('data/factorial_sys', 'r', encoding='utf-8') as file:
    content = file.readlines()
    while my_proc.pc <= len(content):
        line = content[my_proc.pc - 1].split('//')[0].replace('\n', '')
        line = line.split(' ')
        try:
            if line == ['сис']:
                instruction.sys(my_proc)
            elif len(line) == 4:
                if not instruction.f_op_proc(line, my_proc):
                    instruction.t_op_proc(line, my_proc)
            elif len(line) == 3:
                instruction.s_op_proc(line, my_proc)
            else:
                raise MyProgramError('недопустимая операция(количество операндов)')
        except MyProgramError as e:
            print('{0} строка {1}'.format(my_proc.pc, e))  # номер строки как вывести
            exit()
    print("Успех")
