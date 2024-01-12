# SAFpy

[![Python application](https://github.com/chris-hld/SAFpy/actions/workflows/python-safpy.yml/badge.svg)](https://github.com/chris-hld/SAFpy/actions/workflows/python-safpy.yml)

This is a Python binding / wrapper for
https://github.com/leomccormack/Spatial_Audio_Framework

So far, there are a bunch of functions exposed, please feel free to 
add/contribute more if needed!


Prerequisites
---
1. Compile SAF, provided as a submodule, see instructions in its [docs](https://github.com/leomccormack/Spatial_Audio_Framework/blob/master/README.md)
2. Install numpy and CFFI, e.g. `conda install numpy cffi`
3. Now we need to build *safpy*, which creates the module. 
Running `pip install -e .` builds it automatically

(you can also build manually, e.g., for debugging, with 
`python safpy_build.py`)

By default, it assumes SAF in a subdirectory, which is obtained by `git submodule update --init --recursive `. You can simply adapt
the variable `saf_path` in `safpy_build.py` if needed.

If in trouble you can have a look at the CI steps [here](https://github.com/chris-hld/SAFpy/blob/master/.github/workflows/python-safpy.yml).

Install
---
`pip install -e . `

Test
---
`pytest -vvv`

Usage
---
Use *safpy* as a python package.
Have a look at `examples/test_call.py`!
