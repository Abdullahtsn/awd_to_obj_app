from typing import IO

from pyawd.awd.types import Matrix


def decode(data: IO):
    return Matrix.decode(data, 3, 3)
