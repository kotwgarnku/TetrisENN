import unittest

from evolution.genome import ConnectionGene, NodeGene, Genome


class TestConnectionGeneCase(unittest.TestCase):
    def setUp(self):
        self.connectionGene1 = ConnectionGene(NodeGene(), NodeGene())
        self.connectionGene2 = ConnectionGene(NodeGene(), NodeGene())
        self.connectionGene3 = ConnectionGene(NodeGene(), NodeGene())

    def test_innovation_number_assignment1(self):
        self.assertEqual(self.connectionGene1.innovation_number, 0)
        self.assertEqual(self.connectionGene2.innovation_number, 1)
        self.assertEqual(self.connectionGene3.innovation_number, 2)


class TestGenomeCase(unittest.TestCase):

    def test_invalid_connection_exception(self):
        with self.assertRaises(Exception):
            ConnectionGene(NodeGene())
            ConnectionGene()

    def test_uniqueness_of_connections(self):
        connections = [[1, 3, 0, True], [1, 3, 0, True]]
        with self.assertRaises(Exception):
            Genome(connections)

    def test_genome_creation_with_empty_node(self):
        with self.assertRaises(Exception):
            Genome([[1, None, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]])




if __name__ == '__main__':
    firstSuite = unittest.TestLoader().loadTestsFromTestCase(TestGenomeCase)
    secondSuite = unittest.TestLoader().loadTestsFromTestCase(TestConnectionGeneCase)
    unittest.TextTestRunner(verbosity=2).run(firstSuite)
    unittest.TextTestRunner(verbosity=2).run(secondSuite)