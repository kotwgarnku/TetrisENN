import evolution.util
import random
import copy
import json


class Genome:
    """
    Class representing genome in NEAT.
    """

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
        self.fitness = None
        self.adjusted_fitness = None

        # standard creation of new genome
        if len(connections[0]) == 4:
            self._create_connection_genes(connections)

        # creation used during reproduction
        elif len(connections[0]) == 5:
            self._create_connection_genes_with_innovation_numbers(connections)

        else:
            raise Exception('Connection does not contain all necessary information')

        self._set_up_node_genes_types(input_size, output_size)

    def _create_connection_genes(self, connections):
        for connection in connections:
            source_node_id, dest_node_id, weight, enabled = connection
            self._check_nodes(source_node_id, dest_node_id)

            source_node = self.node_genes.get(source_node_id)
            dest_node = self.node_genes.get(dest_node_id)

            if source_node is None:
                source_node = self._create_new_node(source_node_id)
            if dest_node is None:
                dest_node = self._create_new_node(dest_node_id)

            self._check_connections_uniqueness(source_node, dest_node)

            new_connection = ConnectionGene(source_node, dest_node, weight, enabled)
            self.connection_genes[(source_node_id, dest_node_id)] = new_connection

    def _create_connection_genes_with_innovation_numbers(self, connections):
        for connection in connections:
            source_node_id, dest_node_id, weight, enabled, innovation_number = connection
            self._check_nodes(source_node_id, dest_node_id)

            source_node = self.node_genes.get(source_node_id)
            dest_node = self.node_genes.get(dest_node_id)

            if source_node is None:
                source_node = self._create_new_node(source_node_id)
            if dest_node is None:
                dest_node = self._create_new_node(dest_node_id)

            self._check_connections_uniqueness(source_node, dest_node)

            new_connection = ConnectionGene(source_node, dest_node, weight, enabled, innovation_number)
            self.connection_genes[(source_node_id, dest_node_id)] = new_connection

    def _set_up_node_genes_types(self, input_size, output_size):
        for index in range(1, input_size + 1):
            self.node_genes[index].node_type = 'input'
            self.input_node_ids.append(index)
        for index in range(input_size + 1, input_size + 1 + output_size):
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

    def _create_new_node(self, node_id=None):
        if node_id is None:
            node_id = len(self.node_genes) + 1
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
        return sorted([connection.get_connection() for connection in self.connection_genes.values()])

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
        :param coefficients: dictionary with mutation coefficients
        """
        # each coefficient represent probability between [0;1]
        if random.uniform(0.0, 1.0) <= coefficients['add_connection']:
            self._mutate_new_connection(coefficients['new_connection_abs_max_weight'])

        if random.uniform(0.0, 1.0) <= coefficients['split_connection']:
            self._mutate_split_connection()

        if random.uniform(0.0, 1.0) <= coefficients['change_weight']:
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
                                if s != d and (s, d) not in self.connection_genes]

        # if no new connection possible, end mutation
        if not possible_connections:
            return

        # choose random new connection
        new_connection = random.choice(possible_connections)

        # get connection parameters
        source_id = new_connection[0]
        source_node = self.node_genes[source_id]
        destination_id = new_connection[1]
        destination_node = self.node_genes[destination_id]
        weight = random.normalvariate(mu=0.0, sigma=max_weight / 2)
        enable = True

        # create new connection
        self.connection_genes[(source_id, destination_id)] = ConnectionGene(source_node, destination_node, weight,
                                                                            enable)

    def _mutate_split_connection(self):
        connection = self._get_random_enabled_connection()

        if connection is None:
            return

        # disable this connection
        connection.enabled = False

        # get old connection parameters
        (old_source_id, old_dest_id, old_weight, _) = connection.get_connection()
        old_source_node = self.node_genes[old_source_id]
        old_dest_node = self.node_genes[old_dest_id]

        # create new node
        new_node = self._create_new_node()
        new_node_id = new_node.node_id

        # create connection source -> new_node
        first_connection = ConnectionGene(old_source_node, new_node, weight=1.0, enabled=True)
        self.connection_genes[(old_source_id, new_node_id)] = first_connection

        # create connection new_node -> destination
        second_connection = ConnectionGene(new_node, old_dest_node, weight=old_weight, enabled=True)
        self.connection_genes[(new_node_id, old_dest_id)] = second_connection

    def _get_random_enabled_connection(self):
        # build enabled connection pool
        enabled_connections = [c for key, c in self.connection_genes.items() if c.enabled]

        if not enabled_connections:
            return None

        # choose connection to split
        return random.choice(enabled_connections)

    def _mutate_change_weight(self, max_weight_change):
        connection = self._get_random_enabled_connection()

        if connection is None:
            return

        # generate new weight by adding value from N(0, MAX/2) -> chance for value exceeding MAX is ~2%
        # chance for value exceeding MAX twice is 0.003%
        connection.weight = connection.weight + random.normalvariate(mu=0.0, sigma=max_weight_change / 2)

    def compatibility_distance(self, partner, coefficients):
        """
        Returns compatibility distance between this genome and partner.
        The greater, the more the genomes differ.
        :param partner:(Genome) Genome object to mate with
        :param coefficients: dictionary with compatibility distance factors
        """
        connections_a = self.connection_genes.values()
        connections_b = partner.connection_genes.values()

        excess_number = evolution.util.count_excess_connection_genes(connections_a, connections_b)
        disjoint_number = evolution.util.count_disjoint_connection_genes(connections_a, connections_b)
        avg_weight_difference = evolution.util.count_avg_weight_difference(connections_a, connections_b)
        normalization_factor = float(max(len(connections_a), len(connections_b)))

        # "N can be set to 1 if both genomes are small, i.e. consist of fewer than 20 genes"
        if normalization_factor < 20.0:
            normalization_factor = 1.0

        excess_component = coefficients['excess_factor'] * excess_number / normalization_factor
        disjoint_component = coefficients['disjoint_factor'] * disjoint_number / normalization_factor
        weight_difference_component = coefficients['weight_difference_factor'] * avg_weight_difference

        return excess_component + disjoint_component + weight_difference_component

    @staticmethod
    def reproduce(parent1, parent2):
        """
        Produces new genome as a result of reproduction of 2 genomes.
        :type parent1: Genome
        :type parent2: Genome
        :return: new Genome, a child of parent1 and parent2
        """
        assert parent1.input_size == parent2.input_size, "parents' input_size differ"
        assert parent1.output_size == parent2.output_size, "parents' output_size differ"

        if parent1.fitness == parent2.fitness:
            return Genome._reproduce_equal_genomes(parent1, parent2)
        elif parent1.fitness > parent2.fitness:
            return Genome._reproduce_stronger_with_weaker(parent1, parent2)
        elif parent1.fitness < parent2.fitness:
            return Genome._reproduce_stronger_with_weaker(parent2, parent1)

    @staticmethod
    def _reproduce_equal_genomes(parent1, parent2):
        child_connections_with_innovs = {}

        # generate dictionaries as (innovation_number, connection)
        parent1_connections = dict((conn.innovation_number, conn) for (key, conn) in parent1.connection_genes.items())
        parent2_connections = dict((conn.innovation_number, conn) for (key, conn) in parent2.connection_genes.items())

        # get set of every innovation number existing in either collection
        innovation_numbers = set(parent1_connections.keys()).union(set(parent2_connections.keys()))

        # generate child connections with innovation numbers
        for innov in innovation_numbers:
            connection_gene = None
            if innov in parent1_connections and innov in parent2_connections:
                connection_gene = random.choice([parent1_connections[innov], parent2_connections[innov]])
            elif innov in parent1_connections:
                connection_gene = parent1_connections[innov]
            elif innov in parent2_connections:
                connection_gene = parent2_connections[innov]

            (source_id, dest_id, weight, enabled) = connection_gene.get_connection()
            connection_with_innov = (source_id, dest_id, weight, enabled, innov)
            child_connections_with_innovs[(source_id, dest_id)] = connection_with_innov

        # both parents have to have the same input and output sizes
        input_size = parent1.input_size
        output_size = parent1.output_size

        return Genome(list(child_connections_with_innovs.values()), input_size, output_size)

    @staticmethod
    def _reproduce_stronger_with_weaker(stronger, weaker):
        child_connections_with_innovs = {}

        # generate dictionaries as (innovation_number, connection)
        stronger_connections = dict((conn.innovation_number, conn) for (key, conn) in stronger.connection_genes.items())
        weaker_connections = dict((conn.innovation_number, conn) for (key, conn) in weaker.connection_genes.items())

        # generate child connections with innovation numbers
        for innov, stronger_conn in stronger_connections.items():
            if innov in weaker_connections:
                connection_gene = random.choice([stronger_conn, weaker_connections[innov]])
            else:
                connection_gene = stronger_conn

            (source_id, dest_id, weight, enabled) = connection_gene.get_connection()
            connection_with_innov = (source_id, dest_id, weight, enabled, innov)
            child_connections_with_innovs[(source_id, dest_id)] = connection_with_innov

        input_size = stronger.input_size
        output_size = stronger.output_size

        return Genome(list(child_connections_with_innovs.values()), input_size, output_size)

    def to_json(self):
        """
        Produces JSON content from this genome.
        :return: string in JSON format
        """
        genome_dict = dict(input_size=self.input_size,
                           output_size=self.output_size,
                           connections=self.get_connections())
        return json.dumps(genome_dict)

    @staticmethod
    def from_json(json_content):
        """
        Constructs new Genome from JSON formatted string.
        :param json_content: string formatted as JSON
        :return: Genome object constructed from JSON
        """
        genome_dict = json.loads(json_content)
        return Genome(genome_dict["connections"], genome_dict["input_size"], genome_dict["output_size"])


class NodeGene:
    """This class may actually be kinda redundant but OOP is OOP"""

    def __init__(self, node_id=-1, node_type='hidden'):
        self.node_id = node_id
        self.node_type = node_type


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
