def sort_connections_by_innovation_number(connections):
    return sorted(connections.values(), key=lambda connection: connection.innovation_number)


def count_disjoint_connection_genes(connections_a, connections_b):
    """
    Counts disjoint genes of two lists of connections.
    :type connections_b: list(ConnectionGene)
    :type connections_a: list(ConnectionGene)
    :return: number of disjoint connection genes
    """
    innovations_a = [c.innovation_number for c in connections_a]
    innovations_b = [c.innovation_number for c in connections_b]

    max_innov_a = max(innovations_a)
    max_innov_b = max(innovations_b)

    # obtain the common max innovation number
    common_max_innov = min(max_innov_a, max_innov_b)

    # get innovation numbers present only in either a or b's innovation numbers
    innovations_xor = set(innovations_a) ^ set(innovations_b)

    # count innovation_xor elements which are LE than common max innovation number
    # (greater innovation numbers are excess connections)
    return sum(1 for i in innovations_xor if i <= common_max_innov)


def count_excess_connection_genes(connections_a, connections_b):
    """
    Counts excess genes of two lists of connections.
    :type connections_a: list(ConnectionGene)
    :type connections_b: list(ConnectionGene)
    :return: number of excess connection genes
    """
    innovations_a = [c.innovation_number for c in connections_a]
    innovations_b = [c.innovation_number for c in connections_b]

    max_innov_a = max(innovations_a)
    max_innov_b = max(innovations_b)

    # obtain the common max innovation number
    common_max_innov = min(max_innov_a, max_innov_b)

    # get innovation numbers present only in either a or b's innovation numbers
    innovations_xor = set(innovations_a) ^ set(innovations_b)

    # count innovation_xor elements which are greater than common max innovation number
    # (LE innovation numbers are disjoint connections)
    return sum(1 for i in innovations_xor if i > common_max_innov)


def count_avg_weight_difference(connections_a, connections_b):
    """
    Counts average weight difference between corresponding genes with the same innovation number.
    :type connections_a: list(ConnectionGene)
    :type connections_b: list(ConnectionGene)
    :return: average weight difference
    """
    weight_differences = [abs(a.weight - b.weight)
                          for a in connections_a
                          for b in connections_b
                          if a.innovation_number is b.innovation_number]
    return sum(weight_differences) / float(len(weight_differences))
