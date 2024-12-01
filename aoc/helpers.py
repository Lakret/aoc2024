from os import path
from collections.abc import Callable


def read_test_input(day: str, parser: Callable[[str], any] = None) -> any:
    """
    Reads file with the filename `day` in the test inputs folder and optionally
    calls a `parser` on the results. If `parser` is not specified, returns the read file contents.
    """
    return _reader("test_inputs", day, parser=parser)


def read_input(day: str, parser: Callable[[str], any] = None) -> any:
    """Same as `read_test_input`, but uses files from the inputs folder."""
    return _reader("inputs", day, parser=parser)


def _reader(folder: str, day: str, parser: Callable[[str], any] = None) -> any:
    with open(path.join(folder, day)) as f:
        input = f.read()

        if parser:
            return parser(input)
        else:
            return input
