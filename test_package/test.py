import unittest

from processor import Processor
from instruction import Operation, FirstInstruction, SecondInstruction, ThirdInstruction


class ProcessorTest(unittest.TestCase):
    def test_init(self):
        proc = Processor()
        self.assertEqual(proc.pc, 1)
        self.assertEqual(proc.registers[0], 0)
        self.assertEqual(proc.mem[0], 0)


class OperationTest(unittest.TestCase):
    def setUp(self):
        self.proc = Processor(pc=5)
        self.proc.registers[3] = 15
        self.proc.registers[8] = -5
        self.proc.mem[4] = 10

    def test_load_reg(self):
        Operation.load_reg(5, 7, self.proc)
        self.assertEqual(self.proc.registers[5], 7)
        self.assertEqual(self.proc.pc, 6)

    def test_jump(self):
        Operation.jump(2, 4, self.proc)
        self.assertEqual(self.proc.registers[2], 6)
        self.assertEqual(self.proc.pc, 9)

    def test_cond_jump_true(self):
        Operation.cond_jump(0, 7, self.proc)
        self.assertEqual(self.proc.pc, 12)

    def test_cond_jump_false(self):
        Operation.cond_jump(8, 7, self.proc)
        self.assertEqual(self.proc.pc, 6)

    def test_store_mem(self):
        Operation.store_mem(11, 0, 4, self.proc)
        self.assertEqual(self.proc.registers[11], 10)
        self.assertEqual(self.proc.pc, 6)

    def test_load_mem(self):
        Operation.load_mem(8, 3, 5, self.proc)
        self.assertEqual(self.proc.mem[20], -5)
        self.assertEqual(self.proc.pc, 6)

    def test_reg_jump(self):
        Operation.reg_jump(2, 3, 5, self.proc)
        self.assertEqual(self.proc.pc, 20)
        self.assertEqual(self.proc.registers[2], 6)


class FirstInstructionTest(unittest.TestCase):
    def test_translate(self):
        answer = FirstInstruction.translate(['сл', 'р12', 'р10', 'р11'])
        self.assertEqual(answer, '0010110010101011')

    def test_execute(self):
        proc = Processor(pc=5)
        proc.registers[10] = 15
        proc.registers[11] = -5
        FirstInstruction.execute(['0010', '1100', '1010', '1011'], proc)
        self.assertEqual(proc.registers[12], 10)
        self.assertEqual(proc.pc, 6)


class SecondInstructionTest(unittest.TestCase):
    def test_translate(self):
        answer = SecondInstruction.translate(['вр', 'р4', '-1'])
        self.assertEqual(answer, '1000010011111111')

    def test_execute(self):
        proc = Processor(pc=5)
        SecondInstruction.execute(['1000', '0100', '1111', '1111'], proc)
        self.assertEqual(proc.registers[4], -1)
        self.assertEqual(proc.pc, 6)


class ThirdInstructionTest(unittest.TestCase):
    def test_translate(self):
        answer = ThirdInstruction.translate(['опер', 'р2', 'р4', '5'])
        self.assertEqual(answer, '1110001001000101')

    def test_execute(self):
        proc = Processor(pc=5)
        proc.registers[4] = 15
        ThirdInstruction.execute(['1110', '0010', '0100', '0101'], proc)
        self.assertEqual(proc.registers[2], 6)
        self.assertEqual(proc.pc, 20)


if __name__ == '__main__':
    unittest.main()
