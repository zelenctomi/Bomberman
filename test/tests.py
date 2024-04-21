import unittest

# This is the function you want to test
def add(a, b):
    return a + b

# This is your test case class
class TestAddFunction(unittest.TestCase):
    def test_add(self):
        # Test if 1 + 1 equals 2
        self.assertEqual(add(1, 1), 2)

        # Test if -1 + 1 equals 0
        self.assertEqual(add(-1, 1), 0)

# This allows the test to be run
if __name__ == '__main__':
    unittest.main()
