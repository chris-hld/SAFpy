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

import spaudiopy as spa
import safpy


def test_whoami():
    safpy.utils.whoami()


def test_getSHreal():
    num_dirs = 3
    rg = np.random.default_rng()
    azi = rg.uniform(0, 2*np.pi, num_dirs)
    zen = rg.uniform(0, np.pi, num_dirs)
    n_sph = 10
    a = safpy.sh.getSHreal(n_sph, np.c_[azi, zen])
    b = spa.sph.sh_matrix(n_sph, azi, zen, SH_type='real').astype(np.float32)

    assert_allclose(a, b.T, atol=10e-6)


def test_getSHcomplex():
    num_dirs = 3
    rg = np.random.default_rng()
    azi = rg.uniform(0, 2*np.pi, num_dirs)
    zen = rg.uniform(0, np.pi, num_dirs)
    n_sph = 10
    a = safpy.sh.getSHcomplex(n_sph, np.c_[azi, zen])
    b = spa.sph.sh_matrix(n_sph, azi, zen, SH_type='complex').astype(
        np.complex64)

    assert_allclose(a, b.T, atol=10e-6)


def test_vbap_gaintable_3d():
    vecs = spa.grids.load_t_design(10)
    azi, zen, r = spa.utils.cart2sph(*vecs.T)
    azi_deg = spa.utils.rad2deg(azi)
    zen_deg = spa.utils.rad2deg(zen)
    gt = safpy.vbap.generateVBAPgainTable3D(np.c_[azi_deg, zen_deg-90], 1, 1)

    assert(np.all(np.count_nonzero(gt, axis=1) <= 3))
    assert_allclose(np.sum(gt**2, axis=1), np.ones(gt.shape[0]), atol=10e-6)


def test_afstft():
    num_in = 2
    num_out = 2
    hopsize = 128

    h = safpy.afstft.AfSTFT(num_in, num_out, hopsize, fs=48000)
    in_sig = np.random.randn(num_in, 4096)

    data_fd_f = h.forward(in_sig)
    data_td_f = h.backward(data_fd_f)

    h.clear_buffers()
    data_fd = h.forward_slow(in_sig)
    data_td = h.backward_slow(data_fd)

    np.testing.assert_allclose(data_td, data_td_f)
    np.testing.assert_allclose(in_sig[:, :-h.get_processing_delay()],
                               data_td[:, h.get_processing_delay():],
                               atol=10e-3)
