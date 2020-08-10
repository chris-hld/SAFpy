import numpy as np

from ._safpy import ffi, lib


class AfSTFT():
    """."""

    def __init__(self, num_ch_in, num_ch_out, hopsize, fs, HYBRIDMODE=True,
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
        fs : TYPE
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

        self._num_bands = self.get_num_bands()
        self._center_freqs = self.get_center_freqs(fs)
        self._processing_delay = self.get_processing_delay()

    def __del__(self):
        """
        Call Destructor.

        Returns
        -------
        None.

        """
        print(f"Destroying AFSTFT instance at {self._afstft_handle[0]}")
        lib.afSTFT_destroy(self._afstft_handle)

    def get_num_bands(self):
        """
        Return number of frequency bands.

        Returns
        -------
        int
            Number of frequency bands.

        """
        return lib.afSTFT_getNBands(self._afstft_handle[0])

    def get_center_freqs(self, fs):
        """
        Calculate center frequencies of filterbank.

        Parameters
        ----------
        fs : float
            DESCRIPTION.

        Returns
        -------
        freqs : np.array
            DESCRIPTION.

        """
        num_bands = self._num_bands
        freqs = np.zeros(num_bands, dtype=np.float32)
        lib.afSTFT_getCentreFreqs(self._afstft_handle[0], fs, num_bands,
                                  ffi.from_buffer("float []", freqs))
        return freqs

    def get_processing_delay(self):
        """
        Return current processing delay, in samples.

        Returns
        -------
        int
            DESCRIPTION.

        """
        return lib.afSTFT_getProcDelay(self._afstft_handle[0])



