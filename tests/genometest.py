import unittest

from evolution.genome import ConnectionGene


class TestGenomeCase(unittest.TestCase):

    def test_innovation_number_assignment1(self):
        genome1 = ConnectionGene()
        genome2 = ConnectionGene()
        genome3 = ConnectionGene()
        self.assertEqual(genome1.innovation_number, 0)
        self.assertEqual(genome2.innovation_number, 1)
        self.assertEqual(genome3.innovation_number, 2)

    def test_innovation_number_assignment2(self):
        genome = ConnectionGene()
        self.assertEqual(genome.innovation_number, 3)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGenomeCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
