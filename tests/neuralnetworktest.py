import unittest
from nn.neuralnetwork import Neuron, NeuralNetwork


class GenomeMock:
    def __init__(self, connections):
        self.connections = connections

    def get_connections(self):
        return self.connections


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
        genome = GenomeMock([(2, 4, 0, True), (1, 3, -3, True), (2, 3, 4, True), (1, 4, 22, True)])
        nn = NeuralNetwork()
        nn.generate_network(genome, 2, 2)
        self.assertEqual(nn._connections,{(2, 4): 0, (1, 3): -3, (2, 3): 4, (1, 4): 22})

    def test_node_creation(self):
        genome = GenomeMock([(2, 4, 0, True), (1, 3, -3, True), (2, 3, 4, True), (1, 4, 22, True), (1, 5, 3, True)])
        nn = NeuralNetwork()
        nn.generate_network(genome, 2, 2)
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

    def test_conections(self):
        genome = GenomeMock([(2, 4, 0, True), (1, 3, 0, True), (2, 3, 0, True), (1, 4, 0, True)])
        nn = NeuralNetwork()
        nn.generate_network(genome, 2, 2)
        self.assertEqual(nn.connectionss, [(1, 3, 0, True), (1, 4, 0, True), (2, 3, 0, True), (2, 4, 0, True)])

    def test_input_length_exception(self):
        genome = GenomeMock([(2, 4, 0, True), (1, 3, 0, True), (2, 3, 0, True), (1, 4, 0, True)])
        nn = NeuralNetwork()
        nn.generate_network(genome, 2, 2)
        with self.assertRaises(Exception) as e:
            nn.forward([1])
        self.assertEqual(str(e.exception), "Expected 2 inputs, got 1 instead")


if __name__ == '__main__':
    unittest.main()
