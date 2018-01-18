import numpy as np


class NeuralNetwork:
    def __init__(self, genome=None):
        self._genome = None
        self._connections = {}
        self._neurons = {}
        self._input_size = 0
        self._output_size = 0
        self._input_neurons = {}
        self._output_neurons = {}
        self._genome = genome

        if genome is not None:
            self.generate_network(genome)

    def generate_network(self, genome):
        """
        Generates neural network based on given genome.
        :param genome: (Genome) - genome containing all informations
        :return:
        """
        self.clean_network()
        self._genome = genome
        self._input_size = genome.input_size
        self._output_size = genome.output_size
        connections = genome.get_connections()
        for source, destination, weight, enabled in connections:
            if source not in self._neurons:
                self._neurons[source] = Neuron()
            if destination not in self._neurons:
                self._neurons[destination] = Neuron()
            if enabled:
                self._connections[(source, destination)] = weight
                self._neurons[destination].incoming_connections.append((source, weight, enabled))

        for index in range(1, self._input_size + 1):
            self._input_neurons[index] = self._neurons[index]

        for index in range(self._input_size + 1, self._input_size + self._output_size + 1):
            self._output_neurons[index] = self._neurons[index]

    def clean_network(self):
        self._connections = {}
        self._neurons = {}
        self._input_size = 0
        self._output_size = 0
        self._input_neurons = {}
        self._output_neurons = {}

    def forward(self, X):
        """
        Returns value of neural network output after forward propagation.
        :param X: Vector of inputs
        """
        self._clear_neurons()
        if len(X) != self._input_size:
            raise Exception("Expected {!s} inputs, got {!s} instead".format(self._input_size, len(X)))
        for index in range(1, self._input_size + 1):
            self._input_neurons[index].take_input_signal(X[index - 1])

        # Forward propagation with depth-first search
        self._DFS()

        # Fire output nodes
        for output_neuron in self._output_neurons.values():
            output_neuron.fire()

        # Get output signals
        y = []
        for index in range(self._input_size + 1, self._input_size + self._output_size + 1):
            y.append(self._output_neurons[index].get_output_signal())
        return y

    def _clear_neurons(self):
        for neuron in self._neurons.values():
            neuron._input_signals.clear()

    def _DFSUtil(self, v, visited):
        visited[v-1] = True

        # Go deeper into connected nodes
        for source, weight, enabled in self._neurons[v].incoming_connections:
            if visited[source-1] == False:
                self._DFSUtil(source, visited)

        # After handling all connected nodes calculate signal in this node
        for source, weight, enabled in self._neurons[v].incoming_connections:
            if enabled:
                source_id = source
                output_signal = self._neurons[source_id].fire()
                connection_value = output_signal * weight
                self._neurons[v].take_input_signal(connection_value)


    def _DFS(self):
        """
        Depth-first search
        :return:
        """
        visited = [False]*(len(self._neurons))

        # We start depth-first search with node with ID 1
        for v, index in zip(visited, range(len(visited))):
            if(v == False):
                self._DFSUtil(index + 1, visited)

    def get_genome(self):
        return self._genome

class Neuron:
    def __init__(self):
        self._input_signals = []
        self._output_signal = 0
        self.incoming_connections = []

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
