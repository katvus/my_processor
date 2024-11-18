from exception import TranslationError
from instruction import Instruction, FirstInstruction, SecondInstruction, ThirdInstruction, SysInstruction


def translation(file, new_name):
    bin_file = open(new_name, 'w')
    count = 0
    for line in file:
        count += 1
        line = line.split('//')[0].replace('\n', '').split(' ')
        try:
            if FirstInstruction.translate(line) != 'null':
                bin_file.write(FirstInstruction.translate(line))
            elif SecondInstruction.translate(line) != 'null':
                bin_file.write(SecondInstruction.translate(line))
            elif ThirdInstruction.translate(line) != 'null':
                bin_file.write(ThirdInstruction.translate(line))
            elif SysInstruction.translate(line) != 'null':
                bin_file.write(SysInstruction.translate(line))
            else:
                raise TranslationError('недопустимая операция')
        except TranslationError as e:
            print('{0} строка {1}'.format(count, e))
            exit()
