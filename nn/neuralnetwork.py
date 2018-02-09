from nn.neuron import Neuron


class NeuralNetwork:
    def __init__(self, genome=None):
        self._genome = genome
        self._neurons = {}
        self._input_neurons = {}
        self._output_neurons = {}
        self._connections = {}
        self._input_size = 0
        self._output_size = 0

        if genome is not None:
            self.generate_network(genome)

    def generate_network(self, genome):
        """
        Generates neural network based on given genome.
        :param genome: (Genome) - genome containing all informations
        :return:
        """
        self._clean_network()

        self._genome = genome
        self._input_size = genome.input_size
        self._output_size = genome.output_size
        connections = genome.get_connections()

        for (source, destination, weight, enabled) in connections:
            if source not in self._neurons:
                self._neurons[source] = Neuron()
            if destination not in self._neurons:
                self._neurons[destination] = Neuron()
            if enabled:
                self._connections[(source, destination)] = weight
                self._neurons[destination].incoming_connections.append((source, weight, enabled))

        # first self._input_size neurons are input neurons
        self._input_neurons = {key: value for (key, value) in self._neurons.items() if key <= self._input_size}
        # after them are output neurons
        self._output_neurons = {key: value for (key, value) in self._neurons.items() if key > self._input_size}



    def forward(self, X):
        """
        Returns value of neural network output after forward propagation.
        :param X: Vector of inputs
        """
        self._reset_neurons()
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

    def _clean_network(self):
        self._neurons = {}
        self._input_neurons = {}
        self._output_neurons = {}
        self._connections = {}
        self._input_size = 0
        self._output_size = 0

    def _reset_neurons(self):
        for neuron in self._neurons.values():
            neuron.reset()

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
