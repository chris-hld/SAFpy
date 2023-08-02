#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 13:57:41 2020

@author: chris
"""
import numpy as np
from numpy.testing import assert_allclose
import pytest

# import sys
# sys.path.append("../")   # this adds the mother folder

import numpy as np
import safpy


def test_whoami():
    safpy.utils.whoami()


def test_vbap_gaintable_3d():
    azi_deg = np.random.uniform(0, 360, 100)
    zen_deg = np.random.uniform(0, 180, 100)
    gt = safpy.vbap.generateVBAPgainTable3D(np.c_[azi_deg, zen_deg-90], 1, 1)

    assert(np.all(np.count_nonzero(gt, axis=1) <= 3))
    assert_allclose(np.sum(gt**2, axis=1), np.ones(gt.shape[0]), atol=10e-6)


def test_afstft():
    num_in = 2
    num_out = 2
    hopsize = 128

    h = safpy.afstft.AfSTFT(num_in, num_out, hopsize, fs=48000)
    in_sig = np.random.randn(num_in, 1000*4096)

    data_fd = h.forward(in_sig)
    data_td = h.backward(data_fd)

    np.testing.assert_allclose(in_sig[:, :-h.processing_delay],
                               data_td[:, h.processing_delay:],
                               atol=10e-3)


def test_afstft_nd():
    num_in = 2
    num_out = 2
    hopsize = 128

    h = safpy.afstft.AfSTFT(num_in, num_out, hopsize, fs=48000,
                            afstft_format=0)
    in_sig = np.random.randn(num_in, 1000*4096)

    data_fd = h.forward_nd(in_sig)
    data_td = h.backward_nd(data_fd)

    np.testing.assert_allclose(in_sig[:, :-h.processing_delay],
                               data_td[:, h.processing_delay:],
                               atol=10e-3)


def test_afstft_compare():
    num_in = 2
    num_out = 2
    hopsize = 128

    h = safpy.afstft.AfSTFT(num_in, num_out, hopsize, fs=48000,
                            afstft_format=0)
    in_sig = np.random.randn(num_in, 4096)

    data_fd_f = h.forward(in_sig)
    data_td_f = h.backward(data_fd_f)

    h.clear_buffers()
    data_fd_s = h.forward_nd(in_sig)
    data_td_s = h.backward_nd(data_fd_s)

    np.testing.assert_allclose(data_td_s, data_td_f)
    np.testing.assert_allclose(in_sig[:, :-h.processing_delay],
                               data_td_s[:, h.processing_delay:],
                               atol=10e-3)


def test_getSH_variants():
    num_dirs = 3
    rg = np.random.default_rng()
    azi = rg.uniform(0, 2*np.pi, num_dirs)
    zen = rg.uniform(0, np.pi, num_dirs)
    N_sph = 5
    a = safpy.sh.getSHreal(N_sph, np.c_[azi, zen])
    b = safpy.sh.getSHreal_recur(N_sph, np.c_[azi, zen])
    c0 = safpy.sh.getSHreal_part(0, N_sph, np.c_[azi, zen])
    c1 = safpy.sh.getSHreal_part(1, N_sph, np.c_[azi, zen])
    assert_allclose(a, b, atol=10e-3)
    assert_allclose(a, c0, atol=10e-3)
    assert_allclose(a[1:, :], c1[1:, :], atol=10e-3)
