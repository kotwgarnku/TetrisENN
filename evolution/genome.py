
class Genome:
    _genome_ID = 0

    def __init__(self, connections):
        self.node_genes = {}
        self.connection_genes = {}

        for connection in connections:
            if len(connection) != 4:
                raise Exception('Connaction does not contain all necessary informations')

            source_node = self._find_node(connection[0])
            dest_node = self._find_node(connection[1])
            if source_node is None:
                source_node = self._create_new_node(connection[0])
            if dest_node is None:
                dest_node = self._create_new_node(connection[1])

            weight = connection[2]
            enabled = connection[3]

            if (source_node.node_id, dest_node.node_id) in self.connection_genes:
                raise Exception('Connections must be unique')
            else:
                self.connection_genes[(source_node.node_id, dest_node.node_id)] = ConnectionGene(source_node, dest_node,
                                                                                                 weight, enabled)

    def _find_node(self, node_gene_id):
        if node_gene_id in self.node_genes:
            return self.node_genes[node_gene_id]
        else:
            return None

    def _create_new_node(self, node_id):
        self.node_genes[node_id] = NodeGene(node_id=node_id)
        return self.node_genes[node_id]


    def mutate(self):
        pass

    def mate(self):
        pass

    def set_genome(self, config):
        pass


class NodeGene:
    def __init__(self, node_id=-1, node_type='hidden'):
        self.node_id = node_id
        self.node_type = node_type


class ConnectionGene:
    _innovation_number = 0

    def __init__(self, source_node=None, destination_node=None, weight=1, enabled=False):
        self.source_node = source_node
        self.destination_node = destination_node
        self._check_connection_vialability()
        self.weight = weight
        self.enabled = enabled
        self.innovation_number = self._get_innovation_number()

    def _check_connection_vialability(self):
        if self.source_node is None or self.destination_node is None:
            raise Exception('One node is empty')

    def get_connection(self):
        return self.source_node.node_id, self.destination_node.node_id, self.weight, self.enabled

    @staticmethod
    def _get_innovation_number():
        ConnectionGene._innovation_number += 1
        return ConnectionGene._innovation_number - 1