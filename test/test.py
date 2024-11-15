import unittest

from processor import Processor


class OperationTest(unittest.TestCase):
    def SetUp(self):
        self.proc = Processor()

    def test_load_reg(self):
        self.assertEqual(Operation.load_reg(), False)


if __name__ == '__main__':
    unittest.main()
