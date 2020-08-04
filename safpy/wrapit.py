"""This will have the Python functions."""
import sys
from ._safpy import ffi, lib


import numpy as np


def whoami():
    """Pure Python function."""
    print(sys.version)


def factorial(n):
    return np.longdouble(lib.factorial(n))


def getSHreal(order, dirs_deg):
    """
    

    Parameters
    ----------
    order : TYPE
        DESCRIPTION.
    dirs_deg : TYPE
        DESCRIPTION.

    Returns
    -------
    Y : TYPE
        DESCRIPTION.

    """
    order = int(order)
    dirs_deg = np.atleast_2d(dirs_deg)
    dirs_deg = np.ascontiguousarray(dirs_deg, dtype=np.float32)
    nDirs = np.shape(dirs_deg)[0]
    Y = np.zeros(((order+1)**2, nDirs), dtype=np.float32)
    Y_ptr = ffi.cast("float *", ffi.from_buffer(Y))  # out pointer
    lib.getSHreal(order, ffi.cast("float *", ffi.from_buffer(dirs_deg)),
                  nDirs, Y_ptr)
    return Y


def getSHcomplex(order, dirs_deg):
    order = int(order)
    dirs_deg = np.atleast_2d(dirs_deg)
    dirs_deg = np.ascontiguousarray(dirs_deg, dtype=np.float32)
    nDirs = np.shape(dirs_deg)[0]
    Y = np.zeros(((order+1)**2, nDirs), dtype=np.complex64)
    Y_ptr = ffi.cast("float_complex *", ffi.from_buffer(Y))  # out pointer
    lib.getSHcomplex(order, ffi.cast("float *", ffi.from_buffer(dirs_deg)),
                     nDirs, Y_ptr)
    return Y