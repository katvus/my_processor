from instruction import Execution
from exception import MyProgramError
from processor import Processor


my_proc = Processor()
with open('data/factorial_sys', 'r', encoding='utf-8') as file:
    content = file.readlines()
    while my_proc.pc <= len(content):
        line = content[my_proc.pc - 1].split('//')[0].replace('\n', '')
        line = line.split(' ')
        try:
            execute = Execution(my_proc, line)
            if line == ['сис']:
                execute.sys()
            elif len(line) == 4:
                if not execute.f_op():
                    Execution.t_op()
            elif len(line) == 3:
                execute.s_op()
            else:
                raise MyProgramError('недопустимая операция(количество операндов)')
        except MyProgramError as e:
            print('{0} строка {1}'.format(my_proc.pc, e))
            exit()
    print("Успех")
