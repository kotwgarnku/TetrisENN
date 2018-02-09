import numpy as np


class Neuron:
    def __init__(self, activation_function=None):
        self._input_signals = []
        self._output_signal = 0
        self.input_connections = []

        if activation_function is None:
            self._activation_function = Neuron.sigmoid_activation

    def fire(self):
        self._output_signal = self._activation_function(self._input_signals)
        return self._output_signal

    def take_input_signal(self, input_signal):
        self._input_signals.append(input_signal)

    def reset(self):
        self._input_signals.clear()

    def get_output_signal(self):
        return self._output_signal

    @staticmethod
    def sigmoid_activation(input_signal):
        return 1.0/(1 + np.exp(-4.9 * sum(input_signal)))