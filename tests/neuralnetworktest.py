import unittest
from nn.neuralnetwork import Neuron, NeuralNetwork

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

    def test_conections(self):
        class GenomeMock:
            def __init__(self, connections):
                self.connections = connections

            def get_connections(self):
                return self.connections

        genome = GenomeMock([(2, 4, 0, True), (1, 3, 0, True), (2, 3, 0, True), (1, 4, 0, True)])
        nn = NeuralNetwork()
        nn.generate_network(genome)
        self.assertEqual(nn.connectionss, [(1, 3), (1, 4), (2, 3), (2, 4)])


if __name__ == '__main__':
    unittest.main()
