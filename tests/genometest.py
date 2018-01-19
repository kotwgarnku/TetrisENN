import unittest

from evolution.genome import ConnectionGene, NodeGene, Genome
from evolution.util import sort_connections_by_innovation_number


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
        self.assertEqual(genome2.get_connections_ids(), [(1, 2), (1, 3), (1, 4)])

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
        self.assertEqual(nodes[2].node_type, 'output')
        self.assertEqual(nodes[2].node_id, 3)
        self.assertEqual(nodes[3].node_type, 'hidden')
        self.assertEqual(nodes[3].node_id, 4)

    def test_connections_sorting_by_innovation_number(self):
        genome = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 1)
        connections = sort_connections_by_innovation_number(genome.connection_genes)
        self.assertLess(connections[0].innovation_number, connections[1].innovation_number)
        self.assertLess(connections[1].innovation_number, connections[2].innovation_number)
        self.assertLess(connections[2].innovation_number, connections[3].innovation_number)

    def test_mutate_new_connection_to_full_genome(self):
        full_genome = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 2)
        full_genome._mutate_new_connection(1.0)
        self.assertEqual([(1, 3), (1, 4), (2, 3), (2, 4)], full_genome.get_connections_ids())

    def test_mutate_new_connection_to_not_full_genome(self):
        full_genome = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True]], 2, 2)
        full_genome._mutate_new_connection(1.0)
        self.assertEqual([(1, 3), (1, 4), (2, 3), (2, 4)], full_genome.get_connections_ids())

    def test_mutate_split_conneciton_to_genome_with_enabled_connection(self):
        genome = Genome([[1, 2, 0, True]], 1, 1)
        genome._mutate_split_connection()
        self.assertEqual([(1, 2), (1, 3), (3, 2)], genome.get_connections_ids())

    def test_mutate_split_conneciton_to_genome_with_disabled_connection(self):
        genome = Genome([[1, 2, 0, False]], 1, 1)
        genome._mutate_split_connection()
        self.assertEqual([(1, 2)], genome.get_connections_ids())

    def test_mutate_change_weight_for_genome_with_enabled_connection(self):
        weight = 0.0
        genome = Genome([[1, 2, weight, True]], 1, 1)
        genome._mutate_change_weight(1.0)
        (source_id, dest_id, new_weight, enable) = genome.get_connections()[0]
        self.assertNotAlmostEqual(weight, new_weight)

    def test_mutate_change_weight_for_genome_with_disabled_connection(self):
        weight = 0.0
        genome = Genome([[1, 2, weight, False]], 1, 1)
        genome._mutate_change_weight(1.0)
        (source_id, dest_id, new_weight, enable) = genome.get_connections()[0]
        self.assertAlmostEqual(weight, new_weight)

    def test_mutate_for_0_percent_chance_for_any_mutation(self):
        # probability for each mutation
        mutation_coefficients = dict(add_connection=0.0, split_connection=0.0, change_weight=0.0,
                                     new_connection_abs_max_weight=5.0, max_weight_mutation=5.0)
        weight = 0.0
        genome = Genome([[1, 2, weight, True]], 1, 1)
        genome.mutate(mutation_coefficients)
        # add new connection/node mutation
        self.assertEqual([(1, 2)], genome.get_connections_ids())
        # weight mutation
        (source_id, dest_id, new_weight, enable) = genome.get_connections()[0]
        self.assertAlmostEqual(weight, new_weight)

    def test_mutate_for_100_percent_chance_for_add_connection_mutation(self):
        # probability for each mutation
        mutation_coefficients = dict(add_connection=1.0, split_connection=0.0, change_weight=0.0,
                                     new_connection_abs_max_weight=5.0, max_weight_mutation=5.0)
        weight = 0.0
        genome = Genome([[1, 3, weight, True], [1, 4, weight, True], [2, 3, weight, True]], 2, 2)
        genome.mutate(mutation_coefficients)
        self.assertEqual([(1, 3), (1, 4), (2, 3), (2, 4)], genome.get_connections_ids())

    def test_mutate_for_100_percent_chance_for_split_connection_mutation(self):
        # probability for each mutation
        mutation_coefficients = dict(add_connection=0.0, split_connection=1.0, change_weight=0.0,
                                     new_connection_abs_max_weight=5.0, max_weight_mutation=5.0)
        weight = 0.0
        genome = Genome([[1, 2, weight, True]], 1, 1)
        genome.mutate(mutation_coefficients)
        # add new connection/node mutation
        self.assertEqual([(1, 2), (1, 3), (3, 2)], genome.get_connections_ids())

    def test_mutate_for_100_percent_chance_for_weight_mutation(self):
        # probability for each mutation
        mutation_coefficients = dict(add_connection=0.0, split_connection=0.0, change_weight=1.0,
                                     new_connection_abs_max_weight=5.0, max_weight_mutation=5.0)
        weight = 0.0
        genome = Genome([[1, 2, weight, True]], 1, 1)
        genome.mutate(mutation_coefficients)
        # add new connection/node mutation
        (source_id, dest_id, new_weight, enable) = genome.get_connections()[0]
        self.assertNotAlmostEqual(weight, new_weight)

    def test_reproduce_equally_fit_genomes(self):
        genome1 = Genome([[1, 3, 0, True], [2, 4, 0, True]], 2, 2)
        genome2 = Genome([[1, 4, 0, True], [2, 3, 0, True]], 2, 2)
        genome1.fitness = 1.0
        genome2.fitness = 1.0
        child = Genome.reproduce(genome1, genome2)
        self.assertEqual([(1, 3), (1, 4), (2, 3), (2, 4)], child.get_connections_ids())

    def test_reproduce_equally_fit_genomes_with_overlapping_connections(self):
        genome1 = Genome([[1, 3, 0, True], [2, 4, 0, True], [1, 4, 1, True]], 2, 2)
        # genome2 becomes independent copy of genome 1 (same invocation numbers)
        genome2 = Genome._reproduce_equal_genomes(genome1, genome1)
        # add different connection
        genome2._create_connection_genes([[2, 3, 0, True]])
        # change genome 2 (1,4) conneciton weight
        genome2.connection_genes[(1, 4)].weight = 5
        genome1.fitness = 1.0
        genome2.fitness = 1.0
        child = Genome.reproduce(genome1, genome2)
        self.assertEqual([(1, 3), (1, 4), (2, 3), (2, 4)], child.get_connections_ids())

        overlapping_connection = child.connection_genes[(1, 4)]
        weight = overlapping_connection.weight
        self.assertTrue(weight == 1 or weight == 5)

    def test_reproduce_differently_fit_genomes(self):
        genome1 = Genome([[1, 3, 0, True], [2, 4, 0, True]], 2, 2)
        genome2 = Genome([[1, 4, 0, True], [2, 3, 0, True]], 2, 2)
        genome1.fitness = 2.0
        genome2.fitness = 1.0
        child = Genome.reproduce(genome1, genome2)
        self.assertEqual([(1, 3), (2, 4)], child.get_connections_ids())

        genome1.fitness = 1.0
        genome2.fitness = 2.0
        child = Genome.reproduce(genome1, genome2)
        self.assertEqual([(1, 4), (2, 3)], child.get_connections_ids())

    def test_reproduce_differently_fit_genomes_with_overlapping_connections(self):
        genome1 = Genome([[1, 3, 0, True], [2, 4, 0, True], [1, 4, 1, True]], 2, 2)
        # genome2 becomes independent copy of genome 1 (same invocation numbers)
        genome2 = Genome._reproduce_equal_genomes(genome1, genome1)
        # add different connection
        genome2._create_connection_genes([[2, 3, 0, True]])
        # change genome 2 (1,4) connection weight
        genome2.connection_genes[(1, 4)].weight = 5
        genome1.fitness = 2.0
        genome2.fitness = 1.0
        child = Genome.reproduce(genome1, genome2)
        self.assertEqual([(1, 3), (1, 4), (2, 4)], child.get_connections_ids())

        overlapping_connection = child.connection_genes[(1, 4)]
        weight = overlapping_connection.weight
        self.assertTrue(weight == 1 or weight == 5)

        genome1.fitness = 1.0
        genome2.fitness = 2.0
        child = Genome.reproduce(genome1, genome2)
        self.assertEqual([(1, 3), (1, 4), (2, 3), (2, 4)], child.get_connections_ids())

        overlapping_connection = child.connection_genes[(1, 4)]
        weight = overlapping_connection.weight
        self.assertTrue(weight == 1 or weight == 5)

    def test_compatibility_distance(self):
        genome = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 2)
        genome2 = Genome([[1, 4, 0, True], [1, 2, 0, True], [1, 3, 0, True]], 1, 3)

        coefficients = dict(excess_factor=1.0, disjoint_factor=1.0, weight_difference_factor=1.0)
        genome.compatibility_distance(genome2, coefficients)

    def test_json_generation(self):
        genome = Genome([[1, 3, 0, True], [1, 4, 0, True], [2, 3, 0, True], [2, 4, 0, True]], 2, 2)

        genome_from_json = Genome.from_json(genome.to_json())

        self.assertEqual(genome.get_connections(), genome_from_json.get_connections())
        self.assertEqual(genome.input_size, genome_from_json.input_size)
        self.assertEqual(genome.output_size, genome_from_json.output_size)
        self.assertEqual(genome.input_node_ids, genome_from_json.input_node_ids)
        self.assertEqual(genome.output_node_ids, genome_from_json.output_node_ids)

if __name__ == '__main__':
    firstSuite = unittest.TestLoader().loadTestsFromTestCase(TestGenomeCase)
    secondSuite = unittest.TestLoader().loadTestsFromTestCase(TestConnectionGeneCase)
    unittest.TextTestRunner(verbosity=2).run(firstSuite)
    unittest.TextTestRunner(verbosity=2).run(secondSuite)
