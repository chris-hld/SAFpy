import numpy as np

from ._safpy import ffi, lib


def AfSTFT():
    def __init__(self, num_ch_in, num_ch_out, hopsize, HYBRIDMODE=True,
                 LOWDELAYMODE=False):
        # need to call constructor of afstft
        afstft_format = ffi.new("AFSTFT_FDDATA_FORMAT", 0)

