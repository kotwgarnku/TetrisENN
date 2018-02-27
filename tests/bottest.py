import unittest
from bot.tetris_phenotype_handler import TetrisPhenotypesHandler

class TestGroupCase(unittest.TestCase):
    def test_max_height_difference(self):
        maxim = TetrisPhenotypesHandler(None).calculate_max_height_difference([4, 5, 3, 10, 2, 1, 2])
        self.assertEqual(max(maxim), 9)
        self.assertEqual(maxim.count(2), 4)
        self.assertEqual(maxim.count(8), 2)
        self.assertEqual(maxim.count(1), 6)
        self.assertEqual(len(maxim), 21)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGroupCase)
    unittest.TextTestRunner(verbosity=2).run(suite)