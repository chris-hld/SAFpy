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
    assert(np.shape(dirs_deg)[1] == 2)
    nDirs = np.shape(dirs_deg)[0]
    Y = np.zeros(((order+1)**2, nDirs), dtype=np.complex64)
    Y_ptr = ffi.cast("float_complex *", ffi.from_buffer(Y))  # out pointer
    lib.getSHcomplex(order, ffi.cast("float *", ffi.from_buffer(dirs_deg)),
                     nDirs, Y_ptr)
    return Y


def generateVBAPgainTable3D(ls_dirs_deg, az_res_deg, el_res_deg,
                            omitLargeTriangles=False, enableDummies=False,
                            spread=0.):
    ls_dirs_deg = np.atleast_2d(ls_dirs_deg)
    ls_dirs_deg = np.ascontiguousarray(ls_dirs_deg, dtype=np.float32)
    assert(np.shape(ls_dirs_deg)[1] == 2)
    num_dirs = np.shape(ls_dirs_deg)[0]
    az_res_deg = int(az_res_deg)
    el_res_deg = int(el_res_deg)
    omitLargeTriangles = int(omitLargeTriangles)
    enableDummies = int(enableDummies)
    spread = float(spread)

    # guess size to allocate memory, will assert later
    num_gtable = (360 // az_res_deg + 1) * (180 // el_res_deg + 1)
    gtable = np.zeros((num_gtable, num_dirs), dtype=np.float32)
    gtable_ptr = ffi.cast("float **", ffi.from_buffer(gtable))

    num_gtable_out_ptr = ffi.new("int *")
    num_triangles_ptr = ffi.new("int *")

    lib.generateVBAPgainTable3D(ffi.cast("float *",
                                         ffi.from_buffer(ls_dirs_deg)),
                                num_dirs,
                                az_res_deg,
                                el_res_deg,
                                omitLargeTriangles,
                                enableDummies,
                                spread,
                                gtable_ptr,
                                num_gtable_out_ptr,
                                num_triangles_ptr
                                )
    assert(num_gtable == num_gtable_out_ptr[0])
    return gtable
