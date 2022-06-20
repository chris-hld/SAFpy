import numpy as np
import safpy


safpy.utils.whoami()
Y_real = safpy.sh.getSHreal(1, [0, 0])
Y_cpx = safpy.sh.getSHcomplex(1, [0, 0])
vbap_gt = safpy.vbap.generateVBAPgainTable3D(np.reshape(np.arange(10), (5, 2)),
                                             1, 1, 0, 0, 0)

hSTFT = safpy.afstft.AfSTFT(2, 2, 128, fs=48000)
hSTFT.center_freqs
in_sig = np.hstack((np.zeros((2, 128)), np.random.randn(2, 8*128)))
fd_sig = hSTFT.forward(in_sig)
out_sig = hSTFT.backward(fd_sig)

hDecor = safpy.decorrelator.LatticeDecorrelator(48000, 128, hSTFT.center_freqs,
                                                2, [20, 15, 6, 3],
                                                [0.6e3, 2.4e3, 4e3, 12e3], 8)
fd_sig_decor = hDecor.apply(fd_sig)
