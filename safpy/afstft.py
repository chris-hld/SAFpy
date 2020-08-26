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

        afstft_handle = ffi.new("void **")

        lib.afSTFT_create(afstft_handle,
                          num_ch_in, num_ch_out, hopsize,
                          LOWDELAYMODE, HYBRIDMODE, afstft_format)
        self._afstft_handle = afstft_handle  # keep alive
        print(f"Created AFSTFT instance at {self._afstft_handle[0]}")

        # flush
        self.clear_buffers()

        self._num_bands = self.get_num_bands()
        self._center_freqs = self.get_center_freqs(fs)
        self._processing_delay = self.get_processing_delay()

        self._num_ch_in = num_ch_in
        self._num_ch_out = num_ch_out
        self._hopsize = hopsize

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

    def clear_buffers(self):
        """
        Flushes time-domain buffers with zeros.

        Returns
        -------
        None.

        """
        lib.afSTFT_clearBuffers(self._afstft_handle[0])

    def forward(self, in_frame_td):
        """
        

        Parameters
        ----------
        in_frame_td : TYPE
            DESCRIPTION.

        Returns
        -------
        data_fd : TYPE
            DESCRIPTION.

        """
        in_frame_td = np.atleast_2d(in_frame_td)
        in_frame_td = np.ascontiguousarray(in_frame_td, dtype=np.float32)

        num_ch_in = in_frame_td.shape[0]
        assert(num_ch_in == self._num_ch_in)
        framesize = in_frame_td.shape[1]
        assert(framesize % self._hopsize == 0)
        num_hops = framesize // self._hopsize

        num_bands = self._num_bands

        data_fd = np.ones((num_bands, num_ch_in, num_hops),
                          dtype=np.complex64)

        lib.afSTFT_forward_flat(self._afstft_handle[0],
                                ffi.from_buffer("float *", in_frame_td),
                                framesize,
                                ffi.from_buffer("float_complex *", data_fd))
        return data_fd

    def backward(self, in_frame_fd):
        """
        

        Parameters
        ----------
        in_frame_fd : TYPE
            DESCRIPTION.

        Returns
        -------
        data_td : TYPE
            DESCRIPTION.

        """
        assert(in_frame_fd.ndim == 3)
        in_data_fd = np.ascontiguousarray(in_frame_fd, dtype=np.complex64)

        num_ch_out = in_data_fd.shape[1]
        assert(num_ch_out == self._num_ch_out)
        num_hops = in_data_fd.shape[2]
        framesize = num_hops * self._hopsize

        data_td = np.ones((num_ch_out, framesize), dtype=np.float32)

        lib.afSTFT_backward_flat(self._afstft_handle[0],
                                 ffi.from_buffer("float_complex *",
                                                 in_frame_fd),
                                 framesize,
                                 ffi.from_buffer("float *", data_td))

        return data_td

    def forward_slow(self, in_frame_td):
        """Only for reference."""
        in_frame_td = np.atleast_2d(in_frame_td)
        in_frame_td = np.ascontiguousarray(in_frame_td, dtype=np.float32)

        num_ch_in = in_frame_td.shape[0]
        assert(num_ch_in == self._num_ch_in)
        framesize = in_frame_td.shape[1]
        assert(framesize % self._hopsize == 0)
        num_hops = framesize // self._hopsize

        num_bands = self._num_bands

        data_td_ptr = ffi.cast("float **",
                               lib.malloc2d(num_ch_in, framesize,
                                            ffi.sizeof("float")))
        data_fd_ptr = ffi.cast("float_complex ***",
                               lib.malloc3d(num_bands, num_ch_in, num_hops,
                                            ffi.sizeof("float_complex")))

        # populate
        for idx_ch in range(num_ch_in):
            data_td_ptr[idx_ch] = ffi.from_buffer("float *",
                                                  in_frame_td[idx_ch, :])

        lib.afSTFT_forward(self._afstft_handle[0], data_td_ptr, framesize,
                           data_fd_ptr)

        # unpack
        data_fd = np.reshape(np.array(ffi.unpack(data_fd_ptr[0][0],
                                                 num_bands*num_ch_in*num_hops),
                                      dtype=np.complex64, ndmin=3),
                             (num_bands, num_ch_in, num_hops))

        lib.free(data_td_ptr)
        lib.free(data_fd_ptr)

        return data_fd

    def backward_slow(self, in_data_fd):
        """Only for reference."""
        in_data_fd = np.ascontiguousarray(in_data_fd, dtype=np.complex64)

        num_bands = self._num_bands
        num_ch_out = in_data_fd.shape[1]
        assert(num_ch_out == self._num_ch_out)
        num_hops = in_data_fd.shape[2]
        framesize = num_hops * self._hopsize

        data_fd_ptr = ffi.cast("float_complex ***",
                               lib.malloc3d(num_bands, num_ch_out, num_hops,
                                            ffi.sizeof("float_complex")))

        data_td_ptr = ffi.cast("float **", lib.malloc2d(num_ch_out, framesize,
                                                        ffi.sizeof("float")))

        # populate
        for idx_band in range(num_bands):
            for idx_ch in range(num_ch_out):
                data_fd_ptr[idx_band][idx_ch] = \
                    ffi.from_buffer("float_complex *",
                                    in_data_fd[idx_band, idx_ch, :])

        lib.afSTFT_backward(self._afstft_handle[0], data_fd_ptr, framesize,
                            data_td_ptr)

        # unpack
        data_td = np.reshape(np.array(ffi.unpack(data_td_ptr[0],
                                                 num_ch_out*framesize),
                                      dtype=np.float32, ndmin=2),
                             (num_ch_out, framesize))

        lib.free(data_td_ptr)
        lib.free(data_fd_ptr)

        return data_td
