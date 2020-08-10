import numpy as np

from ._safpy import ffi, lib


class AfSTFT():
    """."""

    def __init__(self, num_ch_in, num_ch_out, hopsize, HYBRIDMODE=True,
                 LOWDELAYMODE=False):
        """
        Call Constructor.

        Parameters
        ----------
        num_ch_in : TYPE
            DESCRIPTION.
        num_ch_out : TYPE
            DESCRIPTION.
        hopsize : TYPE
            DESCRIPTION.
        HYBRIDMODE : TYPE, optional
            DESCRIPTION. The default is True.
        LOWDELAYMODE : TYPE, optional
            DESCRIPTION. The default is False.

        Returns
        -------
        None.

        """
        # need to call constructor of afstft
        afstft_format = 0  # < nBands x nChannels x nTimeHops
        # let the compiler fill in the rest...

        afstft_handle = ffi.new("void ** const")

        lib.afSTFT_create(afstft_handle,
                          num_ch_in, num_ch_out, hopsize,
                          LOWDELAYMODE, HYBRIDMODE, afstft_format)
        self._afstft_handle = afstft_handle  # keep alive
        print(f"Created AFSTFT instance at {self._afstft_handle[0]}")

    def __del__(self):
        """
        Call Destructor.

        Returns
        -------
        None.

        """
        print(f"Destroying AFSTFT instance at {self._afstft_handle[0]}")
        lib.afSTFT_destroy(self._afstft_handle)
