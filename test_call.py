import numpy as np
import safpy


safpy.wrapit.whoami()
print(safpy.wrapit.factorial(3))
print(safpy.wrapit.getSHreal(1, [0, 0]))
print(safpy.wrapit.getSHcomplex(1, [0, 0]))
print(safpy.wrapit.generateVBAPgainTable3D(np.reshape(np.arange(10), (5, 2)),
                                           1, 1, 0, 0, 0))
