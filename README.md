# SAFpy

This is a Python binding / wrapper for
https://github.com/leomccormack/Spatial_Audio_Framework

So far, there are a bunch of functions exposed, please feel free to 
add/contribute more if needed!


Prerequisites
---
1. Compile SAF, see instructions in its docs
2. Install numpy and CFFI, e.g. `conda install numpy cffi`

Now we need to build *safpy*, which creates the module. 
Running `pip install -e .` builds it automatically, you can run it manually 
(e.g. for debugging with `python safpy_build.py`)

By default, it assumes SAF in a folder parallel to safpy. You can simply adapt
the variable `saf_path` if needed.

Install
---
`pip install -e . `

Test
---
`pytest -vvv`

Usage
---
We can now use *safpy* as a python module.
Have a look at `examples/test_call.py`!
