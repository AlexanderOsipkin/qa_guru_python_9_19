from pathlib import Path


def schema_dir(schema_name):
    return str(Path(__file__).parent.joinpath(f'schemas/{schema_name}'))
