import numpy as np

from _safpy import ffi, lib


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

        afstft_phandle = ffi.new("void **")
        self._afstft_phandle = afstft_phandle  # keep alive

        lib.afSTFT_create(afstft_phandle,
                          num_ch_in, num_ch_out, hopsize,
                          LOWDELAYMODE, HYBRIDMODE, afstft_format)
        print(f"Created AFSTFT instance at {self._afstft_phandle[0]}")

        # flush
        self.clear_buffers()

        self._fs = fs
        self._hopsize = hopsize

        self._num_bands = None
        self._center_freqs = None
        self._processing_delay = None

        self._num_ch_in = num_ch_in
        self._num_ch_out = num_ch_out

    def __del__(self):
        """
        Call Destructor.

        Returns
        -------
        None.

        """
        print(f"Destroying AFSTFT instance at {self._afstft_phandle[0]}")
        lib.afSTFT_destroy(self._afstft_phandle)

    @property
    def fs(self):
        return self._fs

    @property
    def hopsize(self):
        return self._hopsize

    @property
    def num_bands(self):
        """
        Return number of frequency bands.

        Returns
        -------
        int
            Number of frequency bands.

        """
        if self._num_bands is None:
            self._num_bands = lib.afSTFT_getNBands(self._afstft_phandle[0])
        return self._num_bands

    @property
    def center_freqs(self):
        """
        Return center frequencies of filterbank.

        Returns
        -------
        freqs : np.array
            DESCRIPTION.

        """
        if self._center_freqs is None:
            freqs = np.zeros(self.num_bands, dtype=np.float32)
            lib.afSTFT_getCentreFreqs(self._afstft_phandle[0], self.fs,
                                      self.num_bands,
                                      ffi.from_buffer("float []", freqs))
            self._center_freqs = freqs
        return self._center_freqs

    @property
    def processing_delay(self):
        """
        Return current processing delay, in samples.

        Returns
        -------
        int
            DESCRIPTION.

        """
        if self._processing_delay is None:
            self._processing_delay = lib.afSTFT_getProcDelay(
                                        self._afstft_phandle[0])
        return self._processing_delay

    def clear_buffers(self):
        """
        Flushes time-domain buffers with zeros.
        """
        lib.afSTFT_clearBuffers(self._afstft_phandle[0])

    def forward(self, in_frame_td):
        """
        Forward afSTFT.

        Parameters
        ----------
        in_frame_td : ndarray [num_ch, framesize]
            Time domain signals.

        Returns
        -------
        data_fd : ndarray [num_bands, num_ch_in, num_hops]
            Transformed signals.

        """
        assert(in_frame_td.ndim == 2)
        in_frame_td = np.ascontiguousarray(in_frame_td, dtype=np.float32)

        num_ch_in = in_frame_td.shape[0]
        assert(num_ch_in == self._num_ch_in)
        framesize = in_frame_td.shape[1]
        assert(framesize % self.hopsize == 0)
        num_hops = framesize // self.hopsize
        num_bands = self.num_bands

        data_fd = np.ones((num_bands, num_ch_in, num_hops),
                          dtype=np.complex64)

        lib.afSTFT_forward_flat(self._afstft_phandle[0],
                                ffi.from_buffer("float *", in_frame_td),
                                framesize,
                                ffi.from_buffer("float_complex *", data_fd))
        return data_fd

    def backward(self, in_frame_fd):
        """
        Backward afSTFT.

        Parameters
        ----------
        in_frame_fd : ndarray [num_bands, num_ch_in, num_hops]
            Transformed signals.

        Returns
        -------
        data_td : ndarray [num_ch, framesize]
            Time domain signals.

        """
        assert(in_frame_fd.ndim == 3)
        in_frame_fd = np.ascontiguousarray(in_frame_fd, dtype=np.complex64)

        assert(in_frame_fd.shape[0] == self.num_bands)
        num_ch_out = in_frame_fd.shape[1]
        assert(num_ch_out == self._num_ch_out)
        num_hops = in_frame_fd.shape[2]
        framesize = num_hops * self.hopsize

        data_td = np.ones((num_ch_out, framesize), dtype=np.float32)

        lib.afSTFT_backward_flat(self._afstft_phandle[0],
                                 ffi.from_buffer("float_complex *",
                                                 in_frame_fd),
                                 framesize,
                                 ffi.from_buffer("float *", data_td))

        return data_td

    def forward_nd(self, in_frame_td):
        """Only for reference, using nd-arrays."""
        assert(in_frame_td.ndim == 2)
        in_frame_td = np.ascontiguousarray(in_frame_td, dtype=np.float32)

        num_ch_in = in_frame_td.shape[0]
        assert(num_ch_in == self._num_ch_in)
        framesize = in_frame_td.shape[1]
        assert(framesize % self.hopsize == 0)
        num_hops = framesize // self.hopsize
        num_bands = self.num_bands

        # populate
        data_td_ptr = ffi.new("float *[]", num_ch_in)
        for idx_ch in range(num_ch_in):
            data_td_ptr[idx_ch] = ffi.from_buffer("float *",
                                                  in_frame_td[idx_ch, :])

        data_fd_ptr = ffi.cast("float_complex ***",
                               lib.malloc3d(num_bands, num_ch_in, num_hops,
                                            ffi.sizeof("float_complex")))
        lib.afSTFT_forward(self._afstft_phandle[0], data_td_ptr, framesize,
                           data_fd_ptr)

        # unpack
        data_fd = np.reshape(np.frombuffer(ffi.buffer(data_fd_ptr[0][0],
                                           num_bands*num_ch_in*num_hops *
                                           ffi.sizeof("float_complex")),
                                           dtype=np.complex64),
                             (num_bands, num_ch_in, num_hops))

        # ffi.release(data_td_ptr)  # managed
        return data_fd

    def backward_nd(self, in_frame_fd):
        """Only for reference, using nd-arrays."""
        assert(in_frame_fd.ndim == 3)
        in_frame_fd = np.ascontiguousarray(in_frame_fd, dtype=np.complex64)

        num_ch_out = in_frame_fd.shape[1]
        assert(num_ch_out == self._num_ch_out)
        num_hops = in_frame_fd.shape[2]
        framesize = num_hops * self.hopsize
        num_bands = self.num_bands

        # populate
        data_fd_ptr = ffi.cast("float_complex ***",
                               lib.malloc2d(num_bands, num_ch_out,
                                            ffi.sizeof("float_complex*")))
        for idx_band in range(num_bands):
            for idx_ch in range(num_ch_out):
                data_fd_ptr[idx_band][idx_ch] = \
                    ffi.from_buffer("float_complex *",
                                    in_frame_fd[idx_band, idx_ch, :])

        data_td_ptr = ffi.cast("float **", lib.malloc2d(num_ch_out, framesize,
                                                        ffi.sizeof("float")))
        lib.afSTFT_backward(self._afstft_phandle[0], data_fd_ptr, framesize,
                            data_td_ptr)

        # unpack
        data_td = np.reshape(np.frombuffer(ffi.buffer(data_td_ptr[0],
                                           num_ch_out*framesize *
                                           ffi.sizeof("float")),
                                           dtype=np.float32),
                             (num_ch_out, framesize))

        lib.free(data_fd_ptr)

        return data_td
