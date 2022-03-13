from uuid import uuid4


def get_new_node_identifier():
    return str(uuid4()).replace('-', '')
