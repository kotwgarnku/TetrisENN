from evolution.util import sort_connections_by_innovation_number

class Genome:
    """
    Class representing genome in NEAT.
    """
    _genome_ID = 0

    def __init__(self, connections, input_size, output_size):
        """
        Create genome from given informations.
        :param connections: List of tuples representing connection genes. [(source, destination, weight, enabled),...].
        Connections must be unique and there can not be any loops.
            source(integer) - ID of source node
            destination(integer) - ID of destination node
            weight(float) - weight of the connection
            enabled(boolean) - flag telling if the connection is enabled or not
        :param input_size: (Integer) - How many input nodes are in the genome. Input nodes will be assigned ID's from
            1 to N where N is input_size(for example for input_size 3, there will be 3 input nodes with IDs 1, 2 and 3)
            IMPORTANT: input nodes are indexed from 1 (Matlab masterrace or something)
        :param output_size: (Integer) - How many output nodes are in the genome. Output nodes will be assigned ID's from
            input_size + 1 to input_size + 1 + N where N is output_size
            (for example for input_size 3 and output size 4, there will be 3 input nodes with IDs 1, 2 and 3 and
            4 output nodes with IDs 4, 5, 6 and 7)
        """
        self.node_genes = {}
        self.connection_genes = {}

        self._create_connection_genes(connections)
        self._set_up_node_genes_types(input_size, output_size)

    def _create_connection_genes(self, connections):
        for connection in connections:
            if len(connection) != 4:
                raise Exception('Connection does not contain all necessary information')

            source_node_id, dest_node_id, weight, enabled = connection
            self._check_nodes(source_node_id, dest_node_id)

            source_node = self.node_genes.get(source_node_id)
            dest_node = self.node_genes.get(dest_node_id)

            if source_node is None:
                source_node = self._create_new_node(source_node_id)
            if dest_node is None:
                dest_node = self._create_new_node(dest_node_id)

            self._check_connections_uniqueness(source_node, dest_node)
            self.connection_genes[(source_node.node_id, dest_node.node_id)] = ConnectionGene(source_node, dest_node,
                                                                                             weight, enabled)

    def _set_up_node_genes_types(self, input_size, output_size):
        for index in range(1, input_size + 1):
            self.node_genes[index].node_type = 'input'
        for index in range(len(self.node_genes) - output_size + 1, len(self.node_genes) + 1):
            self.node_genes[index].node_type = 'output'

    def _check_nodes(self, source_node_id, dest_node_id):
        if source_node_id is None and dest_node_id is None:
            raise Exception("Both nodes are empty")

        if source_node_id is None or dest_node_id is None:
            raise Exception('One node is empty')

        if source_node_id == dest_node_id:
            raise Exception('ID\'s are equal')

    def _check_connections_uniqueness(self, source_node, dest_node):
        if (source_node.node_id, dest_node.node_id) in self.connection_genes:
            raise Exception('Connections must be unique')

    def _create_new_node(self, node_id):
        self.node_genes[node_id] = NodeGene(node_id=node_id)
        return self.node_genes[node_id]

    def get_connections_ids(self):
        """
        Returns unordered list of tuples representing connection IDs( [(x, y),...] where
                                                                                x - source noce ID(Integer),
                                                                                y - destination node ID(Integer)
        """
        return [(s_id, d_id) for s_id, d_id in self.connection_genes.keys()]

    def get_connections(self):
        """
        Returns unordered list of tuples representing connections( [(x, y, w, e)] where
                                                                            x - source node ID(Integer),
                                                                            y - destination node ID(Integer),
                                                                            w - weight of connection(float),
                                                                            e - flag if connection is enabled(boolean)
        """
        return [connection.get_connection() for connection in self.connection_genes.values()]

    def get_nodes(self):
        """
        Returns ordered (by NodeGene ID) list of NodeGene objects that are in the genome.
        """
        return [node for (key, node) in sorted(self.node_genes.items())]

    def mutate(self):
        """
        Mutates genome. Currently mutation can add a connection, split connection in two and add a node,
        disable connection(make sure not to disable all connections of any of the output nodes)
        and change connection weight.
        """
        pass

    def mate(self, partner):
        """
        Returns offspring of mating this genome with a partner.
        :param partner:(Genome) Genome object to mate with
        """
        connections_a = sort_connections_by_innovation_number(self.connection_genes)
        connections_b = sort_connections_by_innovation_number(partner.connection_genes)
        #TODO rest of this


class NodeGene:
    """This class may actually be kinda redundant but OOP is OOP"""
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
        self.innovation_number = self._get_new_innovation_number()

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


