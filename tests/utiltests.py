from evolution.util import *
from evolution.genome import ConnectionGene
from copy import copy
import unittest


class UtilTestCase(unittest.TestCase):
    def setUp(self):
        # stanley example crossover of 2 genomes
        def getConn(weight):
            return ConnectionGene(0, 0, weight, True)

        # each connection have innovation number the same as its weight
        # number of excess: 2 (9 and 10)
        # number of disjoint: 3 (6, 7, 8)
        # avg weight difference: 0 (common connections have the same weight from 1 to 5)
        self.connections_a = []
        self.connections_b = []
        self.connections_a = [
            getConn(1),
            getConn(2),
            getConn(3),
            getConn(4),
            getConn(5)
        ]
        self.connections_b = copy(self.connections_a)

        self.connections_b.append(getConn(6))
        self.connections_b.append(getConn(7))

        self.connections_a.append(getConn(8))

        self.connections_b.append(getConn(9))
        self.connections_b.append(getConn(10))

        self.connections_a = sorted(self.connections_a, key=lambda x: x.innovation_number)
        self.connections_b = sorted(self.connections_b, key=lambda x: x.innovation_number)

    def test_count_disjoint_connection_genes(self):
        self.assertEqual(3, count_disjoint_connection_genes(self.connections_a, self.connections_b))

    def test_count_excess_connection_genes(self):
        self.assertEqual(2, count_excess_connection_genes(self.connections_a, self.connections_b))

    def test_count_avg_weight_difference(self):
        self.assertEqual(0, count_avg_weight_difference(self.connections_a, self.connections_b))


if __name__ == '__main__':
    firstSuite = unittest.TestLoader().loadTestsFromTestCase(UtilTestCase)
    unittest.TextTestRunner(verbosity=2).run(firstSuite)
