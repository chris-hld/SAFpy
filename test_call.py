from safpy import wrapit
from safpy._safpy import ffi, lib


wrapit.whoami()
print(lib.factorial(3))
