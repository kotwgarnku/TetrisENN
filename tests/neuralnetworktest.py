import unittest
from nn.neuralnetwork import NeuralNetwork
from nn.neuron import Neuron


class GenomeMock:
    def __init__(self, connections, input_size, output_size):
        self.connections = connections
        self.input_size = input_size
        self.output_size = output_size

    def get_connections(self):
        return sorted(self.connections)


class NeuronTestCase(unittest.TestCase):
    def setUp(self):
        self.test_neuron = Neuron()

    def test_activation_function(self):
        self.test_neuron.take_input_signal(2.34)
        self.assertAlmostEqual(self.test_neuron.fire(), 0.9999895197)

        self.test_neuron.take_input_signal(-2.34)
        self.assertEqual(self.test_neuron.fire(), 0.5)

        self.test_neuron.take_input_signal(0.002)
        self.test_neuron.take_input_signal(0.03)
        self.assertAlmostEqual(self.test_neuron.fire(), 0.5391199)

        self.test_neuron.take_input_signal(0.2)
        self.assertAlmostEqual(self.test_neuron.fire(), 0.757092, places=6)

        self.test_neuron.take_input_signal(-10)
        self.assertAlmostEqual(self.test_neuron.fire(), 0)

    def test_connections_creation(self):
        genome = GenomeMock([(2, 4, 0, True), (1, 3, -3, True), (2, 3, 4, True), (1, 4, 22, True)], 2, 2)
        nn = NeuralNetwork()
        nn.generate_network(genome)
        self.assertEqual(nn._connections, {(2, 4): 0, (1, 3): -3, (2, 3): 4, (1, 4): 22})

    def test_node_creation(self):
        genome = GenomeMock([(2, 4, 0, True), (1, 3, -3, True), (2, 3, 4, True), (1, 4, 22, True), (1, 5, 3, True)], 2, 2)
        nn = NeuralNetwork()
        nn.generate_network(genome)
        self.assertEqual(1 in nn._neurons, True)
        self.assertEqual(2 in nn._neurons, True)
        self.assertEqual(3 in nn._neurons, True)
        self.assertEqual(4 in nn._neurons, True)
        self.assertEqual(5 in nn._neurons, True)
        self.assertEqual(1 in nn._input_neurons, True)
        self.assertEqual(2 in nn._input_neurons, True)
        self.assertEqual(3 in nn._input_neurons, False)
        self.assertEqual(4 in nn._input_neurons, False)
        self.assertEqual(5 in nn._input_neurons, False)
        self.assertEqual(1 in nn._output_neurons, False)
        self.assertEqual(2 in nn._output_neurons, False)
        self.assertEqual(3 in nn._output_neurons, True)
        self.assertEqual(4 in nn._output_neurons, True)
        self.assertEqual(5 in nn._output_neurons, False)

    def test_connections(self):
        genome = GenomeMock([(2, 4, 0, True), (1, 3, 0, True), (2, 3, 0, True), (1, 4, 0, True)], 2, 2)
        nn = NeuralNetwork()
        nn.generate_network(genome)
        self.assertEqual(nn._genome.get_connections(), [(1, 3, 0, True), (1, 4, 0, True), (2, 3, 0, True), (2, 4, 0, True)])

    def test_input_length_exception(self):
        genome = GenomeMock([(2, 4, 0, True), (1, 3, 0, True), (2, 3, 0, True), (1, 4, 0, True)], 2, 2)
        nn = NeuralNetwork()
        nn.generate_network(genome)
        with self.assertRaises(Exception) as e:
            nn.forward([1])
        self.assertEqual(str(e.exception), "Expected 2 inputs, got 1 instead")

    def test_input_neurons_have_input_signal(self):
        genome = GenomeMock([(2, 4, 0, True), (1, 3, 0, True), (2, 3, 0, True), (1, 4, 0, True)], 2, 2)
        nn = NeuralNetwork()
        nn.generate_network(genome)
        nn.forward([3, 22])
        self.assertEqual(nn._input_neurons[1]._input_signals, [3])
        self.assertEqual(nn._input_neurons[2]._input_signals, [22])

    def test_easy_forward_propagation(self):
        genome = GenomeMock([(2, 4, 0, True), (1, 3, 0, True), (2, 3, 0, True), (1, 4, 0, True)], 2, 2)
        nn = NeuralNetwork()
        nn.generate_network(genome)
        y = nn.forward([3, 22])
        self.assertEqual(len(y), 2)
        self.assertEqual(y, [0.5, 0.5])

        genome = GenomeMock([(2, 4, 1, True), (1, 3, 0, True), (2, 3, 0, True), (1, 4, 0, True)], 2, 2)
        nn.generate_network(genome)
        y = nn.forward([3, 22])
        self.assertEqual(y[0], 0.5)
        self.assertAlmostEqual(y[1], 0.9926085)

        genome = GenomeMock([(2, 4, 1, True), (1, 3, 0, True), (2, 3, 0, True), (1, 4, -2, True)], 2, 2)
        nn.generate_network(genome)
        y = nn.forward([3, 22])
        self.assertEqual(y[0], 0.5)
        self.assertAlmostEqual(y[1], 0.00739157)

        genome = GenomeMock([(2, 4, 1, True), (1, 3, 0, False), (2, 3, 0, False), (1, 4, -2, True)], 2, 2)
        nn.generate_network(genome)
        y = nn.forward([3, 22])
        self.assertEqual(y[0], 0.5)
        self.assertAlmostEqual(y[1], 0.00739157)

    def test_hard_forward_propagation(self):
        genome = GenomeMock([(1, 5, 3, True), (2, 5, -2, True), (1, 6, -1, True), (5, 6, -3.4, True), (3, 6, 4, True),
                             (6, 4, 5, True)], 3, 1)
        nn = NeuralNetwork()
        nn.generate_network(genome)
        y = nn.forward([0.2, 2, -0.02])
        self.assertAlmostEqual(y[0], 0.5144, places=4)

        genome = GenomeMock([(1, 5, 3, True), (2, 5, -2, True), (1, 7, -1, True), (5, 7, -3.4, True), (3, 7, 4, True),
                             (7, 6, 2, True), (6, 4, 0.3, True)], 3, 1)
        nn.generate_network(genome)
        y = nn.forward([0.2, 2, -0.02])
        self.assertAlmostEqual(y[0], 0.6778, places=4)


if __name__ == '__main__':
    unittest.main()
