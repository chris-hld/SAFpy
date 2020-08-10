"""This will have the Python functions."""
import sys

import numpy as np

from ._safpy import ffi, lib


def whoami():
    """Pure Python function."""
    print(sys.version)


def factorial(n):
    return np.longdouble(lib.factorial(n))
