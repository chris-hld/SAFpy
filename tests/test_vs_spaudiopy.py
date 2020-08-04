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


def test_getSHreal():
    num_dirs = 3
    rg = np.random.default_rng()
    azi = rg.uniform(0, 2*np.pi, num_dirs)
    zen = rg.uniform(0, np.pi, num_dirs)
    n_sph = 10
    a = safpy.wrapit.getSHreal(n_sph, np.c_[azi, zen])
    b = spa.sph.sh_matrix(n_sph, azi, zen, SH_type='real').astype(np.float32)

    assert_allclose(a, b.T, atol=10e-6)


def test_getSHcomplex():
    num_dirs = 3
    rg = np.random.default_rng()
    azi = rg.uniform(0, 2*np.pi, num_dirs)
    zen = rg.uniform(0, np.pi, num_dirs)
    n_sph = 10
    a = safpy.wrapit.getSHcomplex(n_sph, np.c_[azi, zen])
    b = spa.sph.sh_matrix(n_sph, azi, zen, SH_type='complex').astype(
        np.complex64)

    assert_allclose(a, b.T, atol=10e-6)


test_getSHreal()
test_getSHcomplex()