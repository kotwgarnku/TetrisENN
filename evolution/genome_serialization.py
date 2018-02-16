import json
from evolution.genome import Genome


def genome_to_json(genome):
    """
    Produces JSON content from this genome.
    :return: string in JSON format
    """
    genome_dict = dict(
        input_size=genome.input_size,
        output_size=genome.output_size,
        connections=genome.get_connections()
    )

    return json.dumps(genome_dict)


def genome_from_json(json_content):
    """
    Constructs new Genome from JSON formatted string.
    :param json_content: string formatted as JSON
    :return: Genome object constructed from JSON
    """
    genome_dict = json.loads(json_content)
    genome = Genome(genome_dict["connections"], genome_dict["input_size"], genome_dict["output_size"])

    return genome
