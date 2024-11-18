from instruction import FirstInstruction, SecondInstruction, ThirdInstruction, SysInstruction
from processor import Processor
from translation import translation

FILENAME = 'data/factorial_sys'
BINFILE = 'data/program'

file = open(FILENAME, 'r', encoding='utf-8')
translation(file, BINFILE)
my_proc = Processor()
with open(BINFILE, 'r') as bin_file:
    content = bin_file.read()
    start_symbol = (my_proc.pc - 1) * 16
    end_symbol = start_symbol + 16
    while start_symbol < len(content):
        word = content[start_symbol:end_symbol]
        data = [word[0:4], word[4:8], word[8:12], word[12:16]]
        if not FirstInstruction.execute(data, my_proc):
            if not SecondInstruction.execute(data, my_proc):
                if not ThirdInstruction.execute(data, my_proc):
                    SysInstruction.execute(data, my_proc)
        start_symbol = (my_proc.pc - 1) * 16
        end_symbol = start_symbol + 16


print("Успех")
