import tempfile
from pathlib import Path

import aircopy.io as io


def test_write_docs_to_yaml():
    dct = {'k1': ['v11', 'v12'], 'k2': 'v2'}
    with tempfile.TemporaryDirectory() as d:
        filename = Path(d).joinpath('test.yaml')
        io.write_docs_to_yaml(str(filename), dct)
        with filename.open('r') as f:
            assert f.read() == "k1:\n  - v11\n  - v12\nk2: v2\n"
