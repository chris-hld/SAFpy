import numpy as np

from _safpy import ffi, lib


class LatticeDecorrelator():
    """."""

    def __init__(self, fs, hopsize, freq_vec, num_ch, orders=[20, 15, 6, 3],
                 freq_cutoffs=[0.6e3, 2.4e3, 4e3, 12e3], max_delay=8,
                 lookup_offset=0, en_comp=0.75):
        """
        Call Constructor.

        Parameters
        ----------
        fs : TYPE
            DESCRIPTION.
        hopsize : TYPE
            DESCRIPTION.
        freq_vec : TYPE
            DESCRIPTION.
        num_ch : TYPE
            DESCRIPTION.
        orders : TYPE, optional
            DESCRIPTION. The default is [20, 15, 6, 3].
        freq_cutoffs : TYPE, optional
            DESCRIPTION. The default is [0.6e3, 2.4e3, 4e3, 12e3].
        max_delay : TYPE, optional
            DESCRIPTION. The default is 8.
        lookup_offset : TYPE, optional
            DESCRIPTION. The default is 0.
        en_comp : TYPE, optional
            DESCRIPTION. The default is 0.75.

        Returns
        -------
        None.

        """
        decorrelator_phandle = ffi.new("void **")
        self._decorrelator_phandle = decorrelator_phandle  # keep alive

        freq_vec = np.asarray(freq_vec, dtype=np.float32)
        freq_cutoffs = np.asarray(freq_cutoffs, dtype=np.float32)
        orders = np.asarray(orders, dtype=np.int32)
        num_bands = len(freq_vec)
        num_cutoffs = len(freq_cutoffs)

        lib.latticeDecorrelator_create(decorrelator_phandle,
                                       fs, hopsize,
                                       ffi.from_buffer("float *", freq_vec),
                                       num_bands, num_ch,
                                       ffi.from_buffer("int *", orders),
                                       ffi.from_buffer("float *",
                                                       freq_cutoffs),
                                       num_cutoffs, max_delay,
                                       lookup_offset, en_comp)
        print("Created decorrelator instance at "
              f"{self._decorrelator_phandle[0]}")

        # flush
        self.clear_buffers()

        self._fs = fs
        self._hopsize = hopsize
        self._num_ch = num_ch
        self._num_bands = num_bands
        self._center_freqs = freq_vec
        self._max_delay = max_delay

    def __del__(self):
        """
        Call Destructor.

        Returns
        -------
        None.

        """
        print("Destroying decorrelator instance at "
              f"{self._decorrelator_phandle[0]}")
        lib.latticeDecorrelator_destroy(self._decorrelator_phandle)

    @property
    def fs(self):
        return self._fs

    @property
    def hopsize(self):
        return self._hopsize

    @property
    def num_ch(self):
        return self._num_ch

    @property
    def num_bands(self):
        return self._num_bands

    @property
    def center_freqs(self):
        return self._center_freqs

    @property
    def max_delay(self):
        return self._max_delay

    def clear_buffers(self):
        """
        Flushes internal buffers to zeros.

        Returns
        -------
        None.

        """
        lib.latticeDecorrelator_reset(self._decorrelator_phandle[0])

    def apply(self, in_frame_fd):
        """
        Apply decorrelation.

        Parameters
        ----------
        in_frame_fd : ndarray [num_bands, num_ch_in, num_t_slots]

        Returns
        -------
        out_frame_fd : ndarray [num_bands, num_ch_in, num_t_slots]

        """
        assert(in_frame_fd.ndim == 3)
        in_frame_fd = np.ascontiguousarray(in_frame_fd, dtype=np.complex64)

        num_bands = in_frame_fd.shape[0]
        assert(num_bands == self.num_bands)
        num_ch = in_frame_fd.shape[1]
        assert(num_ch == self.num_ch)
        num_t_slots = in_frame_fd.shape[2]

        # populate
        data_in_ptr = ffi.cast("float _Complex ***",
                               lib.malloc2d(num_bands, num_ch,
                                            ffi.sizeof("float _Complex *")))
        for idx_band in range(num_bands):
            for idx_ch in range(num_ch):
                data_in_ptr[idx_band][idx_ch] = \
                    ffi.from_buffer("float _Complex *",
                                    in_frame_fd[idx_band, idx_ch, :])

        data_out_ptr = ffi.cast("float _Complex ***",
                                lib.malloc3d(num_bands, num_ch, num_t_slots,
                                             ffi.sizeof("float _Complex *")))
        lib.latticeDecorrelator_apply(self._decorrelator_phandle[0],
                                      data_in_ptr, num_t_slots, data_out_ptr)

        # unpack
        data_out = np.reshape(np.frombuffer(ffi.buffer(data_out_ptr[0][0],
                                            num_bands*num_ch*num_t_slots *
                                            ffi.sizeof("float _Complex")),
                                            dtype=np.complex64),
                              (num_bands, num_ch, num_t_slots))

        lib.free(data_in_ptr)
        return data_out


class TransientDucker():
    """."""

    def __init__(self, num_ch, num_bands):
        """
        Call Constructor.

        Parameters
        ----------
        num_ch : TYPE
            DESCRIPTION.
        num_bands : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        ducker_phandle = ffi.new("void **")
        self._ducker_phandle = ducker_phandle  # keep alive

        lib.transientDucker_create(ducker_phandle, num_ch, num_bands)
        print("Created transient ducker instance at "
              f"{self._ducker_phandle[0]}")

        self._num_ch = num_ch
        self._num_bands = num_bands

    def __del__(self):
        """
        Call Destructor.

        Returns
        -------
        None.

        """
        print("Destroying transient ducker instance at "
              f"{self._ducker_phandle[0]}")
        lib.transientDucker_destroy(self._ducker_phandle)

    @property
    def num_ch(self):
        return self._num_ch

    @property
    def num_bands(self):
        return self._num_bands

    def apply(self, in_frame_fd, alpha=0.95, beta=0.995):
        """
        Apply transient ducker.

        Parameters
        ----------
        in_frame_fd : ndarray [num_bands, num_ch_in, num_t_slots]

        Returns
        -------
        res_frame_fd : ndarray [num_bands, num_ch_in, num_t_slots]
        trs_frame_fd : ndarray [num_bands, num_ch_in, num_t_slots]

        """
        assert(in_frame_fd.ndim == 3)
        in_frame_fd = np.ascontiguousarray(in_frame_fd, dtype=np.complex64)

        num_bands = in_frame_fd.shape[0]
        assert(num_bands == self.num_bands)
        num_ch = in_frame_fd.shape[1]
        assert(num_ch == self.num_ch)
        num_t_slots = in_frame_fd.shape[2]

        # populate
        data_in_ptr = ffi.cast("float _Complex ***",
                               lib.malloc2d(num_bands, num_ch,
                                            ffi.sizeof("float _Complex *")))
        for idx_band in range(num_bands):
            for idx_ch in range(num_ch):
                data_in_ptr[idx_band][idx_ch] = \
                    ffi.from_buffer("float _Complex *",
                                    in_frame_fd[idx_band, idx_ch, :])

        data_res_ptr = ffi.cast("float _Complex ***",
                                lib.malloc3d(num_bands, num_ch, num_t_slots,
                                             ffi.sizeof("float _Complex *")))

        data_trs_ptr = ffi.cast("float _Complex ***",
                                lib.malloc3d(num_bands, num_ch, num_t_slots,
                                             ffi.sizeof("float _Complex *")))
        lib.transientDucker_apply(self._ducker_phandle[0],
                                  data_in_ptr, num_t_slots, alpha, beta,
                                  data_res_ptr, data_trs_ptr)

        # unpack
        data_res = np.reshape(np.frombuffer(ffi.buffer(data_res_ptr[0][0],
                                            num_bands*num_ch*num_t_slots *
                                            ffi.sizeof("float _Complex")),
                                            dtype=np.complex64),
                              (num_bands, num_ch, num_t_slots))
        data_trs = np.reshape(np.frombuffer(ffi.buffer(data_trs_ptr[0][0],
                                            num_bands*num_ch*num_t_slots *
                                            ffi.sizeof("float _Complex")),
                                            dtype=np.complex64),
                              (num_bands, num_ch, num_t_slots))
        lib.free(data_in_ptr)
        return data_res, data_trs
