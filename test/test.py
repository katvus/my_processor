import unittest

from processor import Processor
from instruction import Operation
from instruction import Execution


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


class ExecutionTest(unittest.TestCase):
    def setUp(self):
        self.proc = Processor()
        self.proc.registers[11] = 3
        self.proc.registers[12] = 2
        self.proc.mem[9] = 13

    def test_f_op(self):
        Execution(self.proc, ["сл", "р10", "р11", "р12"]).f_op()
        self.assertEqual(self.proc.registers[10], 5)

    def test_s_op(self):
        Execution(self.proc, ["усл", "р11", "21"]).s_op()
        self.assertEqual(self.proc.pc, 22)

    def test_t_op(self):
        Execution(self.proc, ["изп", "р10", "р12", "7"]).t_op()
        self.assertEqual(self.proc.registers[10], 13)


if __name__ == '__main__':
    unittest.main()
