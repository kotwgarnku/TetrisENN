
class Genome:
    _genome_ID = 0

    def __init__(self):
        pass

    def mutate(self):
        pass

    def mate(self):
        pass

    def set_genome(self, config):
        pass


class NodeGene:
    def __init__(self):
        self.node_number = -1
        self.node_type = None


class ConnectionGene:
    _innovation_number = 0

    def _get_innovation_number(self):
        ConnectionGene._innovation_number += 1
        return ConnectionGene._innovation_number - 1

    def __init__(self, input_node = None, output_node = None, weight = 1, enabled = False):
        self.input_node = input_node
        self.output_node = output_node
        self.weight = None
        self.enabled = False
        self.innovation_number = self._get_innovation_number()