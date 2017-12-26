import numpy as np

class NeuralNetwork:
    def __init__(self):
        self._connections = {}

    def generate_network(self, genome):
        self.connectionss = sorted(genome.get_connections())
        connections = sorted(genome.get_connections())
        for source, destination, weight, enabled in connections:
            self._connections[(source, destination)] = Neuron()



    def forward(self):
        pass


class Neuron:
    def __init__(self):
        self._input_signals = []
        self._output_signal = 0

    def take_input_signal(self, input_signal):
        self._input_signals.append(input_signal)

    def fire(self):
        self._output_signal = self._activation_function(self._input_signals)
        return self._output_signal

    def get_output_signal(self):
        return self._output_signal

    @staticmethod
    def _activation_function(input_signal):
        return 1.0/(1 + np.exp(-4.9 * sum(input_signal)))
