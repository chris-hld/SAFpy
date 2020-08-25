import numpy as np
import safpy


safpy.wrapit.whoami()
print(safpy.wrapit.factorial(3))
print(safpy.sh.getSHreal(1, [0, 0]))
print(safpy.sh.getSHcomplex(1, [0, 0]))
print(safpy.vbap.generateVBAPgainTable3D(np.reshape(np.arange(10), (5, 2)),
                                         1, 1, 0, 0, 0))
h = safpy.afstft.AfSTFT(2, 2, 128, fs=48000)
in_sig = np.random.randn(2, 2048)
data_fd = h.forward(in_sig)
