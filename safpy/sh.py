import numpy as np

from _safpy import ffi, lib


def getSHreal(order, dirs):
    """
    

    Parameters
    ----------
    order : TYPE
        DESCRIPTION.
    dirs : TYPE
        dirs in rad, azi, zen.

    Returns
    -------
    Y : TYPE
        ((order+1)**2, nDirs).

    """
    order = int(order)
    dirs = np.atleast_2d(dirs)
    dirs = np.ascontiguousarray(dirs, dtype=np.float32)
    nDirs = np.shape(dirs)[0]
    Y = np.zeros(((order+1)**2, nDirs), dtype=np.float32)
    lib.getSHreal(order, ffi.from_buffer("float *", dirs),
                  nDirs, ffi.from_buffer("float *", Y))
    return Y


def getSHreal_recur(order, dirs):
    """
    

    Parameters
    ----------
    order : TYPE
        DESCRIPTION.
    dirs : TYPE
        dirs in rad, azi, zen.

    Returns
    -------
    Y : TYPE
        ((order+1)**2, nDirs).

    """
    order = int(order)
    dirs = np.atleast_2d(dirs)
    dirs = np.ascontiguousarray(dirs, dtype=np.float32)
    nDirs = np.shape(dirs)[0]
    Y = np.zeros(((order+1)**2, nDirs), dtype=np.float32)
    lib.getSHreal_recur(order, ffi.from_buffer("float *", dirs),
                        nDirs, ffi.from_buffer("float *", Y))
    return Y


def getSHcomplex(order, dirs):
    """
    

    Parameters
    ----------
    order : TYPE
        DESCRIPTION.
    dirs : TYPE
        dirs in rad, azi, zen.

    Returns
    -------
    Y : TYPE
        ((order+1)**2, nDirs).

    """
    order = int(order)
    dirs = np.atleast_2d(dirs)
    dirs = np.ascontiguousarray(dirs, dtype=np.float32)
    assert(np.shape(dirs)[1] == 2)
    nDirs = np.shape(dirs)[0]
    Y = np.zeros(((order+1)**2, nDirs), dtype=np.complex64)
    lib.getSHcomplex(order, ffi.from_buffer("float *", dirs),
                     nDirs, ffi.from_buffer("float_complex *", Y))
    return Y
