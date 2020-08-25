import numpy as np
import safpy


safpy.wrapit.whoami()
print(safpy.wrapit.factorial(3))
print(safpy.sh.getSHreal(1, [0, 0]))
print(safpy.sh.getSHcomplex(1, [0, 0]))
print(safpy.vbap.generateVBAPgainTable3D(np.reshape(np.arange(10), (5, 2)),
                                         1, 1, 0, 0, 0))
h = safpy.afstft.AfSTFT(2, 2, 128, fs=48000)
in_sig = np.random.randn(2, 4096)
#in_sig = np.zeros((2, 4096))

#data_fd = h.forward(in_sig)

#data_fd_f = h.forward_flat(in_sig)
#data_td_f = h.backward_flat(data_fd_f)

data_fd = h.forward(in_sig)
data_td = h.backward(data_fd)

