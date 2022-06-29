"""This will have the Python functions."""
import sys

import numpy as np

from _safpy import ffi, lib


def whoami():
    """Printing python and SAF lib version."""
    print("Python version: ", sys.version)
    print("SAF lib version: ", lib.SAF_VERSION)


def factorial(n):
    """Compute the factorial of n."""
    return np.longdouble(lib.factorial(n))
