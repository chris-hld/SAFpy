# SAFpy
WIP

This is a Python interface / wrapper for
https://github.com/leomccormack/Spatial_Audio_Framework


Prerequisites
---
1. Compile SAF, see instructions in its docs
2. Install numpy and CFFI, e.g. `conda install numpy cffi`

Now we need to build *safpy*, which creates the module with

`python safpy/safpy_build.py`

By default, it assumes SAF in a folder parallel to safpy. You can simply adapt
the variable `saf_path` if needed.

Test
---
`pytest -vvv`

Usage
---
We can now use *safpy* as a python module.
Have a look at test_call.py!
