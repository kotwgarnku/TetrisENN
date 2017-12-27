import numpy as np


class NeuralNetwork:
    def __init__(self):
        self._connections = {}
        self._neurons = {}
        self._input_size = 0
        self._output_size = 0
        self._input_neurons = {}
        self._output_neurons = {}

    def generate_network(self, genome, input_size, output_size):
        self._input_size = input_size
        self._output_size = output_size
        self.connectionss = sorted(genome.get_connections())
        connections = sorted(genome.get_connections())
        for source, destination, weight, enabled in connections:
            if source not in self._neurons:
                self._neurons[source] = Neuron()
            if destination not in self._neurons:
                self._neurons[destination] = Neuron()
            if enabled:
                self._connections[(source, destination)] = weight

        for index in range(1, input_size + 1):
            self._input_neurons[index] = self._neurons[index]

        for index in range(input_size + 1, len(self._neurons)):
            self._output_neurons[index] = self._neurons[index]

    def forward(self, input=[]):
        if(len(input) != self._input_size):
            raise Exception("Expected {!s} inputs, got {!s} instead".format(self._input_size, len(input)))
        connections = sorted(self._connections)



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
