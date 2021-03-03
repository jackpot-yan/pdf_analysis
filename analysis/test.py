import unittest
from io import *

from text_detection import *


class Test(unittest.TestCase):
    def test_get_file_data(self):
        result = File(path, None).get_file_data()
        self.assertIsInstance(obj=result, cls=BufferedReader)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
