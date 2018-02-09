class ConnectionGene:
    _innovation_number = 0

    def __init__(self, source_node=None, destination_node=None, weight=1.0, enabled=False, innovation_number=None):
        """
        :type source_node: NodeGene
        :type destination_node: NodeGene
        :type weight: float
        :type enabled: bool
        :type innovation_number: int
        """
        self.source_node = source_node
        self.destination_node = destination_node
        self._check_connection_vialability()
        self.weight = weight
        self.enabled = enabled
        if innovation_number is None:
            self.innovation_number = self._get_new_innovation_number()
        else:
            self.innovation_number = innovation_number

    def _check_connection_vialability(self):
        if self.source_node is None and self.destination_node is None:
            raise Exception("Both nodes are empty")
        if self.source_node is None or self.destination_node is None:
            raise Exception("One node is empty")

    def get_connection(self):
        return self.source_node.node_id, self.destination_node.node_id, self.weight, self.enabled

    @staticmethod
    def _get_new_innovation_number():
        ConnectionGene._innovation_number += 1
        return ConnectionGene._innovation_number - 1