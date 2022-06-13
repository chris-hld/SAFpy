import numpy as np
import safpy


safpy.utils.whoami()
Y_real = safpy.sh.getSHreal(1, [0, 0])
Y_cpx = safpy.sh.getSHcomplex(1, [0, 0])
vbap_gt = safpy.vbap.generateVBAPgainTable3D(np.reshape(np.arange(10), (5, 2)),
                                         1, 1, 0, 0, 0)

hSTFT = safpy.afstft.AfSTFT(2, 2, 128, fs=48000)

in_sig = np.random.randn(2, 8*128)
fd_sig = hSTFT.forward(in_sig)
fd_sig = hSTFT.forward_nd(in_sig)

out_sig = hSTFT.backward(fd_sig)
out_sig = hSTFT.backward_nd(fd_sig)

