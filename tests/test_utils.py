import unittest
import utils
from datetime import date


class TestUtil(unittest.TestCase):

    def test_split(self):
        d = date(2023, 1, 1)
        monday = utils.get_first_monday(d)
        self.assertEqual(date(2023, 1, 2), monday)


if __name__ == '__main__':
    unittest.main()
