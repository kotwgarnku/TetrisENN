def sort_connections_by_innovation_number(connections):
    return sorted(connections.values(), key=lambda connection: connection.innovation_number)