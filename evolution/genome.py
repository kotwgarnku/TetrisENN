from evolution.util import sort_connections_by_innovation_number
import random


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
        self.input_size = input_size
        self.output_size = output_size
        self.input_node_ids = []
        self.output_node_ids = []

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
            self.input_node_ids.append(index)
        for index in range(len(self.node_genes) - output_size + 1, len(self.node_genes) + 1):
            self.node_genes[index].node_type = 'output'
            self.output_node_ids.append(index)

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
        return sorted([(s_id, d_id) for s_id, d_id in self.connection_genes.keys()])

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

    def mutate(self, coefficients):
        """
        Mutates genome. Mutation can:
        1. add a connection,
        2. add a node (4 -> 5 ==> 4 -> 9 -> 5),
        3. change connection weight.
        """
        uniform_value = random.uniform(0.0, 1.0)

        # each coefficient represent probability between [0;1]
        if uniform_value <= coefficients['add_connection']:
            self._mutate_new_connection(coefficients['max_weight_mutation'])

        if uniform_value <= coefficients['split_connection']:
            self._mutate_split_connection()

        if uniform_value <= coefficients['change_weight']:
            self._mutate_change_weight(coefficients['max_weight_mutation'])

    def _mutate_new_connection(self, max_weight):
        # build lists of possible indexes
        possible_source_indexes = [idx for idx in range(1, len(self.node_genes) + 1)
                                   if idx not in self.output_node_ids]
        possible_destination_indexes = [idx for idx in range(1, len(self.node_genes) + 1)
                                        if idx not in self.input_node_ids]

        # produce every possible connection not already in connection_genes
        possible_connections = [(s, d)
                                for s in possible_source_indexes
                                for d in possible_destination_indexes
                                if (s, d) not in self.connection_genes]

        # if no new connection possible, end mutation
        if not possible_connections:
            return

        # choose random new connection
        new_connection = random.choice(possible_connections)

        # get connection parameters
        source_id = new_connection[0]
        destination_id = new_connection[1]
        weight = random.uniform(0.0, max_weight)
        enable = True

        # create new connection
        self.connection_genes[(source_id, destination_id)] = ConnectionGene(source_id, destination_id, weight, enable)

    def _mutate_split_connection(self):
        connection = self._get_random_enabled_connection()

        if not connection:
            return

        # disable this connection
        connection.enabled = False

        # get old connection parameters
        (old_source_id, old_destination_id, old_weight, old_enabled) = connection.get_connection()
        old_source_node = self.node_genes[old_source_id]
        old_destination_node = self.node_genes[old_destination_id]

        # create new node
        new_node_id = len(self.node_genes) + 1
        new_node = self._create_new_node(new_node_id)

        # create connection source -> new_node
        first_connection_weight = 1.0
        first_connection_enabled = True
        self.connection_genes[(old_source_id, new_node_id)] = ConnectionGene(old_source_node, new_node,
                                                                             first_connection_weight,
                                                                             first_connection_enabled)

        # create connection new_node -> destination
        second_connection_weight = old_weight
        second_connection_enabled = True
        self.connection_genes[(new_node_id, old_destination_id)] = ConnectionGene(new_node, old_destination_node,
                                                                                  second_connection_weight,
                                                                                  second_connection_enabled)

    def _get_random_enabled_connection(self):
        # build enabled connection pool
        enabled_connections = [c for key, c in self.connection_genes.items() if c.enabled]

        if not enabled_connections:
            return None

        # choose connection to split
        return random.choice(enabled_connections)

    def _mutate_change_weight(self, max_weight_change):
        connection = self._get_random_enabled_connection()

        if not connection:
            return

        # generate new weight by adding value from N(0, MAX/2) -> chance for value exceeding MAX is ~2%
        # chance for value exceeding MAX twice is 0.003%
        connection.weight = connection.weight + random.normalvariate(mu=0.0, sigma=max_weight_change/2)

    def mate(self, partner):
        """
        Returns offspring of mating this genome with a partner.
        :param partner:(Genome) Genome object to mate with
        """
        connections_a = sort_connections_by_innovation_number(self.connection_genes)
        connections_b = sort_connections_by_innovation_number(partner.connection_genes)
        # TODO rest of this


class NodeGene:
    """This class may actually be kinda redundant but OOP is OOP"""

    def __init__(self, node_id=-1, node_type='hidden'):
        self.node_id = node_id
        self.node_type = node_type


class ConnectionGene:
    _innovation_number = 0

    def __init__(self, source_node=None, destination_node=None, weight=1.0, enabled=False):
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
