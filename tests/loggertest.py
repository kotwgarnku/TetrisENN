import unittest
from evolution.generation import Group, Generation, Genome
from evolution.logger import Logger

class TestLoggerCase(unittest.TestCase):
    def setUp(self):
        Group._GROUP_ID = 0
        Generation._GENERATION_ID = 0
        self.genome1 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome2 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome3 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome4 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome5 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome6 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome7 = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        self.genome1.fitness = 2
        self.genome2.fitness = 0
        self.genome3.fitness = 22
        self.genome4.fitness = 13
        self.genome5.fitness = 2
        self.genome6.fitness = 6
        self.genome7.fitness = 8
        self.group = Group()
        self.group.add_genome(self.genome1)
        self.group.add_genome(self.genome2)
        self.group.add_genome(self.genome3)
        self.group.add_genome(self.genome4)
        self.group.add_genome(self.genome5)
        self.group.add_genome(self.genome6)
        self.group.add_genome(self.genome7)
        self.logger = Logger()
        self.generation = Generation([self.group], logger=self.logger)

    def test_logging(self):
        self.assertIs(self.logger.log[0].groups_log[0], self.group)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLoggerCase)
    unittest.TextTestRunner(suite)