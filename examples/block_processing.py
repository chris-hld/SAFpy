#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 16:15:54 2022

@author: chris
"""
from pathlib import Path
import numpy as np
import safpy
import soundfile
import sounddevice

import matplotlib.pyplot as plt


in_sig, fs = soundfile.read(Path("../data/music_snares.wav"), always_2d=1)
in_sig = in_sig.T
num_ch = in_sig.shape[0]
hopsize = 128
blocksize = 8*hopsize

in_sig = np.hstack((np.zeros((num_ch, blocksize)), in_sig))

hSTFT = safpy.afstft.AfSTFT(num_ch, num_ch, hopsize, fs, afstft_format=0)
hDecor = safpy.decorrelator.LatticeDecorrelator(fs, hopsize,
                                                hSTFT.center_freqs, num_ch)
hDucker = safpy.decorrelator.TransientDucker(num_ch, len(hSTFT.center_freqs))
out_sig = np.zeros_like(in_sig)

hSTFT.clear_buffers()
hDecor.clear_buffers()

blk_idx = 0
while blk_idx+blocksize <= in_sig.shape[1]:
    blk_in = in_sig[:, range(blk_idx, blk_idx+blocksize)]

    # afstft
    fd_sig_in = hSTFT.forward(blk_in)
    # transient ducker
    fd_res, fd_trs = hDucker.apply(fd_sig_in, alpha=0.9)
    # decorrelate transient ducker residual
    fd_decor = hDecor.apply(fd_res)
    # add a bit of transient back
    fd_decor += 1*fd_trs
    # back
    blk_out = hSTFT.backward(fd_decor)
    out_sig[:, range(blk_idx, blk_idx+blocksize)] = blk_out
    blk_idx += blocksize

sounddevice.sleep(100)
sounddevice.play(in_sig.T, samplerate=fs, blocking=True)
sounddevice.sleep(100)
sounddevice.play(out_sig.T, samplerate=fs, blocking=True)

plt.figure()
plt.plot(in_sig.T, label="in")
plt.plot(out_sig[:, hSTFT.processing_delay:].T, label="out")
plt.legend()
plt.show()
