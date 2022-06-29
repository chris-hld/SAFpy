import numpy as np

from _safpy import ffi, lib


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
    lib.getSHreal(order, ffi.from_buffer("float *", dirs_deg),
                  nDirs, ffi.from_buffer("float *", Y))
    return Y


def getSHcomplex(order, dirs_deg):
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
    assert(np.shape(dirs_deg)[1] == 2)
    nDirs = np.shape(dirs_deg)[0]
    Y = np.zeros(((order+1)**2, nDirs), dtype=np.complex64)
    lib.getSHcomplex(order, ffi.from_buffer("float *", dirs_deg),
                     nDirs, ffi.from_buffer("float_complex *", Y))
    return Y
