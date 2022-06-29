"""Docstring VBAP."""

import numpy as np

from _safpy import ffi, lib


def generateVBAPgainTable3D(ls_dirs_deg, az_res_deg, el_res_deg,
                            omitLargeTriangles=False, enableDummies=False,
                            spread=0.):
    """
    generateVBAPgainTable3D.

    Parameters
    ----------
    ls_dirs_deg : TYPE
        DESCRIPTION.
    az_res_deg : TYPE
        DESCRIPTION.
    el_res_deg : TYPE
        DESCRIPTION.
    omitLargeTriangles : TYPE, optional
        DESCRIPTION. The default is False.
    enableDummies : TYPE, optional
        DESCRIPTION. The default is False.
    spread : TYPE, optional
        DESCRIPTION. The default is 0..

    Returns
    -------
    gtable : TYPE
        DESCRIPTION.

    """
    ls_dirs_deg = np.ascontiguousarray(np.atleast_2d(ls_dirs_deg),
                                       dtype=np.float32)
    assert(np.shape(ls_dirs_deg)[1] == 2)
    num_ls = np.shape(ls_dirs_deg)[0]

    # let the compiler handle this
    # az_res_deg = int(az_res_deg)
    # el_res_deg = int(el_res_deg)
    # omitLargeTriangles = int(omitLargeTriangles)
    # enableDummies = int(enableDummies)
    # spread = float(spread)

    gtable_ptr = ffi.new("float **")
    num_gtable_out_ptr = ffi.new("int *")
    num_triangles_ptr = ffi.new("int *")

    lib.generateVBAPgainTable3D(ffi.from_buffer("float []", ls_dirs_deg),
                                num_ls,
                                az_res_deg,
                                el_res_deg,
                                omitLargeTriangles,
                                enableDummies,
                                spread,
                                gtable_ptr,
                                num_gtable_out_ptr,
                                num_triangles_ptr
                                )
    num_gtable = num_gtable_out_ptr[0]
    # num_triangles = num_triangles_ptr[0]

    gtable = np.reshape(np.array(ffi.unpack(gtable_ptr[0],
                                            num_ls*num_gtable),
                                 dtype=np.float32, ndmin=2),
                        (num_gtable, num_ls))
    return gtable
