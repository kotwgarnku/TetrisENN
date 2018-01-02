import unittest

from evolution.genome import ConnectionGene, NodeGene, Genome
from evolution.genome import sort_connections_by_innovation_number


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
        connections = [[1, 2, 0, True], [1, 2, 0, True]]
        with self.assertRaises(Exception):
            Genome(connections, 1, 1)

    def test_genome_creation_with_empty_node(self):
        with self.assertRaises(Exception):
            Genome([[1, None, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 1, 2)

    def test_genome_creation_with_loop(self):
        with self.assertRaises(Exception):
            Genome([[1, 1, 0, True]], 1, 0)

    def test_get_connections_ids(self):
        genome = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 2)
        genome2 = Genome([[1, 4, 0, True], [1, 2, 0, True], [1, 3, 0, True]], 1, 3)

        self.assertEqual(genome.get_connections_ids(), [(1, 3), (1, 4), (2, 3), (2, 4)])
        self.assertEqual(genome2.get_connections_ids(), [(1, 4), (1, 2), (1, 3)])

    def test_get_connections(self):
        genome = Genome([[2, 3, 0, True], [1, 4, 0, True], [1, 3, 0, True], [2, 4, 0, True]], 2, 2)
        connections = sorted(genome.get_connections())
        self.assertEqual(connections, [(1, 3, 0, True), (1, 4, 0, True), (2, 3, 0, True), (2, 4, 0, True)])

    def test_get_nodes(self):
        genome = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        nodes = genome.get_nodes()
        self.assertEqual(nodes[0].node_type, 'input')
        self.assertEqual(nodes[0].node_id, 1)
        self.assertEqual(nodes[1].node_type, 'input')
        self.assertEqual(nodes[1].node_id, 2)
        self.assertEqual(nodes[2].node_type, 'hidden')
        self.assertEqual(nodes[2].node_id, 3)
        self.assertEqual(nodes[3].node_type, 'output')
        self.assertEqual(nodes[3].node_id, 4)

    def test_connections_sorting_by_innovation_number(self):
        genome = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        connections = sort_connections_by_innovation_number(genome.connection_genes)
        self.assertLess(connections[0].innovation_number, connections[1].innovation_number)
        self.assertLess(connections[1].innovation_number, connections[2].innovation_number)
        self.assertLess(connections[2].innovation_number, connections[3].innovation_number)




if __name__ == '__main__':
    firstSuite = unittest.TestLoader().loadTestsFromTestCase(TestGenomeCase)
    secondSuite = unittest.TestLoader().loadTestsFromTestCase(TestConnectionGeneCase)
    unittest.TextTestRunner(verbosity=2).run(firstSuite)
    unittest.TextTestRunner(verbosity=2).run(secondSuite)