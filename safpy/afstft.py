import numpy as np

from ._safpy import ffi, lib


class AfSTFT():
    def __init__(self, num_ch_in, num_ch_out, hopsize, HYBRIDMODE=True,
                 LOWDELAYMODE=False):
        # need to call constructor of afstft
        afstft_format = 0
        # let the compiler fill in the rest
        handle_ptr = ffi.new("void ** const")
        lib.afSTFT_create(handle_ptr,
                          num_ch_in, num_ch_out, hopsize,
                          LOWDELAYMODE, HYBRIDMODE, afstft_format)

